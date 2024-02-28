from django.contrib import admin
from .models import Profile, Story, Comment

# Registers the database tables on the admin page so they can be viewed and
# edited when logged in as an admin. 
admin.site.register(Profile)
admin.site.register(Story)
admin.site.register(Comment)
# Register your models here.
