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
#    print(User.objects.get(username='bob').__dict__)
#    print(Profile.objects.all())
#    print(User.objects.get(username='bob'))

    try:
        bob = User.objects.create_user(username='bob', password='squarepants')
    except:
        bob = User.objects.get(username='bob')
        print("We already have a user called %s" % bob)

    bobid = User.objects.get(username='bob').id
    try:
        bobpro = Profile.objects.create(user=bob, social_security="20010603-1234", num_licenses=2)
    except:
        bobpro = Profile.objects.get(user=bob)
        print("We already have a Profile called %s with SS %s" % (bob, bobpro.social_security))

    try:
        alice = User.objects.create_user(username='alice', password='redqueen')
    except:
        alice = User.objects.get(username='alice')
        print("We already have a user called %s" % alice)

    aliceid = User.objects.get(username='alice').id
    try:
        alicepro = Profile.objects.create(user=alice, social_security="20010603-1234", num_licenses=2)
    except:
        print("We already have a Profile called %s" % alice)

    return HttpResponse('OK: Users Created')
