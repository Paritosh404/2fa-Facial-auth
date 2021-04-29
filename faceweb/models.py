from django.db import models
import os
import uuid
import random

from datetime import datetime 

def user_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.now()

    path = str(todays_date.year) + str(todays_date.month) + str(todays_date.day)
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))

    # Filename reformat
    filename_reformat = path + stringId + randInt + extension

    return os.path.join('', filename_reformat)
# Create your models here.
class Face_registration(models.Model):
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    face_reg = models.BooleanField(default=False)
    encodings = models.CharField(max_length=100)
    vid = models.FileField(upload_to=user_directory_path)
    data = models.TextField()


