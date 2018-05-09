from apiblueprint_view.views import ApiBlueprintView

class ApiDocsView(ApiBlueprintView):

    blueprint = 'polling_stations/templates/api_docs/blueprints/wheredoivote.apibp'
    template_name = 'api_docs/api_base_template.html'
    styles = {
        'resource': {'class': 'card'},
        'resource_group': {'class': 'card'},
        'method_GET': {'class': 'badge success'},
    }
