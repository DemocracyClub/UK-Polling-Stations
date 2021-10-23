from django.urls import re_path, path
from .views import (
    CouncilListView,
    CouncilDetailView,
    FileDetailView,
    FileUploadView,
    CouncilLoginView,
    AuthenticateView,
)

app_name = "file_uploads"
urlpatterns = [
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
    path("authenticate/", AuthenticateView.as_view(), name="council_authenticate"),
]
