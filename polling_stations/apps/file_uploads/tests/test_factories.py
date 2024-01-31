from django.test import TestCase
from file_uploads.tests.factories import FileFactory, UploadFactory


class UploadFactoryTest(TestCase):
    def test_upload_factory(self):
        upload = UploadFactory()
        self.assertTrue(upload.gss)

    def test_file_factory(self):
        file = FileFactory()
        self.assertTrue(file.upload)
