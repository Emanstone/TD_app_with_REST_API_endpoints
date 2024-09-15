from rest_framework import serializers
from todoapp.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault()) #If user had been added in the fields below

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important']




class TodoCompleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important']