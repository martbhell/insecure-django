from django.contrib.auth.models import User

bob = User.objects.create_user(username='bob', password='squarepants')
alice = User.objects.create_user(username='alice', password='redqueen')
