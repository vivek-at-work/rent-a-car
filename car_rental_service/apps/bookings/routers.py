from rest_framework.routers import DefaultRouter

from .views import BookingsViewSet

bookings_router = DefaultRouter()
bookings_router.register(r'bookings', BookingsViewSet)
