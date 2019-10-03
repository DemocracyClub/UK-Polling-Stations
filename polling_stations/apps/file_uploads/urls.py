from django.conf.urls import url

from .views import FileUploadView

urlpatterns = [url(r"^$", FileUploadView.as_view(), name="file_upload_index")]
