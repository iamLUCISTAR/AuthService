from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from .serializers import MemberSerializer, InvitationSerializer
from .models import Member, Role, Organization, Invitation


User = get_user_model()


class MemberView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API for updating and deleting members.
    """
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
    """
    API to invite a user to a organization.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invited_by=request.user)
            return Response({"msg": "Invitation sent to the user"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptInviteView(APIView):
    """
    API to accept the invite from the admin and join as a member of an organization.
    """
    permission_classes = [IsAuthenticated]

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
