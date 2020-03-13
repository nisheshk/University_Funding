from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password        = serializers.CharField(write_only=True)
    first_name      = serializers.CharField()
    last_name       = serializers.CharField()
    password2       = serializers.CharField(write_only=True)
    type            = serializers.CharField(required=False)
    location        = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password','password2', 'first_name', \
                    'last_name','type', 'location']

    def validate(self, data):
        """
            This method validates the new users credentials during registration.

            Parameters:
            -----------
            data: dic
                It contains the data entered by the user

            Returns
            --------
            data: dic
        """

        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')

        #type is to determine whether the use is MGO,donor or fundraiser
        type = data.get('type')

        #Fundraiser must have domain @uwindsor.ca at the end.
        if ('@uwindsor.ca' not in username) and (type == 'f'):
            raise serializers.ValidationError('Please check the domain @uwindso'
                                                'r.ca is present in the'
                                                'email address')
        if password != password2:
            raise serializers.ValidationError('The passwords do not match')
        return data

    def create(self, validated_data):
        """
            This method saves the new users info after the validation is done

            Parameters:
            -----------
            validated_data: dic
                It contains the same data as above method; but its validated at
                this point.

            Returns
            --------
            user: User type object
        """

        user_type = validated_data['type']
        user = User(username=validated_data['username'],type=validated_data\
                                                                    ['type'])
        user.set_password(validated_data['password'])

        #Saving the user would trigger a signal which then saves the same user
        #to another model DonorProfile, FundRaiserProfile or MGOProfile, based
        #on its type.
        #CHANGES:This should be other way around and needs to be changed later.
        user.save()
        return user
