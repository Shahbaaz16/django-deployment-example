from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)#this one to one relationship is defined in the views with the line of code profile.user
    #adding more fields as the user have first & last name, email and Password as default fields
    portfolio_site = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
