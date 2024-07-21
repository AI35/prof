from django.contrib.auth.models import User
from rest_framework import serializers
# from prof.models import Profile



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_login']

""" class ProfileSerializer(serializers.ModelSerializer):
    task_extendeds = UserSerializer(many=True)
    
    class Meta:
        model = Profile
        fields = ['Last_login'] """