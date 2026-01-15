from rest_framework import routers
from .views import ActivityViewSet, ParticipantViewSet

router = routers.DefaultRouter()
router.register('activities', ActivityViewSet)
router.register('participants', ParticipantViewSet)

urlpatterns = router.urls