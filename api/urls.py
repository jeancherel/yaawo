from django.urls import path, include
from . import views
from authentication import views as auth_views
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register('users', auth_views.UserViewSet, basename='users')
router.register('products', views.ProductViewSet, basename='products')
router.register('stores', views.StoreViewSet, basename='stores')
router.register('receipts', views.ReceiptViewSet, basename='receipts')

urlpatterns = [
    path('', include(router.urls))
]