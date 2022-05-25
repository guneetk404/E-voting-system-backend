from rest_framework import serializers
from accounts.models import CustomUser as User,TempimageHolder
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    Aadhaar = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'first_name',
                  'last_name', 'Mobile', 'Aadhaar', 'is_voter')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            Mobile=validated_data['Mobile'],
            Aadhaar=validated_data['Aadhaar'],
            is_voter=validated_data['is_voter']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class TempimageHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempimageHolder
        fields = '__all__'