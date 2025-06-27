from django.shortcuts import render
from .models import Book
from django.http import HttpResponse

# Create your views here.

def Book_list(request):
    Books = Book.objects.all()
    return render(request,'book_list.html',{'books':Books})

def book_detail(request,id):
    try:
        Book=Book.objects.get(id=id)
    except Book.DoesNotExist:
        raise HttpResponse("Book not found")
    return render(request,'book_detail.html',{'book':Book})