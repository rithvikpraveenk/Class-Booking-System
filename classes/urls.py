from django.urls import path
from .import views


urlpatterns = [
    
    path('', views.homepage, name='home'),
    path('add-class', views.add_class, name='add_class'), 
    path('classes', views.class_list, name='class_list'),
    path('book', views.book_class, name='book_class'),
    path('bookings', views.view_bookings, name='view_bookings'),
]