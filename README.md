# NTU-CZ3002

Required packages:<br />
pip install Django<br />
pip install firebase-admin<br />
pip install Pillow<br />
pip install django-widget-tweaks<br />

Unzip Firebase JSON file (password-protected) before running web application<br />
Otherwise use your own Firebase JSON file and update path in this line in views.py:<br />
cred = credentials.Certificate("../cz3002-firebase-adminsdk-zn2kj-457d20ac3e.json")<br />
