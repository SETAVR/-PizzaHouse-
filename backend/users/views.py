from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import ProfileSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


LoginView = TokenObtainPairView
RefreshView = TokenRefreshView
