from django.shortcuts import render,redirect
from .models import Book, CartItem, Customer
from django.contrib.auth.models import User
from django.contrib.auth import login
from App.forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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


def customer_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Customer.objects.create(user=user)
            
            login(request, user)  
            return redirect('Book_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def add_to_cart(request, book_id):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return HttpResponse("❌ Customer not found. Please register.")

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponse("📕 Book not found. Please try again.")  

    cart_item, created = CartItem.objects.get_or_create(customer=customer, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponse(f"✅ '{book.title}' added to cart successfully.")

# def cart_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')  

#     try:
#         customer = Customer.objects.get(user=request.user)
#     except Customer.DoesNotExist:
#         return redirect('book_list')  

#     cart_items = CartItem.objects.filter(customer=customer)
#     total_price = sum(item.book.price * item.quantity for item in cart_items)

#     return render(request, 'cart.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })

