from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, Role, Member, CustomUser, Invitation
from django.db import transaction
from datetime import datetime
from django.shortcuts import get_object_or_404


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
    name = serializers.CharField(max_length=50, default='owner')
    organization = OrganizationSerializer()

    class Meta:
        model = Role
        fields = ['name', 'organization', 'description']

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
    created_at = serializers.DateTimeField(required=False, default=datetime.now())
    updated_at = serializers.DateTimeField(required=False, default=datetime.now())

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
            user = CustomUser.objects.create(**user_data)
            member = Member.objects.create(
                user=user,
                organization=organization,
                role=role,
                status=status,
                settings=settings
            )
            return member

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.settings = validated_data.get('settings', instance.settings)
        instance.updated_at = datetime.now()
        instance.role = RoleSerializer().create(validated_data=validated_data['role'])
        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registered.")
        return value

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user


class InvitationSerializer(serializers.ModelSerializer):

    role = RoleSerializer()
    class Meta:
        model = Invitation
        fields = ["email", "token", "is_accepted", "created_at", "accepted_at", "role"]
        read_only_fields = ["token", "is_accepted", "expires_at"]

    def create(self, validated_data):
        role = validated_data.get('role')
        print(role['name'], role['organization']['name'])
        validated_data['role'] = get_object_or_404(Role,
                                                   name=role['name'],
                                                   organization__name=role['organization']['name'])
        invitation = super().create(validated_data)
        invitation.send_invite_mail()
        return invitation

