import os

from django.http import Http404
# Create your views here.
from django.shortcuts import render, redirect

from dateapp import settings
from .models import ImageUpload
import datetime


def imagedetail(request, pk):
    image_detail = ImageUpload.objects.get(pk=pk)
    data = {
        'image_detail': image_detail,
    }
    return render(request, 'image_detail.html', data)


def imagedelete(request, pk):
    image_delete = ImageUpload.objects.get(pk=pk)
    os.remove(os.path.join(settings.MEDIA_ROOT, str(image_delete.imgfile)))
    image_delete.delete()
    return redirect('/')


def imageUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        date = request.POST['date']
        content = request.POST['content']
        imagefile = request.FILES.get('imgfile', False)
        imageupload = ImageUpload(
            title=title,
            imgfile=imagefile,
            date=date,
            content=content,
        )
        try:
            imageupload.save()
            return redirect('/')
        except:
            raise Http404("Image does not exist")
    else:
        return render(request, 'image_upload.html')


def overview(request):
    imagefiles = ImageUpload.objects.all()

    today_date = datetime.date.today()
    start_date = datetime.date(2022, 2, 26)
    d_day = (today_date - start_date).days + 1
    context = {
        'd_day': d_day,
        'imagefiles': imagefiles
    }
    return render(request, 'overview.html', context)
