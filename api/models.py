from django.db import models

import os
import uuid
from datetime import datetime

def date_upload_to(instance, filename):
    path = datetime.now().strftime("%Y") + '/' + datetime.now().strftime("%m") + '/' + datetime.now().strftime("%d")  #년도 + 월 폴더
    # 길이 32 인 uuid 값
    uuid_name = uuid.uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        path,
        uuid_name + extension,
    ])

class Contact(models.Model):
    name = models.CharField(max_length=30) # 제목 
    info = models.CharField(max_length=254) # 장르 
    time = models.CharField(max_length=254) #날짜 및 시간
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.name

class TodayList(models.Model):
    image = models.ImageField(upload_to=date_upload_to)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)

class TableList(models.Model):
    days = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class TableItem(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)