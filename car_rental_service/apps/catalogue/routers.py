from catalogue.views import CarViewSet
from rest_framework.routers import DefaultRouter

catalogue_router = DefaultRouter()
catalogue_router.register(r'cars', CarViewSet)
