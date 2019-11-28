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
		user.is_active = False
		user.is_superuser = False
		user.save()

		return user

	class Meta:
		model = User
		fields =('email','password','confirm_password','first_name','last_name','phone')

class VerificationSeialiser(serializers.Serializer):
	active_code = serializers.CharField()

	def get(self,request):
		code = request.GET.get('active_code')
		try: 
			user =  User.objects.get(verification_code=code)
		except:
			user = False

		if user:
			user.is_active = True
			user.save()
		
			data = {"status": True, "message": "User is Activate"}
		else:
			data = {"status": False, "message": "Invalide Code"}
		return data
