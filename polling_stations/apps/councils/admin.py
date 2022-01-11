from django.contrib import admin

from councils.models import Council
from polling_stations.db_routers import get_logger_db_name

LOGGER_DB_NAME = get_logger_db_name()


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


class LoggerDBModelAdmin(admin.ModelAdmin):

    using = LOGGER_DB_NAME

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


class CouncilUserInline(admin.StackedInline):
    model = Council.users.through
    extra = 0


class CouncilAdmin(ReadOnlyModelAdminMixin, LoggerDBModelAdmin):
    inlines = [CouncilUserInline]
    search_fields = ["council_id", "name", "identifiers"]


admin.site.register(Council, CouncilAdmin)
