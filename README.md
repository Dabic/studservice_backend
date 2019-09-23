# **Studsentski servis - Backend**
<br>

>How to download the project?

In command line type the following:
```
 git clone https://github.com/Dabic/studservice_backend.git
 ```
 <br>
 
>Configure project dependencies

In command line type the following:
```
pip install -r requirements.txt
```

This will install dependencies need for to project expect mysqlclient.
<br>
<br>
>Installing mysqlclient

If you are using Python x64 then type the following:
```
pip install mysqlclient-1.4.4-cp37-cp37m-win_amd64.whl
```
<br>

If you are using Python x84 then type the following:
```
pip install mysqlclient-1.4.4-cp37-cp37m-win32.whl
```
<br>

>Starting the application

To run the server type the following code snippet:
```
python manage.py runserver
```
This will run the local server on your machine.<br>
Open the browser and navigate to http://127.0.0.1:8000/studserviceapp/
