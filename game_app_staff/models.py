from django.db import models
from game_app_user.models import CustomUser

class Staff(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='staff_profile')
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15,blank=True,null=True)
    is_staff_member=models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
    

    

class Game(models.Model):
    CATEGORY_CHOICES = [('Free', 'Free'), ('Premium', 'Premium')]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='game_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    file = models.URLField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
