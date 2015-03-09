from track.models import *
from rest_framework import viewsets
from track.serializers import BugSerializer,UserSerializer

class BugViewSet(viewsets.ModelViewSet):
     """
     bug API
     """
     queryset = Bug.objects.all()
     serializer_class = BugSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    user API
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
