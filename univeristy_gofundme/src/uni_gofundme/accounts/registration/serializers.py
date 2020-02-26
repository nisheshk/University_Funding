from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password        = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    first_name      = serializers.CharField()
    last_name       = serializers.CharField()
    password2       = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    type            = serializers.CharField(required=False)
    location        = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password','password2', 'first_name', 'last_name','type', 'location']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        type = data.get('type')
        print (data)
        if ('@uwindsor.ca' not in username) and (type == 'f'):
            raise serializers.ValidationError('Please check the domain @uwindsor.ca is present in the\
                                                email address')
        if password != password2:
            raise serializers.ValidationError('The passwords do not match')
        return data

    def create(self, validated_data):
        print (validated_data)
        user_type = validated_data['type']
        user = User(username=validated_data['username'],type=validated_data['type'])
        user.set_password(validated_data['password'])
        user.save()
        return user
