from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from .serializers import *

class StoreViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = StoreSerializer
    
    def get_queryset(self):
        return Store.objects.all()
    
    def create(self, request, *args, **kwargs):
        if not isSellerPermission(request):
            return Response({"error": "Vous n'êtes pas vendeur"}, status=403)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class ProductViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all()
    
    def create(self, request, *args, **kwargs):
        if not hasStorePermission(request):
            return Response({'error': "Vous devez être vendeur et posséder une boutique"}, 403)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        try:
            store = Store.objects.get(id=self.request.data['store_id'])
            if store is not None and store.owner == self.request.user:
                serializer.save(store=store)
        except:
            return Response({"error": "La boutique n'existe pas"}, status=404)
    
class ReceiptViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.filter(customer = self.request.user)
    
    def perform_create(self, serializer):
        try:
            products = []
            for order in self.request.data:
                product = Product.objects.get(id=order['product_id'])
                products.append((product, order['quantity']))

            receipt = serializer.save(customer = self.request.user)
            total_price = 0

            for product in products:
                order = Order.objects.create(
                    receipt = receipt,
                    ordered_quantity = product[1],
                    product = product[0],
                    total_price = product[0].price * product[1]
                )

                total_price += order.total_price

            receipt.total_price = total_price

        except Product.DoesNotExist:
            return Response({'error': "Un ou plusieurs produits n'existent pas"}, status=404)
        return super().perform_create(serializer)
    
    def update(self, request, *args, **kwargs):
        return Response({'error': "Vous ne pouvez pas modifier une facture"}, 403)
    
    def destroy(self, request, *args, **kwargs):
        return Response({'error': "Vous ne pouvez pas supprimer une facture"}, 403)