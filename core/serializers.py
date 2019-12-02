from rest_framework import serializers
from core import models as core_model



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
		model = core_model.User
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

class OTPSerializer(serializers.ModelSerializer):

	class Meta:
		model = core_model.User
		fields = ('phone',)

class OTPVerifySeialiser(serializers.Serializer):
	otp_code = serializers.CharField()

	def get(self,request):
		code = request.GET.get('otp_code')
		try: 
			user =  OTPVerification.objects.get(code=code)
		except:
			user = False

		if user:
			# user.is_active = True
		
			data = {"status": True, "message": "Code Verified"}
		else:
			data = {"status": False, "message": "Invalide Code"}
		return data

class SendRequestSerializer(serializers.Serializer):
	receiver_id = serializers.CharField()
	channel_name = serializers.CharField()

	def send(self,request):
		request_user = request.data.get("receiver_id")
		event = request.data.get("channel_name")
		sender = request.user
		receiver = core_model.User.objects.filter(pk=request_user).first()

		if receiver:
			friend_obj = core_model.Friend(from_user=sender,to_user=receiver)
			friend_obj.save()
			data ={"status":True,"message":"Friend Request Sent Successfully ! "}
		else:
			data = {"status":False,"message":"User Not Found !"}
		return data
class AcceptRequestSerializer(serializers.Serializer):
	sender_id = serializers.CharField()
	channel_name = serializers.CharField()

	def accept(self,request):
		sender_user = request.data.get("sender_id")
		event =request.data.get("channel_name")
		receiver = request.user
		sender = core_model.User.objects.filter(pk=sender_user).first()

		try:
			friend_obj = core_model.Friend.objects.get(
				status="requested",from_user=sender,to_user=receiver)
		except core_model.Friend.DoesNotExist:
			friend_obj = None

		if friend_obj:
			friend_obj.status='accepted'
			friend_obj.save()
			personal_chat, created = core_model.PersonalChat.objects.get_or_create(
                chat_id=chat_id
            )
			
			data = {"status":True,"message":"Request Accepted !"}
		else:
			data = {"status":False,"message":"Request Not Found !"}