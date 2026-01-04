from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:id>/', views.book_room, name='book_room'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('pay/<int:listing_id>/', views.create_payment, name="create_payment"),
    path("verify/",views.verify_payment, name="verify_payment")
]
