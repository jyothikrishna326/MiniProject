from django.shortcuts import render,redirect
from .models import Book, CartItem, Customer,Wishlist,Customer
from django.contrib.auth.models import User
from django.contrib.auth import login
from App.forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def Book_list(request):
    query = request.GET.get("q", "")
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'query': query})

def book_detail(request,book_id):
    try:
        book=Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponse("Book not found")
    return render(request,'book_detail.html',{'book':book})


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


def add_to_wishlist(request, book_id):
    customer = request.user.customer
    book = Book.objects.get(id=book_id)

    if not Wishlist.objects.filter(customer=customer, book=book).exists():
        Wishlist.objects.create(customer=customer, book=book)

    return redirect('wishlist_view')

def wishlist_view(request):
    customer = request.user.customer
    wishlist_items = Wishlist.objects.filter(customer=customer)

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})




def remove_from_wishlist(request, book_id):
    book_qs = Book.objects.filter(id=book_id)
    if not book_qs.exists():
        return redirect('wishlist_view')

    book = book_qs.first()
    customer_qs = Customer.objects.filter(user=request.user)
    if not customer_qs.exists():
        return redirect('wishlist_view')  
    customer = customer_qs.first()
    wishlist_item = Wishlist.objects.filter(customer=customer, book=book).first()
    if wishlist_item:
        wishlist_item.delete()

    return redirect('wishlist_view')