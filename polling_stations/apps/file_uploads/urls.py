from django.conf.urls import url

from .views import CouncilListView, CouncilDetailView, FileDetailView, FileUploadView

app_name = "file_uploads"
urlpatterns = [
    url(r"^councils/$", CouncilListView.as_view(), name="councils_list"),
    url(
        r"^councils/(?P<pk>.+)/$", CouncilDetailView.as_view(), name="councils_detail",
    ),
    url(r"^files/(?P<pk>.+)/$", FileDetailView.as_view(), name="files_detail",),
    url(r"^upload_files/(?P<gss>.+)/$", FileUploadView.as_view(), name="file_upload",),
]
