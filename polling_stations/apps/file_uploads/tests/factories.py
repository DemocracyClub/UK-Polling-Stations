from datetime import datetime

import factory
from councils.tests.factories import CouncilFactory
from file_uploads.models import File, Upload


class UploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Upload

    gss = factory.SubFactory(CouncilFactory)
    timestamp = factory.LazyFunction(datetime.now)


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = File

    upload = factory.SubFactory(UploadFactory)
    csv_valid = True
