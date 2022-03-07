import os
# Create your views here.
from django.shortcuts import render, redirect

from dateapp import settings
from .models import ImageUpload, TodoList
import datetime


def image_detail(request, pk):
    image = ImageUpload.objects.get(pk=pk)
    data = {
        'image': image,
    }
    return render(request, 'image_detail.html', data)


def image_delete(request, pk):
    image = ImageUpload.objects.get(pk=pk)
    os.remove(os.path.join(settings.MEDIA_ROOT, str(image.imgfile)))
    image.delete()
    return redirect('/')


def image_upload(request):
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
            return render(request, 'page-404.html')
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


def todo_list_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        delete_list = request.POST.getlist("delete_list")
        done_delete_list = request.POST.getlist("done_delete_list")
        done_delete = request.POST.get("done_delete")
        not_done = request.POST.get("not_done")
        delete = request.POST.get("delete")
        done = request.POST.get("done")
        add = request.POST.get("add")

        todo_list_upload = TodoList(
            title=title,
        )
        if add == "add":
            try:
                todo_list_upload.save()
                return redirect('/todolist')
            except:
                return render(request, 'page-404.html')

        if delete == "delete":
            for item in delete_list:
                TodoList.objects.get(pk=item).delete()

        if done_delete == "done_delete":
            for item in done_delete_list:
                TodoList.objects.get(pk=item).delete()

        if done == "done":
            for item in delete_list:
                todo_list = TodoList.objects.get(pk=item)
                todo_list.done = True
                todo_list.save()
                print(TodoList.objects.get(pk=item).done)

        if not_done == "not_done":
            for item in done_delete_list:
                todo_list = TodoList.objects.get(pk=item)
                todo_list.done = False
                todo_list.save()

    todo_list = TodoList.objects.all()
    data = {
        "todo_list": todo_list
    }
    return render(request, 'todo_list.html', data)
