from rest_framework import routers
from .views import ActivityViewSet, ParticipantViewSet, TemaViewSet, CompanionViewSet

router = routers.DefaultRouter()
router.register('temas', TemaViewSet)
router.register('activities', ActivityViewSet)
router.register('participants', ParticipantViewSet)
router.register('companions', CompanionViewSet)

urlpatterns = router.urls