import asana
from django.conf import settings
from django.contrib import admin


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


class AsanaUrlExistsFilter(admin.SimpleListFilter):
    title = "URL Exists"
    parameter_name = "has_asana_url"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(asana_url__exact="")
        if self.value() == "no":
            return queryset.filter(asana_url__exact="")
        return queryset


@admin.action(description="Send to Asana")
def send_to_asana(modeladmin, request, queryset):
    queryset = queryset.filter(asana_url__exact="")
    configuration = asana.Configuration()
    configuration.access_token = settings.ASANA_TOKEN
    api_client = asana.ApiClient(configuration)

    tasks_api_instance = asana.TasksApi(api_client)

    for instance in queryset:
        task_details = instance.as_asana_object()

        opts = {"opt_fields": ",".join(settings.ASANA_OPT_FIELDS)}

        created_task = tasks_api_instance.create_task({"data": task_details}, opts)
        instance.asana_url = created_task["permalink_url"]
        instance.save()
