from rest_framework import serializers
from core.models import *



class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        if not attrs.get('password') == attrs.pop('confirm_password'):
            raise serializers.ValidationError(
                'ERROR: Your password and confirmation password do not match.')
        return attrs
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.is_superuser = False
        user.save()

        return user

    class Meta:
        model = User
        fields =('phone','first_name','last_name','email','username','password','confirm_password')

