from django.shortcuts import render

from django.contrib.auth.models import User

from expense_tracker_app.models import Expense
from expense_tracker_app.serializers import Userserializer, ExpenseSerializser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from django.db.models import Sum

class RegisterView(APIView):

    def post(self, request, *args, **kwargs):

        data = request.data

        serializer_inst = Userserializer(data = data)

        if serializer_inst.is_valid():

            serializer_inst.save()

            return Response(data=serializer_inst.data)
        
        else:

            return Response(data=serializer_inst.errors)

class CreateListExpense(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer_inst = ExpenseSerializser(data = request.data)

        if serializer_inst.is_valid():

            serializer_inst.save(owner = request.user)

            return Response(data=serializer_inst.data)
        
        else:

            return Response(data=serializer_inst.errors)
        
    def get(self, request, *args, **kwargs):

        user = request.user

        expenses_obj = Expense.objects.filter(owner = user)

        serialiser_inst = ExpenseSerializser(expenses_obj, many = True)

        return Response(data=serialiser_inst.data)

class ExpenseRetriveupdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        expense_obj = Expense.objects.get(id = id)

        if expense_obj.owner != request.user:

            raise serializers.ValidationError("Owner permission required")
        
        else:

            serialier_inst = ExpenseSerializser(expense_obj)

            return Response(data=serialier_inst.data)
        
    def put(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        expense_obj = Expense.objects.get(id = id)

        serializers_inst = ExpenseSerializser(expense_obj, data=request.data)

        if expense_obj.owner != request.user:

            raise serializers.ValidationError("Owner permission required")
        
        else:

            if serializers_inst.is_valid():

                serializers_inst.save()

                return Response(data=serializers_inst.data)

            else:

                return Response(data=serializers_inst.errors)
            

    def delete(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        expense_obj = Expense.objects.get(id = id)

        if expense_obj.owner != request.user:

            raise serializers.ValidationError("owner permission required")
        
        else:

            expense_obj.delete()

            return Response(data={"message" : "deleted"})
        

class TotalExpenseView(APIView):

    def get(self, request, *args, **kwargs):

        total = Expense.objects.filter(owner=request.user).aggregate(
            total_amount=Sum("amount")
        )

        return Response(total)



            


        

            

