from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.utils import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserLoginSerializer, MemberSerializer, PasswordUpdateSerializer, InvitationSerializer
from .models import Member, Role, Organization, Invitation


User = get_user_model()


class SignUpView(APIView):
    def post(self, request):
        member_serializer = MemberSerializer(data=request.data)
        if member_serializer.is_valid():
            member_serializer.save()
            return Response(member_serializer.data, status=status.HTTP_201_CREATED)
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request,
                                email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                # user_logged_in.send(sender=self.__class__, request=request, user=user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdateView(APIView):
    def post(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f'Password has been updated and confirmation email sent to {serializer.data["email"]}'}
                            , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberView(APIView):
    def put(self, request):
        data = request.data
        user = get_object_or_404(User, email=request.data.get('email'))
        organization = get_object_or_404(Organization, name=data['role']['organization']['name'])
        member = get_object_or_404(Member, user=user, organization=organization)
        member_serializer = MemberSerializer(member, data=data, partial=True)
        if member_serializer.is_valid():
            try:
                role = Role.objects.get(name=data['role']['name'], organization=organization)
                member_serializer.save()
                return Response(member_serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"msg": "Mentioned role is not present in the requested organization"})
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        member = get_object_or_404(Member, user=user)
        member.delete()
        return Response({"msg": "Member deleted successfully!!"}, status=status.HTTP_204_NO_CONTENT)


class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invited_by=request.user)
            return Response({"msg": "Invitation sent to the user"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptInviteView(APIView):
    def post(self, request, token):
        try:
            invitation = Invitation.objects.get(token=token, is_accepted=False)
        except ObjectDoesNotExist:
            return Response({"err": "Invitation invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        if not invitation.is_expired():
            try:
                user = User.objects.get(email=invitation.email)
                role = invitation.role
                organization = role.organization
                member = Member.objects.create(user=user, role=role, organization=organization)
                invitation.accept()
                return Response({"msg":"Member created Successfully"}, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response({"err": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({"err": "User already has role in this org."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Invitation expired"}, status=status.HTTP_410_GONE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_roles_count(request):
    role_member_count = Member.objects.values('role__name').annotate(member_count=Count('id'))
    response_dict = {item['role__name']: item['member_count'] for item in role_member_count}
    return Response(response_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_users_count(request):
    org_member_count = Member.objects.values('organization__name').annotate(member_count=Count('id'))
    response_dict = {item['organization__name']: item['member_count'] for item in org_member_count}
    return Response(response_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_role_users_count(request):
    org_role_member_count = Member.objects.values('organization__name','role__name').annotate(member_count=Count('id'))
    org_set = set()
    response_dict = {}
    for item in org_role_member_count:
        org = item['organization__name']
        role = item['role__name']
        count = item['member_count']
        if org not in org_set:
            org_set.add(org)
            response_dict[org] = {role: count}
        else:
            response_dict[org][role] = count
    return Response(response_dict, status=status.HTTP_200_OK)
