from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from ..models import Member, Role
from ..filters import MemberFilter


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_roles_count(request):
    """
    stats api for role wise number of users
    :param request:
    :return:
    """
    member_filter = MemberFilter(request.GET, queryset=Member.objects.all())
    filtered_members = member_filter.qs
    role_counts = Role.objects.filter(members__in=filtered_members).values('name').annotate(member_count=Count('members'))
    response_dict = {item['name']: item['member_count'] for item in role_counts}
    return Response(response_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_users_count(request):
    """
    stats api for organization wise number of members
    :param request:
    :return:
    """
    member_filter = MemberFilter(request.GET, queryset=Member.objects.all())
    filtered_members = member_filter.qs
    org_member_count = Role.objects.filter(members__in=filtered_members).values('organization__name').annotate(member_count=Count('members'))
    response_dict = {item['organization__name']: item['member_count'] for item in org_member_count}
    return Response(response_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_role_users_count(request):
    """
    stats api for organization wise role wise number of users
    :param request:
    :return:
    """
    member_filter = MemberFilter(request.GET, queryset=Member.objects.all())
    filtered_members = member_filter.qs
    org_role_member_count = Role.objects.filter(members__in=filtered_members).values('organization__name', 'name').annotate(member_count=Count('members'))
    org_set = set()
    response_dict = {}
    for item in org_role_member_count:
        org = item['organization__name']
        role = item['name']
        count = item['member_count']
        if org not in org_set:
            org_set.add(org)
            response_dict[org] = {role: count}
        else:
            response_dict[org][role] = count
    return Response(response_dict, status=status.HTTP_200_OK)
