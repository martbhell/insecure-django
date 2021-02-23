from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )

def LicensesView(request):

    # user = request.user
    # search through the DB
    # make a dict with list of dicts
    # make it in JSON

    return render(request, 'index.html', {'licenses': [ { "licenseid": "123ABC", "owner": "bob", "created_at": "2021-12-13", "expired_at": "2022-12-13"} ] } )
