from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'student_number', 'lecturer_number', 'registrar_number']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'student_number', 'lecturer_number', 'registrar_number']
        extra_kwargs = {
            'student_number': {'required': False},
            'lecturer_number': {'required': False},
            'registrar_number': {'required': False},
        }

    def validate(self, data):
        role = data.get('role')
        
        if role == 'student' and not data.get('student_number'):
            raise serializers.ValidationError({'student_number': 'This field is required for students.'})
        if role == 'lecturer' and not data.get('lecturer_number'):
            raise serializers.ValidationError({'lecturer_number': 'This field is required for lecturers.'})
        if role == 'registrar' and not data.get('registrar_number'):
            raise serializers.ValidationError({'registrar_number': 'This field is required for registrars.'})
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
