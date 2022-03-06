import os

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from dateapp import settings
from .models import ImageUpload
import datetime


def deleteimage(request,pk):
    delete_image = ImageUpload.objects.get(pk = pk)
    os.remove(os.path.join(settings.MEDIA_ROOT, str(delete_image.imgfile)))
    delete_image.delete()
    return redirect('/')

def imageUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        date = request.POST['date']
        imagefile = request.FILES.get('imgfile', False)
        imageupload = ImageUpload(
            title=title,
            imgfile=imagefile,
            date=date,
        )
        try:
            imageupload.save()
            return redirect('/')
        except:
            raise Http404("Image does not exist")
    else:
        return render(request, 'imageupload.html')


def overview(request):
    imagefiles = ImageUpload.objects.all()

    today_date = datetime.date.today()
    start_date = datetime.date(2022, 2, 26)
    d_day = (today_date - start_date).days + 1
    context = {
        'd_day' : d_day,
        'imagefiles': imagefiles
    }
    return render(request, 'overview.html', context)
