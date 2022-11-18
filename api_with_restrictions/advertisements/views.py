import django_filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer

from advertisements.permissions import OwnerHasRights, OwnerNotHasRights

from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(),OwnerHasRights()]
        return []

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        id=Favorite.objects.create(user_id=int(request.user.id), advertisement_id=pk)
        return id.id

# class FavoriteViewSet(ModelViewSet):
#     """ViewSet для избранных объявлений."""
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer
#     throttle_classes = [UserRateThrottle,AnonRateThrottle]
#
#     def get_permissions(self):
#         """Получение прав для действий."""
#         if self.action in ["create", "update", "partial_update", "destroy"]:
#             return [IsAuthenticated(),OwnerNotHasRights]
#         return []

