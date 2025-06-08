from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Article, Ticket

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    search_fields = ('username', 'email')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content')
    raw_id_fields = ('created_by',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('created_by', 'assigned_to')

admin.site.register(User, CustomUserAdmin)