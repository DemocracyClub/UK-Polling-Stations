from django.views.generic import TemplateView

class ApiDocsView(TemplateView):
    template_name = "api_docs/html/docs.html"
