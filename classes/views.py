from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now
from .models import FitnessClass, Booking


def homepage(request):
    return render(request, 'classes/homepage.html')


def add_class(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        datetime_str = request.POST.get('datetime')  
        instructor = request.POST.get('instructor')
        total_slots = int(request.POST.get('total_slots'))

        from datetime import datetime
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

        add_class = FitnessClass.objects.create(
            name=name,
            datetime=datetime_obj,
            instructor=instructor,
            total_slots=total_slots,
            available_slots=total_slots
        )

        return HttpResponse("Class added successfully!")
    

    return render(request, 'classes/add_class.html')



def class_list(request):
    classes = FitnessClass.objects.filter(datetime__gte=now()).order_by('datetime')
    return render(request, 'classes/class_list.html', {'classes': classes})



def book_class(request):
    classes = FitnessClass.objects.filter(datetime__gte=now()).order_by('datetime')
    
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
            if fitness_class.available_slots <= 0:
                return HttpResponse("No available slots.")

            Booking.objects.create(
                fitness_class=fitness_class,
                client_name=client_name,
                client_email=client_email
            )

            fitness_class.available_slots -= 1
            fitness_class.save()

            return HttpResponse("Booking successful!")

        except FitnessClass.DoesNotExist:
            return HttpResponse("Invalid class selected.")
    
    return render(request, 'classes/book_class.html', {'classes': classes})



def view_bookings(request):
    email = request.GET.get('email')  
    bookings = []

    if email:
        bookings = Booking.objects.filter(client_email=email)

    return render(request, 'classes/view_bookings.html', {'email': email, 'bookings': bookings})




