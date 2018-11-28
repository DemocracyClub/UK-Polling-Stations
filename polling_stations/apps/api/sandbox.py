import json
import os
import re
from django.http import HttpResponse
from django.views import View

class SandboxView(View):
    def get(self, request, *args, **kwargs):

        base_path = os.path.dirname(__file__)
        get_fixture = lambda filename: open(
            os.path.join(base_path, "sandbox-responses", filename + ".json")
        )

        example_postcodes = (
            "AA12AA",  # station known
            "AA12AB",  # station not known
            "AA13AA",  # address picker
        )

        if "postcode" in kwargs:
            postcode = re.sub("[^A-Z0-9]", "", kwargs["postcode"].upper())
            if postcode in example_postcodes:
                return HttpResponse(
                    get_fixture(postcode), content_type="application/json", status=200
                )
            return HttpResponse(
                json.dumps({"message": "Could not geocode from any source"}),
                content_type="application/json",
                status=400,
            )

        example_slugs = (
            "e07000223-524-2-truleigh-way-shoreham-by-sea-west-sussex-bn436hw",
            "e07000223-527-5-truleigh-way-shoreham-by-sea-west-sussex-bn436hw",
        )
        if "slug" in kwargs:
            if kwargs["slug"] in example_slugs:
                return HttpResponse(
                    get_fixture(kwargs["slug"]),
                    content_type="application/json",
                    status=200,
                )
            return HttpResponse(
                json.dumps({"message": "Address not found"}),
                content_type="application/json",
                status=404,
            )

        return HttpResponse(
            json.dumps({"message": "Internal Server Error"}),
            content_type="application/json",
            status=500,
        )
