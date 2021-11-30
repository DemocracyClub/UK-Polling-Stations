from django.conf import settings


def canonical_url(request):
    return {"CANONICAL_URL": f"{request.scheme}://{request.get_host()}"}


def site_title(request):
    return {"SITE_TITLE": settings.SITE_TITLE}
