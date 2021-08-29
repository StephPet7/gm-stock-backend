from rest_framework import viewsets
from .serializer import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CommandsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     command = super(CommandsViewSet, self).retrieve(self, request).data
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=command['command_by'])
    #     serializer = UserSerializer(user)
    #     command['command_by'] = serializer.data
    #     return Response(command)


class CommandRowsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CommandRow.objects.all().order_by('command')
    serializer_class = CommandRowSerializer


class DeliveriesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class DeliveryDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = DeliveryDetails.objects.all()
    serializer_class = DeliverySerializer

