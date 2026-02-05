from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProdukViewSet, basename='products')
router.register(r'categories', views.KategoriViewSet, basename='categories')
router.register(r'statuses', views.StatusViewSet, basename='statuses')

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/', include(router.urls)),
]
