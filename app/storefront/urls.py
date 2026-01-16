from rest_framework import routers
from .views import ActivityViewSet, ParticipantViewSet, TemaViewSet

router = routers.DefaultRouter()
router.register('temas', TemaViewSet)
router.register('activities', ActivityViewSet)
router.register('participants', ParticipantViewSet)

urlpatterns = router.urls