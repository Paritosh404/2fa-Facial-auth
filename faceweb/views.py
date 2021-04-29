from django.shortcuts import render
import os
from face_auth.settings import MEDIA_ROOT
# Create your views here.
from utility.face_detect import face_encode, check_face_encode, compair
from utility.blink import blink_check
from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User , auth
from django.contrib import messages

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:    
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                context = { 
                    'username' : username,
                }
                return render(request, '2outh.html', context=context)
                auth.login(request,user)
                return redirect('index')
            else:
                messages.info(request,'invalid credentials')
                return redirect('login')

        else:
            return render(request,'login.html')

def outh(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        try:
            abc = request.FILES['video']
        except:
            messages.info(request,'Video File Required')
            return redirect('login')
        username = request.POST['username']
        password = request.POST['password']
        fc = Face_registration.objects.get(username=username)
        fc.vid = abc
        fc.save()
        blinks = blink_check(str(fc.vid).split('.')[0])
        if blinks > 6:
            path1 = str(fc.encodings)
            path2 = check_face_encode(str(fc.vid).split('.')[0])
            try:
                cmp = compair(path1, path2)
            except:
                os.remove(MEDIA_ROOT + str(fc.vid))
                os.remove(MEDIA_ROOT + path2)
                messages.info(request,'Face Auth Failed')
                return redirect('login')
            if cmp:
                user = auth.authenticate(username=username,password=password)
                if user is not None:
                    os.remove(MEDIA_ROOT + str(fc.vid))
                    os.remove(MEDIA_ROOT + path2)
                    auth.login(request,user)
                    return redirect('index')
                else:
                    os.remove(MEDIA_ROOT + str(fc.vid))
                    os.remove(MEDIA_ROOT + path2)
                    messages.info(request,'invalid credentials')
                    return redirect('login')
            else:
                os.remove(MEDIA_ROOT + str(fc.vid))
                os.remove(MEDIA_ROOT + path2)
                messages.info(request,'Face Auth Failed')
                return redirect('login')
        else:
            os.remove(MEDIA_ROOT + str(fc.vid))
            messages.info(request,'Face Auth Failed')
            return redirect('login')

def store(request):
    if request.user.is_authenticated:
        try:
            text = request.POST['text']
            username = request.POST['username']
        except:
            return redirect('index')
        user = Face_registration.objects.get(username=username)
        user.data = text
        user.save()
        print(user.data)
        context = { 
        'username' : username,
        'data': user.data}
        return render(request, 'index.html', context=context)
    else:
        return render(request,'login.html')

def adm(request):
    return HttpResponseRedirect("http://127.0.0.1:8000/admin/login/")

def face(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        try:
            username = request.POST['username']
            email = request.POST['email']
        except:
            return redirect('register')
        try:
            abc = request.FILES['video']
        except:
            user = User.objects.get(email=email)
            fc_user = Face_registration.objects.get(email=email)
            user.delete()
            fc_user.delete()
            
            messages.info(request,'Video File Required')
            return redirect('register')

        
        fc = Face_registration.objects.get(email=email)
        fc.vid = abc
        fc.save()
        enc = face_encode(str(fc.vid).split('.')[0])
        fc.encodings = enc
        fc.face_reg = True
        fc.save()
        if fc.encodings == enc:
            os.remove(MEDIA_ROOT + str(fc.vid))
            return redirect(login)
        else:
            user = User.objects.get(email=email)
            fc_user = Face_registration.objects.get(email=email)
            user.delete()
            fc_user.delete()
            messages.info(request,'Something Went Wrong, Please Try Again')
            return redirect('register')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        
        if request.method == 'POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    print('Username Taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email taken')
                    print('Email taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,password=password1, email=email , first_name=first_name, last_name=last_name)
                    user.save()
                    face = Face_registration.objects.create(username=username, email=email,face_reg=False)
                    face.save()
                    messages.info(request,'User created')
                    context = { 
                    'email' : email,
                    'username' : username}
                    return render(request, 'face_register.html', context=context)
            else:
                messages.info(request,'Password not maching')
                print('password not maching')
                return redirect('register')
            return render(request, 'register.html')
        else:
            return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('register')

def index(request):
    if request.user.is_authenticated:
        usr = Face_registration.objects.get(username=request.user.username)
        context ={
            "data" : usr.data
        }
        return render(request, 'index.html', context=context)
    else:
        return render(request,'login.html')

def info(request):
    if request.user.is_authenticated:
        return render(request,'info.html')
    else:
        return render(request,'login.html')