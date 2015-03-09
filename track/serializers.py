__author__ = 'ZYW'
from track.models import Bug,User
from  rest_framework import serializers

class BugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bug
        fields = ('id','name','content','version','date','finish','distribter')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
