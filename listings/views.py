from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .models import Listing
from django.db.models import Q


def home(request):
    location = request.GET.get('location')
    query = request.GET.get('q')

    listings = Listing.objects.all()

    # Filter by location
    if location:
        listings = listings.filter(location=location)

    # Search by keyword (title + description)
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    listings = listings.order_by('-created_at')

    # Group listings by location
    location_groups = defaultdict(list)
    for listing in listings:
        location_groups[listing.location].append(listing)

    # For dropdown
    all_locations = Listing.objects.values_list(
        'location', flat=True
    ).distinct()

    return render(request, 'home.html', {
        'location_groups': dict(location_groups),
        'all_locations': all_locations,
        'selected_location': location,
        'search_query': query,
    })


# Single listing detail page
def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    images = listing.images.all()

    return render(request, "listing_detail.html", {
        "listing": listing,
        "images": images,
    })
