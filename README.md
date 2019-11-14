# NTU-CZ3002

Required packages:<br />
pip install Django<br />
pip install firebase-admin<br />
pip install Pillow<br />
pip install django-widget-tweaks<br />

Unzip Firebase JSON file (password-protected) before running web application<br />
Otherwise use your own Firebase JSON file and update path in this line in views.py:<br />
cred = credentials.Certificate("../cz3002-firebase-adminsdk-zn2kj-457d20ac3e.json")<br />

To get started, in terminal change directory to WebOne and create superuser: <br />
python manage.py createsuperuser <br />

Then start the application with: <br />
python manage.py runserver <br />

Then, go to http://127.0.0.1:8000/admin/ and log in using superuser account created earlier to add/manage new student & professor accounts.
