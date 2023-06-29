from django.shortcuts import render,redirect, get_object_or_404
from .models import Patient, Appointment, Room, message, Staff
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .forms import PatientSearchForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .tables import PatientTable
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django_tables2 import RequestConfig
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'index.html')

def patient_login(request):
    return render(request, 'login.html')

@login_required
def welcome(request):
    user = request.user
    try:
        patient = Patient.objects.get(email=user.email)
        rooms = Room.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        patient = Patient.objects.create(email=user.email)
        rooms = []
    
    return render(request, 'welcome.html', {'user': user, 'patient': patient, 'rooms': rooms})
    
@login_required
def changeprofile(request):
    user = request.user
    patient = Patient.objects.get(email=user.email)

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        address = request.POST['address']

        patient.name = name
        patient.gender = gender
        patient.age = age
        patient.address = address

        patient.save()
        return redirect('/welcome')

    return render(request, 'changeprofile.html', {'patient': patient})

def profile(request, id):
    try:
        patient = Patient.objects.get(id=id)
        return render(request, 'profile.html', {'patient': patient})
    except Patient.DoesNotExist:
        return HttpResponse('Such profile doesnot exist')
    
@login_required
def welcomestaff(request):
    return render(request, 'welcomestaff.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('hospital:welcomestaff')
    if request.method == 'POST':
        if request.POST['secret'] == 'secret':
           username = request.POST['username']
           email = request.POST['email']
           password = request.POST['password']
           password2 = request.POST['password2'] 

           if password == password2:
               if User.objects.filter(email=email).exists():
                   messages.info(request, 'Email taken')
                   return redirect('hospital:register')
               elif User.objects.filter(username=username).exists():
                   messages.info(request, 'Username taken')
                   return redirect('hospital:register')
               else:
                   user = User.objects.create_user(username=username, email=email, password=password)
                   user.save()
                   staff = Staff.objects.create(username=username, email=email)
                   staff.save()
                   user = authenticate(request, username=username, password=password)
                   login(request, user)
                   return redirect('/staffwelcome')
           else:
               messages.info(request, 'Passwords donot match')
               return redirect('hospital:register')
        else:
            messages.info(request, 'Incorrect secret')
            return redirect('hospital:register')
    else:
        return render(request, 'register.html')

def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/staffwelcome')
        else:
            error_message = 'Invalid email or password'
            return render(request, 'staff_login.html', {'error_message': error_message})
    return render(request, 'staff_login.html')

def Logout(request):
    logout(request)
    return redirect('/')

@login_required
def add_appointment(request):
    error=""
    if request.method=='POST':
        p = request.POST['patient']
        d = request.POST['doctor']
        date = request.POST['date']
        time = request.POST['time']
        complain = request.POST['complain']
        patient = Patient.objects.filter(name=p).first()
        if patient is None:
            error='Patient does not exsist'
        try:
            Appointment.objects.create(patient=patient, doctor=d, date1=date, time1 = time, complain=complain)
            error='No'
            return redirect('profile')
        except:
            error='yes'
    return render(request, 'add_appointment.html', {'error' :error})
        

def view_appointment(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments})

def search_patients(request):
    form = PatientSearchForm()
    results = []

    if request.method == 'GET':
        form = PatientSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            patients = Patient.objects.filter(Q(name__icontains=query))
            results = patients[:10]

    return render(request, 'search_users.html', {'form': form, 'results': results})

def see_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
        return render(request, 'see_appointment.html', {'appointment': appointment})
    except Appointment.DoesNotExist:
        return HttpResponse('Such appointment does not exist')
    
def change_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        cost = request.POST.get('cost')
        billing_status = request.POST.get('billing_status')
        prescription = request.POST['prescription']

        appointment.status = status
        appointment.cost = cost
        appointment.billing_status = billing_status
        appointment.prescription = prescription

        appointment.save()
        return redirect('/view_appointment')

    return render(request, 'change_appointment.html', {'appointment': appointment})


    
    
def patient_appointments(request):
    patient = Patient.objects.get(email=request.user.email)
    appointments = Appointment.objects.filter(patient=patient.id)
    return render(request, 'patient_appointment.html', {'appointments': appointments})

@login_required    
def chatrooms(request):
    rooms = Room.objects.all()
    patients = Patient.objects.all()
    return render(request, 'chatrooms.html', {'rooms': rooms, 'patients':patients})

@login_required
def createroom(request):
    room = request.POST['room_name']
    patientname = request.POST['patient_name']

    if Room.objects.filter(patient=patientname, name=room).exists():
        return redirect("chatrooms/"+patientname)
    else:
        new_room = Room.objects.create(name=room, patient=patientname)
        new_room.save()
        return redirect('hospital:chatrooms')

@login_required   
def room(request, patient):
    try:
        user = request.user
        room = Room.objects.get(patient=patient)
        return render(request, 'room.html', {'room': room, 'user':user})
    except Room.DoesNotExist:
        return HttpResponse('No such room exists')
    
def send(request):
    msg = request.POST['message']
    username = request.user
    room_id = request.POST['room_id']
    new_message = message.objects.create(value=msg, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, patient):
    room_details = Room.objects.get(patient=patient)
    messages = message.objects.filter(room=room_details)

    return JsonResponse({"messages":list(messages.values())})

@login_required
def staff_dashboard(request):
    patients = Patient.objects.all()
    table = PatientTable(patients)
    
    # Pagination
    paginator = Paginator(table.rows, 1)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    RequestConfig(request, paginate={'per_page': 1}).configure(table)
    
    return render(request, 'staff_dashboard.html', {'table': table, 'page_obj': page_obj})



