from rest_framework import serializers
from django.contrib.auth.models import User

from expense_tracker_app.models import Expense

class Userserializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ['id','username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ExpenseSerializser(serializers.ModelSerializer):

    class Meta:

        model = Expense

        fields = '__all__'

        read_only_fields = ['id', 'owner']