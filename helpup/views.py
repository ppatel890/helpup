import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import stripe
from helpup.forms import CustomUserCreationForm, AddPicture, DonateForm
from helpup.models import Project, Donation


def home(request):
    return render(request, 'base_template.html', {'user': request.user})

# Shows list of users projects and past donations
@login_required()
def profile(request):
    projects = Project.objects.filter(student=request.user)
    donations = Donation.objects.filter(donor=request.user)
    data = {'projects': projects, 'donations': donations}
    return render(request, 'profile.html', data)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


#Creates an instance of a new project in database
@csrf_exempt
def new_project(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        location = data['location']
        lng = data['lng']
        lat = data['lat']
        amount = data['amount']

        new_project = Project.objects.create(
            title=title,
            date_created=datetime.today(),
            description=description,
            location=location,
            student=request.user,
            lat=lat,
            lng=lng,
            amount=amount,
        )

        project_info = {
            'title': new_project.title,
            'descriptions': new_project.description,
            'location': new_project.location,
            'lat': lat,
            'lng': lng,
            'amount': new_project.amount
        }
        return HttpResponse(json.dumps(project_info), content_type='application/json')


def project_map(request, zipcode):
    return render(request, 'maps.html')

#Gets the lat lng and project information of all projects for google maps
@csrf_exempt
def get_location(request):
    projects = Project.objects.all()
    project_list=[]
    for project in projects:
        project_info = {
            'title': project.title,
            'description': project.description,
            'lat': project.lat,
            'lng': project.lng,
            'id': project.id
        }
        project_list.append(project_info)
    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def get_project(request):
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        project_info = {
            'title': project.title,
            'description': project.description,
            'first_name': project.student.first_name,
            'last_name': project.student.last_name,
            'image': str(project.picture),
            'id': project.id

        }
        project_list.append(project_info)

    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    donations = Donation.objects.filter(project=project)
    form = AddPicture(instance=project)
    user = request.user
    data={'project': project, 'form': form, 'donations': donations, 'user': user}

    if request.method == 'POST':
        print "posted"
        form = AddPicture(request.POST, instance=project)
        print form
        if form.is_valid():
            print 'form valid'
            form.save()
            return redirect('home')
    else:
        form=AddPicture()

    return render(request, 'view_project.html', data)


@csrf_exempt
def get_user_project(request):
    user=request.user
    projects = Project.objects.filter(student=user)
    project_list=[]
    for project in projects:
        project_info = {
            'title': project.title,
            'id': project.id
        }
        project_list.append(project_info)
    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')

def form(request):
    form = DonateForm()


    data = {'form': form}
    return render(request, 'form.html', data)



def upload_picture(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        print 'post'
        form = AddPicture(request.POST, request.FILES, instance=project)
        print form
        if form.is_valid():
            print "form valid"
            if form.save():
                print 'formsaved'
                return redirect('/view_project/'+project_id)
    else:
        form=AddPicture(instance=project)
    data = {'project': project, 'form': form}
    return render(request, 'upload_picture.html', data)


# Creates an instance of a donation for project, and updates the amount needed
@csrf_exempt
def make_donation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data['donationAmount']
        print type(amount)
        project_id = data['projectId']
        donor = request.user
        project = Project.objects.get(pk=project_id)
        new_donation = Donation.objects.create(
            donation_amount=amount,
            project=project,
            donor=donor,
            date=datetime.now()
        )
        print project.donate
        print type(new_donation.donation_amount)
        project.donate = project.donate + float(new_donation.donation_amount)
        project.save()
        print project.donate
        donation_info = {
            'amount': new_donation.donation_amount,
            'project': new_donation.project.title,
            'donor': new_donation.donor.first_name
        }

        return HttpResponse(json.dumps(donation_info), content_type='application/json')


@csrf_exempt
def charge(request):
    # donation = Donation.objects.get(pk=donation_id)
    # donation_data = {'donation': donation}
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account
    stripe.api_key = "sk_test_4V8sw4NSu68ALG9fcV4mm9cP"

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Create a Customer
    customer = stripe.Customer.create(
        card=token,
        description="payinguser@example.com"
    )

    # Charge the Customer instead of the card
    stripe.Charge.create(
        amount=1000,  # in cents
        currency="usd",
        customer=customer.id
    )

    return render(request, 'charge.html')




