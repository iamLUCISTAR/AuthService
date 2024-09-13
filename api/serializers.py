from .models import Organization, Role, Member
from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, Role, Member, CustomUser
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'status', 'personal', 'settings', 'created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Role
        fields = ['name', 'description', 'organization']

    def create(self, validated_data):
        # Extract organization data
        organization_data = validated_data.pop('organization')
        organization, created = Organization.objects.get_or_create(**organization_data)
        # Create the role with the retrieved or created organization
        role, created = Role.objects.get_or_create(organization=organization, **validated_data)
        return role


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'profile', 'status', 'settings', 'created_at', 'updated_at', 'password']

    def validate(self, data):
        if not (data['email'] and data['password']):
            raise serializers.ValidationError("Both email and password needed")
        return data


class MemberSerializer(serializers.Serializer):
    user = CustomUserSerializer()
    organization = OrganizationSerializer()
    role = RoleSerializer()
    status = serializers.IntegerField(required=False, default=0)
    settings = serializers.JSONField(required=False, default=dict)

    class Meta:
        model = Member
        fields = ['user', 'organization', 'role', 'status', 'settings', 'created_at', 'updated_at']

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            organization_data = validated_data.pop('organization')
            role_data = validated_data.pop('role')
            status = validated_data.pop('status', 0)
            settings = validated_data.pop('settings', dict)
            organization, created = Organization.objects.get_or_create(**organization_data)
            role = RoleSerializer().create(validated_data=role_data)
            user = CustomUser.objects.create_user(**user_data)
            member = Member.objects.create(
                user=user,
                organization=organization,
                role=role,
                status=status,
                settings=settings
            )
            return member
