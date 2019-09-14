# Digital-Attendence<Enter>

 <Enter>
 
 ## Project Setup
 - First Of all create a virual environment.
 - Then install all the required packages from [requirements.txt](https://github.com/sbhusal123/Digital-Attendence/blob/master/app/requirements.txt) file  (<Enter> **Note that the requirement file is located inside the folder _app_**) using _**pip install -r requirements.txt**_
 - Then create the database as specified in the [settings.py](https://github.com/sbhusal123/Digital-Attendence/blob/master/app/app/settings.py).
 - Then migrate to update the database using **_python manage.py migrate_**
 - Then run the project : **_python manage.py runserver_**
 
 ## Snapshoots

1. Teacher's Panel
![Teacher's Panel](https://github.com/sbhusal123/Digital-Attendence/blob/master/snapshoots/teacher's%20panel.png?raw=true)

2. Student's Panel
![Student's Panel](https://github.com/sbhusal123/Digital-Attendence/blob/master/snapshoots/student's%20panel.png?raw=true)

3. Classes Attended By Student
![Class Attended By Students](https://github.com/sbhusal123/Digital-Attendence/blob/master/snapshoots/Student%20Attended%20Class.png?raw=true)

4. Lectures Missed By Stuent
![Missing Lectures](https://github.com/sbhusal123/Digital-Attendence/blob/master/snapshoots/Student%20Missing%20Class.png?raw=true)

5. Attendance Details in Teacher's Panel

![Class Details Of Teacher](https://github.com/sbhusal123/Digital-Attendence/blob/master/snapshoots/class%20details.png?raw=true)

## Issues:
### 1. Error on installing mysqlclient

> pip install mysqlclient

>Error: error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

##### For python 3:
sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip
     
##### For python 2:
sudo apt-get install python-dev  \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip

### 2. Timezone Configuration:

To view the list of avilable time zone:

[Time Zone Database ](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Then use one of the time zone in settings.py.

```python
TIME_ZONE = ".../..."
```
For example:
In case of Kathmandu
```python
TIME_ZONE = 'Asia/Kathmandu'
'''
