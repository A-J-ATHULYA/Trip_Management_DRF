from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TripDb(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    destination = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class TripMemberDb(models.Model):
    trip = models.ForeignKey(TripDb, on_delete=models.CASCADE, related_name='trip_member')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_trips')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    # This means the combination of trips and user must be unique.
    # It does not mean that trip alone or user alone must be unique.
    # A user can join multiple trips, and a trip can have multiple users, but the same user cannot join the same trip more than once
    
    def __str__(self):
        return f"{self.user.username} - {self.trip.title}"

    
    # manju - family trip to Ootty 
    # anagha - office trip to munnar
