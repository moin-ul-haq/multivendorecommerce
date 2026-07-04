from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiRouteListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        resolver = get_resolver()
        all_routes = []
        self.get_routes(resolver.url_patterns, "", all_routes)
        api_routes = []
        for item in all_routes:
            if item.startswith("api/"):
                api_routes.append(item)
        return Response(
            {
                "api_routes": api_routes,
            }
        )

    def get_routes(self, patterns, prefix, all_routes):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                route = prefix + str(pattern.pattern)
                all_routes.append(route)
            elif isinstance(pattern, URLResolver):
                self.get_routes(
                    pattern.url_patterns, prefix + str(pattern.pattern), all_routes
                )
