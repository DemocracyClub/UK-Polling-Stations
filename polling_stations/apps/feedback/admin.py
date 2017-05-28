from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('found_useful',)
    list_display = ('found_useful', 'comments',)
    readonly_fields = [f.name for f in Feedback._meta.get_fields()]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Feedback, FeedbackAdmin)
