import django_filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer

from advertisements.permissions import OwnerHasRights, OwnerNotHasRights

from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Advertisement.objects.filter(creator_id=user_id) \
            .union(Advertisement.objects.exclude(status='DRAFT'))
        return queryset
    
    serializer_class = AdvertisementSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), OwnerHasRights()]
        return []

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        if Advertisement.objects.filter(creator=request.user.id, id=pk):
            return Response({'status': 'User is creator'})
        else:
            Favorite.objects.create(user_id=request.user.id, advertisement_id=pk)
            return Response({'status': 'Add favorites'})

    @action(detail=False)
    def favorites(self, request):
        #return Response(list(item['advertisement_id'] for item in Favorite.objects.filter(user_id=request.user.id).values('advertisement_id')))
        return Response(Favorite.objects.filter(user_id=request.user.id).values_list('advertisement_id'))