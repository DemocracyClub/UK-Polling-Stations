from django.contrib import admin

from councils.models import Council


class ReadOnlyModelAdminMixin:
    def get_actions(self, request):
        actions = super(ReadOnlyModelAdminMixin, self).get_actions(request)
        del_action = "delete_selected"
        if del_action in actions:
            del actions[del_action]
        return actions

    def get_readonly_fields(self, request, obj=None):
        return (
            list(self.readonly_fields)
            + [field.name for field in obj._meta.fields]
            + [field.name for field in obj._meta.many_to_many]
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass


class CouncilUserInline(admin.StackedInline):
    model = Council.users.through
    extra = 0


class CouncilAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    inlines = [CouncilUserInline]
    search_fields = ["council_id", "name", "identifiers"]


admin.site.register(Council, CouncilAdmin)
