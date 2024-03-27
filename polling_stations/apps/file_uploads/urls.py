from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from .views import (
    AccessibilityInformationUploadView,
    AuthenticateView,
    CouncilDetailView,
    CouncilListView,
    CouncilLoginView,
    FileDetailView,
    FileUploadView,
)

app_name = "file_uploads"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("file_uploads:councils_list"))),
    re_path(r"^councils/$", CouncilListView.as_view(), name="councils_list"),
    re_path(
        r"^councils/(?P<pk>.+)/$",
        CouncilDetailView.as_view(),
        name="councils_detail",
    ),
    re_path(
        r"^files/(?P<pk>.+)/$",
        FileDetailView.as_view(),
        name="files_detail",
    ),
    re_path(
        r"^upload_files/(?P<gss>.+)/$",
        FileUploadView.as_view(),
        name="file_upload",
    ),
    path("login/", CouncilLoginView.as_view(), name="council_login_view"),
    path(
        "about/",
        TemplateView.as_view(template_name="file_uploads/about.html"),
        name="council_uploader_alpha",
    ),
    path(
        "logout/",
        TemplateView.as_view(template_name="file_uploads/logout_confirm.html"),
        name="logout_confirm",
    ),
    path("authenticate/", AuthenticateView.as_view(), name="council_authenticate"),
    re_path(
        "^upload_accessibility_info/(?P<council_id>.+)/$",
        AccessibilityInformationUploadView.as_view(),
        name="accessibility_upload",
    ),
]
