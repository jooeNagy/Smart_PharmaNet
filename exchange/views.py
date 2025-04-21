from django.shortcuts import render
from .models import ExchangeMedciene
from medicine.models import *
from medicine.serializers import MedicineSerializer

from .serializers import ExchangeMedcieneSerializer
# from  ExchangeMedcieneSerializer
from rest_framework import generics, status
from django.shortcuts import get_object_or_404  # ✅ Import added
from rest_framework.response import Response


# class SellMedicineView(generics.CreateAPIView):
#     serializer_class = ExchangeMedcieneSerializer

#     def post(self, request, pk, *args, **kwargs):
        
#         medicine = get_object_or_404(Medicine, pk=pk)
#         quantity = request.data.get("quantity")

#         if not quantity or int(quantity) <= 0:
#             return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

#         if medicine.quantity < int(quantity):
#             return Response({"error": "Not enough stock available"}, status=status.HTTP_400_BAD_REQUEST)

#         # Reduce medicine stock
#         medicine.quantity -= int(quantity)
#         medicine.save()

#         # Create ExchangeMedciene record
#         exchange = ExchangeMedciene.objects.create(
#             operation="Sell",
#             medicine=medicine,
#             quantity=int(quantity)
#         )

#         return Response(ExchangeMedcieneSerializer(exchange).data, status=status.HTTP_201_CREATED)




# testing another idea
class MedicineRetrieveUpdateDestroyView(generics.UpdateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer



# def add_to_sell(request, pk):
#     medicine = get_object_or_404(Medicine, pk=pk)
#     if medicine.can_be_sell == 'False':
#         medicine.can_be_sell = 'True'
#         medicine.save()
        
#     if ExchangeMedciene.objects.filter(medicine=medicine).exists():
#         return Response(status=status.HTTP_302_FOUND)
#     else:
#         ExchangeMedciene.objects.create(medicine=medicine)
#         ExchangeMedciene.save()
    
#     return Response(status=status.HTTP_201_CREATED)


class ExchangeMedicineView(generics.ListAPIView):
    queryset = ExchangeMedciene.objects.all()
    serializer_class = ExchangeMedcieneSerializer
