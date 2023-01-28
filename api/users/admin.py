from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
