import os

import boto3
from django.shortcuts import render, redirect

from dateapp import settings
from .models import ImageUpload, TodoList
import datetime


def start():
    return datetime.date(2022, 2, 26)


def today():
    return datetime.date.today()


def calculate_d_day():
    return (today() - start()).days + 1


def overview(request):
    imagefiles = ImageUpload.objects.all()
    d_day = calculate_d_day()

    context = {
        "d_day": d_day,
        "imagefiles": imagefiles
    }

    return render(request, "overview.html", context)


class HandleImage:
    def __init__(self):
        self.image = ImageUpload.objects.all()

    def sort_by_id(self, pk):
        return self.image.get(pk=pk)

    def detail(self, pk):
        return {"image": self.sort_by_id(pk)}

    def delete(self, pk):
        image = self.sort_by_id(pk)
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=os.path.join("media", str(image.imgfile)),
        )
        image.delete()

    def sort_by_date(self, date):
        return self.image.filter(date=date)

    def by_date(self, request):
        date = request.POST.get("date", today().strftime("%Y-%m-%d"))
        show_all_date = self.image.values("date").distinct()

        data = {
            "date": date,
            "imagefiles": self.sort_by_date(date),
            "show_all_date": show_all_date
        }
        return data


def image_by_date(request):
    data = HandleImage().by_date(request)
    return render(request, "image/image_by_date.html", data)


def image_detail(request, pk):
    data = HandleImage().detail(pk)
    return render(request, "image/image_detail.html", data)


def image_delete(request, pk):
    HandleImage().delete(pk)
    return redirect("/")


def image_parsed_data(request):
    title = request.POST.get("title")
    date = request.POST.get("date")
    content = request.POST.get("content")
    imagefile = request.FILES.get("imgfile", False)

    parsed_data = {
        "title": title,
        "date": date,
        "content": content,
        "imagefile": imagefile,
    }
    return parsed_data


def image_upload(request):
    parsed_data = image_parsed_data(request)
    imageupload = ImageUpload(
        title=parsed_data["title"],
        imgfile=parsed_data["imagefile"],
        date=parsed_data["date"],
        content=parsed_data["content"],
    )
    try:
        imageupload.save()
        return redirect("/")
    except:
        return render(request, "image/image_upload.html")


class HandleTodoList:
    def __init__(self):
        self.todo_list = TodoList.objects.all()

    def add(self, value):
        try:
            todo_list_upload = TodoList(title=value)
            todo_list_upload.save()
            return redirect("/todolist")

        except:
            return redirect("page-404.html")

    def delete(self, lists):
        for item in lists:
            self.todo_list.get(pk=item).delete()

    def move(self, lists):
        for item in lists:
            todo_list = self.todo_list.get(pk=item)
            todo_list.done = True if not todo_list.done else False
            todo_list.save()

    def data(self):
        return {"todo_list": self.todo_list}


def todo_list_parsed_data(request):
    context = request.POST.get("context")
    delete_list = request.POST.getlist("delete_list")
    done_delete_list = request.POST.getlist("done_delete_list")
    done_delete = request.POST.get("done_delete")
    not_done = request.POST.get("not_done")
    delete = request.POST.get("delete")
    done = request.POST.get("done")
    add = request.POST.get("add")

    parsed_data = {
        "context": context,
        "delete_list": delete_list,
        "done_delete_list": done_delete_list,
        "done_delete": done_delete,
        "not_done": not_done,
        "delete": delete,
        "done": done,
        "add": add,
    }

    return parsed_data


def todo_list_page(request):
    parsed_data = todo_list_parsed_data(request)

    if parsed_data["add"] == "add":
        HandleTodoList().add(parsed_data["context"])

    if parsed_data["delete"] == "delete":
        HandleTodoList().delete(parsed_data["delete_list"])

    if parsed_data["done_delete"] == "done_delete":
        HandleTodoList().delete(parsed_data["done_delete_list"])

    if parsed_data["done"] == "done":
        HandleTodoList().move(parsed_data["delete_list"])

    if parsed_data["not_done"] == "not_done":
        HandleTodoList().move(parsed_data["done_delete_list"])

    data = HandleTodoList().data()

    return render(request, "todo_list.html", data)
