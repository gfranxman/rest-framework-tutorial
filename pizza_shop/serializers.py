from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from .models import Pizza, Topping, ToppingType


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
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

