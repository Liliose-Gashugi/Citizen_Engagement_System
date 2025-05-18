from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import ComplaintForm
from .models import Complaint, Agency
from django.core.mail import send_mail
from .forms import ResponseForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django import forms

def home(request):
    return render(request, 'complaints/home.html')


@login_required
def agency_dashboard(request):
    try:
        agency = request.user.agency  # assumes OneToOne user-agency link
        complaints = Complaint.objects.filter(agency=agency)
    except Agency.DoesNotExist:
        complaints = []

    return render(request, 'complaints/agency_dashboard.html', {
        'complaints': complaints
    })


def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            selected_category = form.cleaned_data['category']
            agency = Agency.objects.filter(name=selected_category).first()
            complaint.agency = agency
            complaint.save()

            return redirect('complaint_status', complaint_id=complaint.id)
    else:
        form = ComplaintForm()

    return render(request, 'complaints/submit.html', {'form': form})

def complaint_status(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    return render(request, 'complaints/status.html', {'complaint': complaint})

def respond_to_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.user.agency != complaint.agency:
        return HttpResponseForbidden("You are not authorized to respond to this complaint.")

    # If the complaint is still 'Open', update it to 'In Progress'
    if complaint.status == 'Open':
        complaint.status = 'In Progress'
        complaint.save()

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response_text = form.cleaned_data['response']
            complaint.response = response_text
            complaint.status = 'Resolved'  # Automatically mark as resolved
            complaint.save()

            # Send the email to the citizen
            send_mail(
                subject='Response to Your Complaint',
                message=response_text,
                from_email='gashugilili@gmail.com',
                recipient_list=[complaint.citizen_email],
                fail_silently=False,
            )

            return redirect('complaint_status', complaint_id=complaint.id)
    else:
        form = ResponseForm(initial={'response': complaint.response})

    return render(request, 'complaints/respond.html', {'form': form, 'complaint': complaint})

def home(request):
    return render(request, 'complaints/home.html')

class AgencyLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def agency_login(request):
    if request.method == 'POST':
        form = AgencyLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('agency_dashboard')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = AgencyLoginForm()
    return render(request, 'complaints/agency_login.html', {'form': form})
