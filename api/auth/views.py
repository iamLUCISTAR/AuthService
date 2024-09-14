from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in

from ..serializers import CustomUserLoginSerializer, MemberSerializer, PasswordUpdateSerializer
from ..models import Member, Role, Organization, Invitation

User = get_user_model()


class SignUpView(APIView):
    """
    API for signing up a new user with organization and role details and by default assign the owner role unless a role
    is specified.
    """
    def post(self, request):
        member_serializer = MemberSerializer(data=request.data)
        if member_serializer.is_valid():
            member_serializer.save()
            return Response(member_serializer.data, status=status.HTTP_201_CREATED)
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """
    API for login and send login alert once logged in.
    """
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request,
                                email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            print(user)
            if user:
                refresh = RefreshToken.for_user(user)
                user_logged_in.send(sender=self.__class__, request=request, user=user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdateView(APIView):
    """
    API to reset password and send email alert for password change.
    """
    def post(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f'Password has been updated and confirmation email sent to {serializer.data["email"]}'}
                            , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)