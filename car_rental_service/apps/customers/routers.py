from customers.views import CustomersViewSet
from rest_framework.routers import DefaultRouter

customers_router = DefaultRouter()
customers_router.register(r'customers', CustomersViewSet)
