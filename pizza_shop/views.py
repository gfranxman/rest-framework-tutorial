from rest_framework import viewsets, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Pizza, Topping, ToppingType
from .serializers import PizzaSerializer, ToppingSerializer, \
    ToppingTypeSerializer


# class PizzaList(generics.ListCreateAPIView):
class PizzaList(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permissions_classes = ()


class PizzaDetail(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permissions_classes = ()


# class TopppingList(generics.ListCreateAPIView):
class ToppingList(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = ()

class ToppingDetail(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = ()

class ToppingTypeList(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ToppingType.objects.all()
    serializer_class = ToppingTypeSerializer
    permission_classes = ()



class ToppingTypeDetail(viewsets.ModelViewSet):
    queryset = ToppingType.objects.all()
    serializer_class = ToppingTypeSerializer
    permission_classes = ()




