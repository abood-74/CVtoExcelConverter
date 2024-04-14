from django.db import models


class CV(models.Model):
    name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='cv_files/')
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    text_content = models.TextField()