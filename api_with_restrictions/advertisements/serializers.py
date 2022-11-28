from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # количество открытых объявлений должно валидироваться только
        # при создании или если пользователь хочет открыть уже закрытое объявление
        # TODO: добавьте требуемую валидацию
        auth_user_id = self.context['request'].user.id
        count_advertisement = Advertisement.objects.filter(creator=auth_user_id, status='OPEN').count()

        if self.context['request'].method == 'POST':
            if count_advertisement < 10:
                return data
            else:
                raise ValidationError("Count_advertisements = 10!")
        elif self.context['request'].method == 'PATCH' or self.context['request'].method == 'PUT':
            if count_advertisement < 10 or (count_advertisement == 10 and data['status'] != 'OPEN'):
                return data
            else:
                raise ValidationError("Count_advertisements = 10!")