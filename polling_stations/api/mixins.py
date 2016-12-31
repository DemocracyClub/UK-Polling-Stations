from rest_framework.decorators import list_route
from rest_framework.response import Response


class PollingEntityMixin():

    def output(self, request):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, many=True, read_only=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.geo = False
        return self.output(request)

    @list_route(url_path='geo')
    def geo(self, request, format=None):
        self.geo = True
        return self.output(request)
