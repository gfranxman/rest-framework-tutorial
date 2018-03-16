from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


# the dream, but you probably dont want the gis libraries this brings along
from .serializers import PizzaSerializer, ToppingSerializer
# from wq.db import rest
# rest.router.register_model(Pizza,serializer=PizzaSerializer)
# rest.router.register_model(Topping, serializer=ToppingSerializer)

# Create a router and register our viewsets with it.
from .views import PizzaList, ToppingList, ToppingTypeList, ToppingTypeDetail, \
    PizzaDetail, ToppingDetail

router = DefaultRouter()
router.register(r'pizzas', PizzaDetail)
router.register(r'toppings', ToppingDetail)
router.register(r'toppingtypes', ToppingTypeDetail)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
