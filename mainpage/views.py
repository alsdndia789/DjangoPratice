from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload


def imageUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        imagefile = request.FILES["imgfile"]
        imageupload = ImageUpload(
            title=title,
            content=content,
            imgfile=imagefile,
        )
        imageupload.save()
        return redirect('imageupload')
    else:
        imageuploadForm = ImageUploadForm
        context = {
            'imageuploadForm': imageuploadForm,
        }
        return render(request, 'imageupload.html', context)


def overview(request):
    imagefiles = ImageUpload.objects.all()
    print(imagefiles.values("title"))
    context = {
        'imagefiles': imagefiles
    }
    return render(request, 'overview.html', context)
