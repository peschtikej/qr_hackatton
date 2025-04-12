from django.contrib import admin
from bot.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role')
    list_filter = ('role',)
    search_fields = ('user_id',)
    
    def __str__(self):
        return f"User {self.user_id} ({self.get_role_display()})"
