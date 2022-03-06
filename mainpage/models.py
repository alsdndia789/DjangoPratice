from django.db import models


# Create your models here.
class ImageUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=False, upload_to="", blank=True)
    date = models.DateField(null=False)
    content = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.title
