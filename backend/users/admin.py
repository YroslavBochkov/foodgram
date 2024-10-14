from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'role', 'id', 'first_name', 'last_name']
    list_editable = 'role',
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')
