from django.db import models


class ImageUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=False, upload_to="", blank=True)
    date = models.DateField(null=False)
    content = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.title


class TodoList(models.Model):
    title = models.TextField(max_length=40, null=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class WentList(models.Model):
    title = models.TextField(max_length=40, null=False)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.title
