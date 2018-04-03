from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from .models import Pizza, Topping, ToppingType#, PizzaPizzaTopping


class ValidateManyToManyFieldsMixin:
    """ checks all validators on any ManyToManyFields for Models
        this makes 'create' calls work just like updates, allowing the
        ValidatedModel to appliy any validators on save during updates
    """
    def create(self, validated_data):
        with transaction.atomic():
            original_data = validated_data.copy()
            instance = super(ValidateManyToManyFieldsMixin, self).create(validated_data)
            # ^^ instance created without m2m's which are then added
            #    then after they are added, we can call update with the original
            # vv to re-validate
            instance = super(ValidateManyToManyFieldsMixin, self).update(instance, original_data)
        return instance

class PizzaSerializer(ValidateManyToManyFieldsMixin, serializers.HyperlinkedModelSerializer):
    toppings = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='topping-detail',
        queryset=Topping.objects.all())

    class Meta:
        model = Pizza
        fields = '__all__'
        url = HyperlinkedIdentityField(view_name='pizza-detail',
                                       lookup_field='id')


class ToppingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topping
        fields = '__all__'
        url = HyperlinkedIdentityField(view_name='topping-detail',
                                       lookup_field='id')

class ToppingTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToppingType
        fields = '__all__'
        url = HyperlinkedIdentityField(view_name='toppingtype-detail',
                                       lookup_field='id')

