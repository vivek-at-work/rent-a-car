"""
car_rental_service URL Configuration
"""
from bookings.routers import bookings_router
from catalogue.routers import catalogue_router
from customers.routers import customers_router
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from car_rental_service.default_router import DefaultRouter

router = DefaultRouter()
router.extend(bookings_router)
router.extend(catalogue_router)
router.extend(customers_router)

urlpatterns = [
    path('api/v1/login/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
