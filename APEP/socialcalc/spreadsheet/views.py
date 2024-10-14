from django.shortcuts import render, redirect, get_object_or_404
from .models import Spreadsheet, Cell, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import sessions
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username , password = password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("create_spreadsheet"))
        return render(request, "spreadsheet/login.html", {"message": "Invalid Details"})
    return render(request, "spreadsheet/login.html") 
            
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        password = request.POST["password"]
        confirm = request.POST["confirmation"]
        if confirm != password:
            return render(request, "spreadsheet/register.html", {username : "username" , "message":"Password not matches"})
        
        #Attempt to create a user
        try:
           user = User.objects.create_user(username, email, password)
           user.save()
        except IntegrityError:
            return render(request, "spreadsheet/register.html", {"message":"username already taken"})
        login(request, user)
        return HttpResponseRedirect(reverse("create_spreadsheet"))
    return render(request, "spreadsheet/register.html")   

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("create_spreadsheet"))

def index(request):
    return render(request, "spreadsheet/index.html")

@login_required
def create_spreadsheet(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        spreadsheet = Spreadsheet.objects.create(title=title, owner=request.user)
        return redirect('spreadsheet_detail', spreadsheet_id=spreadsheet.id)
    return render(request, 'spreadsheet/create.html')

@login_required
def spreadsheet_detail(request, spreadsheet_id):
    spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
    cells = Cell.objects.filter(spreadsheet=spreadsheet)
    cell_dict = {}
    for cell in cells:
          cell_dict[(cell.row, cell.column)] = cell.value
    print(cell_dict)
    return render(request, 'spreadsheet/detail.html', {'spreadsheet': spreadsheet, 'cell_dict': cell_dict})

@login_required
def update_cell(request, spreadsheet_id):
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        column = int(request.POST.get('column'))
        value = request.POST.get('value')
        spreadsheet = get_object_or_404(Spreadsheet, id=spreadsheet_id)
        cell, created = Cell.objects.get_or_create(spreadsheet=spreadsheet, row=row, column=column)
        cell.value = value
        cell.save()
        return redirect('spreadsheet_detail', spreadsheet_id=spreadsheet.id)
    

def old(request):
    return render(request, "spreadsheet/old_patient.html") 