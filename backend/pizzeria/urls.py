from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    PizzaViewSet,
    create_order,
    my_favorites,
    my_orders,
    order_detail,
    pay_order,
    toggle_favorite,
)


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("pizzas", PizzaViewSet, basename="pizza")

urlpatterns = [
    path("", include(router.urls)),
    path("favorites/my/", my_favorites, name="my_favorites"),
    path("favorites/toggle/", toggle_favorite, name="toggle_favorite"),
    path("orders/my/", my_orders, name="my_orders"),
    path("orders/", create_order, name="create_order"),
    path("orders/<int:pk>/", order_detail, name="order_detail"),
    path("orders/<int:pk>/pay/", pay_order, name="pay_order"),
]
