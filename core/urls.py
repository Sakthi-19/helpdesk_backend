from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from .views import (
    CreateUserView,
    ArticleViewSet,
    TicketViewSet,
    ai_answer_view,
    UserProfileView,
    MyTokenView
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    # Authentication
    path('auth/register/', CreateUserView.as_view(), name='register'),
    path("auth/token/", MyTokenView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User Profile
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    
    # AI Assistant
    path('ai/answer/', ai_answer_view, name='ai-answer'),
    
    # Router URLs (Articles and Tickets)
    path('', include(router.urls)),
]
