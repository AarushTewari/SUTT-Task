from django.shortcuts import render,redirect, get_object_or_404
from .models import Patient, Appointment, Staff
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .forms import PatientSearchForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, 'index.html')

def patient_login(request):
    return render(request, 'login.html')

@login_required
def welcome(request):
    user = request.user
    patient = Patient.objects.get(email = user.email)
    return render(request, 'welcome.html', {'user': user, 'patient': patient}) 

@receiver(user_logged_in)
def create_patient(sender, user, request, **kwargs):
    if not Patient.objects.filter(email=user.email).exists():
        # Create a new patient with the user's email
        patient = Patient.objects.create(email=user.email)
        patient.save()



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
        return redirect('profile')

    return render(request, 'changeprofile.html', {'patient': patient})

def profile(request):
    patient = get_object_or_404(Patient)
    return render(request, 'profile.html', {'patient': patient})

def staff_login(request):# i haven't added a staff signup option because staff will be added from admin panel, obviously we dont want rsndom people accessing the site and signing up as staff
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = auth.authenticate(username=u, password=p)
        
        if user is not None:
            auth.login(request, user)
            return redirect(welcomestaff)
        else:
            messages.info(request, 'Credential invalid')
            return redirect('staff_login')
    return render(request,'staff_login.html', {'user': request.user})

def Logout(request):
    logout(request)
    return redirect('index')

def welcomestaff(request):
    return render(request, 'welcomestaff.html')

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
            patients = Patient.objects.all()
            patient_names = [patient.name for patient in patients]
            extracted_results = process.extract(query, patient_names, scorer=fuzz.token_sort_ratio, limit=10)
            matched_names = [result[0] for result in extracted_results if result[1] >= 70]
            results = patients.filter(name__in=matched_names)

    return render(request, 'search_users.html', {'form': form, 'results': results})
