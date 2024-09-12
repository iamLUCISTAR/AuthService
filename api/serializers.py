from .models import Organisation, User, Role, Member
from rest_framework import serializers


class OrganisationSerializer(serializers.ModelSerializer):
    pass

class RoleSerializer(serializers.ModelSerializer):
    pass

class Member(serializers.ModelSerializer):
    pass
