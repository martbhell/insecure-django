from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, License

# Create your views here.

def index(request):
    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )

def LicensesView(request):

    # user = request.user
    # search through the DB
    # make a dict with list of dicts
    # make it in JSON

    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )

def CreateUsers(request):
    print(User.objects.get(username='bob').__dict__)
    print(Profile.objects.all())
    print(User.objects.get(username='bob'))

    try:
        print("We already have a user called %s" % User.objects.get(username='bob'))
#        print("We already have a Profile called %s" % Profile.objects.get(username='bob'))
    except:
        bob = User.objects.create_user(username='bob', password='squarepants')

    try:
        print("We already have a Profile called %s" % Profile.objects.get(username='bob'))
    except:
        bob = Profile.objects.create_user(username='bob', password='squarepants')

    try:
        print("We already have a user called %s" % User.objects.get(username='alice'))
    except:
        alice = User.objects.create_user(username='alice', password='redqueen')

    return HttpResponse('OK: Users Created')
