from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from TripMaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from django.contrib.auth.models import User
from TripMaster.models import TripDb, TripMemberDb
from rest_framework import authentication, permissions, serializers
from TripMaster.permissions import OwnerOnly
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"User created successfully"}, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)
        
        
class TripListCreateView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        qs = TripDb.objects.filter(created_by=request.user)
        serializer_instance = TripSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=200)
    
    # def get(self, request):
    #     qs = TripDb.objects.all()
    #     serializer_instance = TripSerializer(qs, many=True)
    #     return Response(data=serializer_instance.data, status=200)
    
    def post(self, request):
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={"message":"Trip created successfully.", "trip":serializer_instance.data}, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)
        


class TripRetrieveUpadateDelete(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
            
    def get(self, request, pk):
        trip_object = get_object_or_404(TripDb, id=pk)
        # if trip_object.created_by==request.user:
        #     serializer_instance=TripSerializer(trip_object)
        #     return Response(data=serializer_instance.data, status=200)
        # else:
        #     raise serializers.ValidationError("You are not allowed to access this trip")
        
        #custom permisssion
        if trip_object.created_by==request.user:
            serializer_instance=TripSerializer(trip_object)
            return Response(data=serializer_instance.data, status=200)
        
        
    def put(self, request, pk):
        trip_object = get_object_or_404(TripDb, id=pk)
        #1, Trip to munnar,.....2
        
        # if trip_object.created_by != request.user:  # using custom permission method we don't need this condition which we already passed in permissions.py
        #     raise serializers.ValidationError("You are not allowed to update this trip.")
        
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data, instance=trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"massage":"Trip Updated successfully.", "Updated Trip Details":serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)
        
    def delete(self, request, pk):
        trip_object = get_object_or_404(TripDb, id=pk)
        # if trip_object.created_by == request.user:
        #     trip_object.delete()
        #     return Response(data={"Message":"Trip deleted successfully"})
        # else:
        #     raise serializers.ValidationError("You are not allowed to delete this trip.")
        
        # different way
        # if trip_object.created_by != request.user:
            # raise serializers.ValidationError("You are not allowed to delete this trip.")
        # trip_object.delete()
        # return Response(data={"Message":"Trip deleted successfully"})
         
        #custom permission
        trip_object.delete()
        return Response(data={"Message":"Trip deleted successfully"})
    
    
class UserView(APIView):
    def get(self, request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=200)
    
    
    

class TripMemberListCreateView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def get(self, request, trip_id):
        # Step-1
        trip_object = get_object_or_404(TripDb, id=trip_id)
        # Step-2
        is_owner = trip_object.created_by==request.user
        is_member = TripMemberDb.objects.filter(trip=trip_object, user=request.user).exists()
        if not (is_owner or is_member):
            raise serializers.ValidationError("You are not allowed to access this trip.")
        # Get all members of this trip
        members = TripMemberDb.objects.filter(trip=trip_object)
        serializer_instance = TripMemberSerializer(members, many=True)
        return Response(data=serializer_instance.data, status=200)
        
    def post(self, request, trip_id):
        
        trip_object = get_object_or_404(TripDb, id=trip_id)
        # Checks trip ownership
        if trip_object.created_by != request.user:
            raise PermissionDenied("Only the trip owner can add members.")
        form_data = request.data
        serializer_instance = TripMemberSerializer(data=form_data, context={'trip' : trip_object})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"Message":"Trip member added successfully..!"})
        else:
            return Response(data=serializer_instance.errors)
        
        

class TripMemberDeleteView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, trip_id, member_id):
        trip_object = get_object_or_404(TripDb, id=trip_id)
        
        # Checks Trip Ownership
        if trip_object.created_by != request.user:
            raise PermissionDenied("Only the Trip Owner can delete members..!")
        
        member_object = get_object_or_404(TripMemberDb, id=member_id, trip=trip_object)
        member_object.delete()
        return Response(data={"Message":"Trip member deleted successfully !"})
        
    
