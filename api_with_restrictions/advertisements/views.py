import django_filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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

        queryset = (Advertisement.objects.filter(creator_id=user_id) |
                    (Advertisement.objects.exclude(status='DRAFT')))

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

    # в методе add_favorite() нужно получить само
    # объявление и сравнить его автора с request.user
    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        advertisement = Advertisement.objects.filter(id=pk).first()
        if advertisement.creator.id == request.user.id:
            raise ValidationError("Not add favorite. User is creator")
        else:
            return Response(Favorite.objects.create(user_id=request.user.id, advertisement_id=pk).id)


    @action(detail=False)
    def favorites(self, request):
        advertisement_favorites = Advertisement.objects.filter(id__in=Favorite.objects.filter(user_id=request.user.id).values_list('advertisement_id')).values()
        return Response(advertisement_favorites)