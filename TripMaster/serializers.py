from rest_framework import serializers
from django.contrib.auth.models import User
from TripMaster.models import TripDb, TripMemberDb

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDb
        fields = "__all__"
        read_only = ["id", "created_by", "created_at", "updated_at"]
        
        
class TripMemberSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(write_only=True)
    member_username = serializers.CharField(source='user.username', read_only=True)
    member_username_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = TripMemberDb
        fields = ["id", "username", "member_username", "member_username_id", "joined_at"]
        read_only_fields = ["id", "joined_at"]
        
    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
        
        trip = self.context['trip']
        if user == trip.created_by:
            raise serializers.ValidationError("The creator of the trip cannot be added as a member.")
        if TripMemberDb.objects.filter(trip=trip, user=user).exists():
            raise serializers.ValidationError("This user is already a member of the trip.")
        return value
    
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        user = User.objects.get(username=username)
        trip = self.context['trip']
        trip_member = TripMemberDb.objects.create(trip=trip, user=user)
        return trip_member
            
        