__author__ = 'ZYW'
from rest_framework.routers import DefaultRouter
from track import views

router = DefaultRouter()
router.register(r'Bugs',views.BugViewSet)
router.register(r'Users',views.UserViewSet)
