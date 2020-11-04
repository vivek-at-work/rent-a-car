from customers.models import Customer
from customers.serializers import CustomerSerializer, SignUpSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

CUSTOMER = Customer

class CustomersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Model view set for customer listing and registration
    """
    queryset = CUSTOMER.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        serializer_class=SignUpSerializer,
        permission_classes=[permissions.AllowAny],
        methods=['post'],
    )
    def register(self, request):
        """
        Custom action for customer sign up
        using name, date of birth, contact number and password
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            customer = CUSTOMER.objects.create_user(
                **serializer.validated_data
            )
            return Response(
                CustomerSerializer(customer, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return CUSTOMER.objects.all()
        return self.queryset.filter(contact_number=user.contact_number)
