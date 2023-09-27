from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class GroupSerializer(serializers.ModelSerializer):
    name = serializers.RegexField(
        regex=r'^[A-Za-z]*$',
        error_messages={
            'invalid': 'Ce champ ne peut pas contenir que de A à Z.'
        }
     )
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'first_name', 'last_name', 'groups')
        extra_kwargs={'password': {'write_only':True}}
        user= User()
        user.set_password('password')

#serializer list user
class UserListSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id','password', 'email', 'first_name', 'last_name', 'groups','username')
        extra_kwargs={'password': {'write_only':True}}

  
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    hierarchie=serializers.IntegerField(max_value=201)


class EmailSerializer(serializers.Serializer):
    """
    Reset Password Email Request Serializer.
    """
    email = serializers.EmailField()
    class Meta:
        fields = ("email")

class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )
    class Meta:
        field = ("password", "password2")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        else:
            token = self.context.get("kwargs").get("token")
            encoded_pk = self.context.get("kwargs").get("encoded_pk")

            if token is None or encoded_pk is None:
                raise serializers.ValidationError("Missing data.")

            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset token is invalid")

            user.set_password(password)
            user.save()
            return data
