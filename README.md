# insecure-django
For http://cybersecuritybase.mooc.fi/

# At least 5 flaws from OWASP top 10

https://owasp.org/www-project-top-ten/

# Usage:

"standard django" I hope :)


```bash
$ python3 -m venv venv_test
$ source venv_test/bin/activate
$ git clone https://github.com/martbhell/insecure-django
$ pip install -r requirements.txt
$ cd licensegenerator
$ python manage.py migrate
$ python manage.py runserver &
$ curl localhost:8000
```

# Features:

Functions:
- Login page
- Database with:
    - Table/Model Users (default django)
	- Table/Model Profile (username, social security number, password, num_licenses, admin)
	- Table/Model Licenses (licenseid, owner, mac_address, created_at, expired_at)
- Hidden API call to view all users /accounts/
- License Code List & Generator on / or /licenses
- /admin/ page for adding licenses

