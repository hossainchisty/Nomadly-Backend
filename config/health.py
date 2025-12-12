from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Health Check",
        description="Check if the server is running",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(
            {
                "status": "success",
                "code": 200,
                "message": "👍 Don't worry, your server is alive!",
            },
            status=status.HTTP_200_OK,
        )
