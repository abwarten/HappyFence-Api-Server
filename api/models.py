from django.db import models

class Contact(models.Model): 
    name = models.CharField(max_length=30) # 제목 
    info = models.CharField(max_length=254) # 장르 
    time = models.DateTimeField()
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.name
