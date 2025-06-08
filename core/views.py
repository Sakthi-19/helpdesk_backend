from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchVector, SearchQuery
import openai
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from .models import User, Article, Ticket
from .serializers import UserSerializer, ArticleSerializer, TicketSerializer, AIQuestionSerializer, MyTokenObtainPairSerializer
from .permissions import IsAdmin, IsSupportAgent, IsOwnerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        search_query = SearchQuery(query)
        results = Article.objects.annotate(
            search=SearchVector('title', 'content')
        ).filter(search=search_query)
        
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority', 'status', 'created_by', 'assigned_to']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Ticket.objects.none()  # avoid error when generating schema

        user = self.request.user

        if not user.is_authenticated:
            return Ticket.objects.none()  # or raise PermissionDenied

        if user.role == 'employee':
            return self.queryset.filter(created_by=user)
        elif user.role == 'agent':
            return self.queryset.filter(assigned_to=user)

        return self.queryset  # admin sees all

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@swagger_auto_schema(
    method='post',
    request_body=AIQuestionSerializer,
    responses={200: openapi.Response(description="AI-generated answer")}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_answer_view(request):
    serializer = AIQuestionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Now it's safe to access this
    question = serializer.validated_data['question']

    # Search KB articles for relevant context
    search_query = SearchQuery(question)
    articles = Article.objects.annotate(
        search=SearchVector('title', 'content')
    ).filter(search=search_query)[:3]

    context_text = "\n\n".join(f"{a.title}\n{a.content}" for a in articles)

    prompt = f"""You're an internal support AI. Use this context to answer the employee's question.

    Context:
    {context_text}

    Question:
    {question}

    Answer in a professional and helpful manner:"""

    try:
        if settings.OPENAI_API_KEY == "mock-api-key":
            response_text = "Mock AI response: Please contact your support team for assistance."
            confidence = 0.5
        else:
            openai.api_key = settings.OPENAI_API_KEY
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            response_text = completion.choices[0].message.content.strip()
            confidence = min(0.9 + (len(articles)/10), 1.0)

        return Response({
            "answer": response_text,
            "confidence": confidence,
            "sources": [{"title": a.title, "id": a.id} for a in articles]
        })

    except Exception as e:
        return Response({
            "error": "AI service is currently unavailable",
            "details": str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
