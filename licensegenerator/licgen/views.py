from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, License
import time
import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )

def GenerateLicense(MAC):

    now = time.time()

    if ":" in MAC or "-" in MAC:
        step1_license = MAC+str(now)
        step2_license = step1_license.replace(":", "").replace(".", "")
        return (step2_license, now)
    else:
        print("not a MAC")
        return False


def AddLicense(request):

    user = request.user

    profile = Profile.objects.get(user=user)
    user_licenses_left = profile.num_licenses

#    print(user_licenses_left)

    if user_licenses_left <= 0:
        return HttpResponse("Error: No licenses left")

    if request.method == "POST":
        print("POST")
#        print("existing: %s" % License.objects.get(licenseid="abc"))
        try:
            MAC = request.POST.get('MAC', '')
            license, now = GenerateLicense(MAC)

            now_1y = now + 31556926
            try:
                License.objects.create(licenseid=license, owner=user, created_at=datetime.datetime.fromtimestamp(now), expire_at=datetime.datetime.fromtimestamp(now_1y), mac_address=MAC)
                profile.num_licenses = profile.num_licenses - 1 
                profile.save()
                print("Licenses left: %s" % profile.num_licenses)
                return HttpResponse("OK: License Added")
            except:
                print("existing: %s" % License.objects.get(licenseid=license))
        except:
            return HttpResponse("Error: No MAC")

def LicensesView(request):

    user = request.user
    if not user.is_anonymous:
        licenses = License.objects.filter(owner=user)
        print(licenses.__dict__)

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

    try:
        admin = User.objects.create_user(username='admin', password='nimda')
    except:
        admin = User.objects.get(username='admin')
        print("We already have a user called %s" % admin)

    adminid = User.objects.get(username='admin').id
    try:
        adminpro = Profile.objects.create(user=admin, social_security="19666666-1234", num_licenses=99, admin=True)
    except:
        print("We already have a Profile called %s" % admin)

    return HttpResponse('OK: Users Created')
