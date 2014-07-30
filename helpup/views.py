import json
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from helpup.forms import CustomUserCreationForm
from helpup.models import Project


def home(request):
    return render(request, 'base_template.html', {'user': request.user})

def profile(request):
    projects = Project.objects.filter(student=request.user)
    data = {'projects': projects}
    return render(request, 'profile.html', data)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_exempt
def new_project(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        location = data['location']
        lng=data['lng']
        lat=data['lat']
        print title
        print description
        print location
        new_project=Project.objects.create(
            title=title,
            date_created=datetime.today(),
            description=description,
            location=location,
            student=request.user,
            lat=lat,
            lng=lng
        )

        project_info = {
            'title': new_project.title,
            'description': new_project.description,
            'student': new_project.student.first_name
        }

        return HttpResponse(json.dumps(project_info), content_type='application/json')


def project_map(request):
    return render(request, 'maps.html')

@csrf_exempt
def get_location(request):
    projects = Project.objects.all()
    project_list=[]
    for project in projects:
        project_info = {
            'title': project.title,
            'description': project.description,
            'lat': project.lat,
            'lng': project.lng
        }
        project_list.append(project_info)
    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')


