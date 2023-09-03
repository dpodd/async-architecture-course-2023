from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserDetailView(APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['read']
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
