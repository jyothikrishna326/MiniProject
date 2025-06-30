from django.shortcuts import render,redirect
from .models import Book, CartItem, Customer
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


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('book_list')  

    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

