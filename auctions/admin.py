from django.contrib import admin
from .models import User, Categories, Listings, Comments, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bid)