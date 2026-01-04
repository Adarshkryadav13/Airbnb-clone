from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 3

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]


