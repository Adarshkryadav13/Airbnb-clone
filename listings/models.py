from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Listing(models.Model):
    host = models.ForeignKey(User ,on_delete= models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.IntegerField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="listings/")
    
