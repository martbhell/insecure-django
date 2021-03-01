from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Profile, License
import time
import datetime
import json
import logging
import sys

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )

@login_required
def AllAccountsView(request):
    # Return a handy list of profiles for automating system administration
    logged_in_user = User.objects.get(username=request.user)
    logged_in_profile = Profile.objects.get(user=logged_in_user)
    if not logged_in_profile.admin:
        msg = { "msg": "user %s attempted to access the AllAccountsView" % (str(request.user)), "user": str(request.user), "function": "AllAccountsView" }
        logger.warn(__name__ + " JSON= " + str(msg))
        return redirect('/')

    users = User.objects.all()
    profiles = Profile.objects.all()
    pretty = request.GET.get('pretty')
    ulist = []
    plist = []
    for user in users:
        ulist.append(user)
        try:
            plist.append(Profile.objects.get(user=user.id))
        except:
            print("no profile for %s" % user)
            pass

    datadict = {}
    for p in plist:
        ss = p.social_security
        u = str(p.user)
        a = p.admin
        n = p.num_licenses
        d = p.description
        #print(type(ss))
        #print(type(u))
        #print(type(a))
        #print(type(n))
        datadict[ss] = { "social_security": ss, "username": u, "admin": a, "num_licenses": n, "description": d }

    msg = { "msg": "user %s accessed the AllAccountsView" % (str(request.user)), "user": str(request.user), "function": "AllAccountsView" }

    print(type(datadict))

    logger.warn(__name__ + " JSON= " + str(msg))

    if pretty or pretty == "":
        return JsonResponse(datadict, safe=True, json_dumps_params={'indent': 2})
    return JsonResponse(datadict)


def AdminView(request):
    # send a long a list of users
    users = User.objects.all()
    ulist = []
    for user in users:
        ulist.append(user)

    return render(request, 'admin.html', {'users': ulist } )

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
            e = sys.exc_info()[0]
            msg = { "msg": "User %s tried to add MAC %s which was denied because we got error %s (%s)" % (str(user), MAC, e, e.__doc__), "user": str(user), "MAC": MAC, "exception": str(e), "doc": str(e.__doc__) }
            logging.error(__name__ + " JSON= " + str(msg))
            return HttpResponse("Error: No MAC")

def LicensesView(request):

    user = request.user
    data = []
    if len(User.objects.all()) == 0:
        CreateUsers(request)

    if not user.is_anonymous:
        licenses = License.objects.filter(owner=user)
        #print(licenses.__dict__)
        #print(licenses)
        for l in licenses:
#            print(l.licenseid)
            licenseid = l.licenseid
            owner = l.owner
            created_at = l.created_at
            expire_at = l.expire_at
            mac_address = l.mac_address
            data.append({"licenseid": licenseid, "owner": owner, "created_at": created_at, "expire_at": expire_at, "mac_address": mac_address })

    return render(request, 'index.html', {'licenses': data})

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
        alicepro = Profile.objects.create(user=alice, social_security="19990103-5555", num_licenses=6)
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

@login_required
def AddUserLicenses(request):

    if request.method == "POST":
        more_licenses = request.POST.get('more_licenses', '0')
        chosen_user = request.POST.get('chosen_user', '')
        user = User.objects.get(username=chosen_user)
        logged_in_user = User.objects.get(username=request.user)
        logged_in_profile = Profile.objects.get(user=logged_in_user)
        profile = Profile.objects.get(user=user)
        if logged_in_profile.admin:
            user_licenses = profile.num_licenses
            profile.num_licenses = int(profile.num_licenses) + int(more_licenses)
            profile.save()
            return HttpResponse("OK: %s for %s that has %s" % (more_licenses, chosen_user, user_licenses))
        else:
            raise PermissionDenied
    else:
        return redirect('/admin')

@login_required
def AddProfileDescription(request):

    if request.method == "POST":
        description = request.POST.get('description', '')
        logged_in_user = User.objects.get(username=request.user)
        logged_in_profile = Profile.objects.get(user=logged_in_user)
        old_description = logged_in_profile.description
        logged_in_profile.description = description
        logged_in_profile.save()
        print("OK: Description set to %s for %s instead of %s" % (description, logged_in_user, old_description))
        return HttpResponse("OK: Description set to %s for %s" % (description, logged_in_user))
    else:
        return redirect('/')
