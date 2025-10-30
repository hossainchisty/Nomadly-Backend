from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "status": "success",
                "code": 200,
                "message": "👍 Don't worry, your server is alive!",
            },
            status=status.HTTP_200_OK,
        )
