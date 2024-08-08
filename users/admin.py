from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Tutor

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_student', 'is_tutor')
    list_filter = ('is_student', 'is_tutor')
    search_fields = ('email',)
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
admin.site.register(User, UserAdmin)

class TutorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'year', 'courses', 'bio', 'rating', 'total_ratings')
    readonly_fields = ('rating', 'total_ratings')
    search_fields = ('user__email', 'first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        user = obj.user
        user.is_student = False
        user.is_tutor = True
        user.save()
        super().save_model(request, obj, form, change)

admin.site.register(Tutor, TutorAdmin)