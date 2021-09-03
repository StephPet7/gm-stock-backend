from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializer import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request):
        product = Product.objects.get(id=request.GET['id'])
        data = dict(request.data)
        keys = data.keys()

        for key in keys:
            if key == 'name':
                product.name = data['name']
            if key == 'description':
                product.description = data['description']
            if key == 'unitPrice':
                product.unitPrice = data['unitPrice']
            if key == 'stockUnit':
                product.stockUnit = data['stockUnit']
            if key == 'stockQuantity':
                product.stockQuantity = data['stockQuantity']
            if key == 'alertThreshold':
                product.alertThreshold = data['alertThreshold']

        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request):
        product = Product.objects.get(id=request.GET['id'])
        if product:
            Product.objects.filter(id=request.GET['id']).delete()
            return Response(data=ProductSerializer(product).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

    def delete(self, request):
        command = Command.objects.get(id=request.GET['id'])
        if command:
            Command.objects.filter(id=request.GET['id']).delete()
            return Response(data=CommandSerializer(command).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommandRowsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CommandRow.objects.all().order_by('command')
    serializer_class = CommandRowSerializer

    def put(self, request):
        commandRow = CommandRow.objects.get(id=request.GET['id'])
        data = dict(request.data)
        keys = data.keys()

        for key in keys:
            if key == 'quantityOrdered':
                commandRow.quantityOrdered = data['quantityOrdered']
            if key == 'remaining':
                commandRow.remaining = data['remaining']

        commandRow.save()
        serializer = CommandRowSerializer(commandRow)
        return Response(serializer.data)


class DeliveriesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class DeliveryDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = DeliveryDetails.objects.all()
    serializer_class = DeliverySerializer


# Statics

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getCommandRowByCommandId(request):
    commands = CommandRow.objects.filter(command=request.GET['command_id'])
    return Response(data=CommandRowSerializer(commands, many=True).data, )


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getDeliveryDetailsByDeliveryId(request):
    deliveryDetails = DeliveryDetails.objects.filter(
        delivery=request.GET['delivery_id'])
    return Response(data=DeliveryDetailsSerializer(deliveryDetails, many=True).data, )


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def getProductQuantityById(request):
    product = Product.objects.get(id=request.GET['product_id'])
    response = {"stockQuantity": product.stockQuantity}
    return Response(data=response)
