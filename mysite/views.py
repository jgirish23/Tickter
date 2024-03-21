from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as django_logout
from . forms import TicketForm
from . models import Ticket
from django.contrib.auth.models import User
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

home_page = "/home/"

def signup(request):
    if request.method=="POST":
        try:
            email=request.POST["Email"]
            password=request.POST["Password"]
            user_id=User.objects.get(email=email)
            username=user_id.username
            print(email)
            user = authenticate(request,username=username,email=email,password=password)
            print(username)
            if user is not None:
                login(request, user)
                return redirect(home_page)
                # return render(request,"chatbot.html",{"Email":email, "Password":password,"username":username})
            else:
                print("User does not exist!")
                return render(request,"login.html",{"Error":"User does not exist!"})
        except:
            print("wrong creditionals")
            return render(request,"login.html",{"Error":"Invalid input try again!"})

    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        try:
            print("register")
            print(request.POST)
            email=request.POST["Email"]
            username=request.POST["username"]
            password_1=request.POST["password1"]
            password_2=request.POST["password2"]
            if( password_1==password_2 ):
                if not (User.objects.filter(username=username).exists() | User.objects.filter(email=email).exists()):
                    User.objects.create_user(username,email, password_1)
                    user = authenticate(username=username,email=email, password = password_1)
                    login(request, user)
                    return redirect(home_page)
                else:
                    return render(request,"register.html",{"Error":"Enter different username and password!"})
            else:
                return render(request,"register.html",{"Error":"Enter same password!"})

        except:
            return render(request,"register.html",{"Error":"Invalid input try again!"})

    return render(request,"register.html")

def logout(request):
    try:
        django_logout(request)
        print("Successful Logout")
    except:
        pass
    return redirect("/login")

def profile(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            # print(body["password1"])
            password1=body["password1"]
            password2=body["password2"]
            if password1==password2 :
                user = User.objects.get(username__exact=request.user)
                user.set_password(password1)
                user.save()
                user = authenticate(username=request.user,password = password1)
                login(request, user)
                print("Password Changed")
        except:
            pass
    return render(request,"profile.html")



def home(request):
    if request.user.is_authenticated:

        # Retrieve all tickets with the given email_id
        email_id = request.user.email
        tickets = Ticket.objects.filter(Email = email_id)
    return render(request,"my-tickets.html",{'tickets': tickets})



def handle_uploaded_file(f):
    file_name = f.name
    name = file_name.split(".")
    with open(f"uploaded_file/{name[0]}.{name[1]}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def all_tickets(request):
    # Retrieve all tickets with the given email_id
    all_tickets = Ticket.objects.all()
    return render(request,"all-tickets.html",{'tickets': all_tickets})

def create_ticket(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():

                if(request.FILES):
                    handle_uploaded_file(request.FILES["file"])
                form.save()
                return redirect(home_page)  # Redirect to a success page or any other page you want
        else:
            # If it's a GET request, initialize the form
            user_email = request.user.email

            initial_data = {
                'Email': user_email  # Add your custom data here
            }
            form = TicketForm(initial=initial_data)
        return render(request, 'create_ticket.html', {'form': form})
    return redirect("/login")
