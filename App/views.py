from django.shortcuts import render,redirect
from .models import Book, CartItem, Customer,Wishlist,Order, OrderItem,Review
from django.contrib.auth.models import User
from django.contrib.auth import login
from App.forms import UserRegistrationForm,CustomerForm,ReviewForm,Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



# Create your views here.

def home (request):
    return render(request,'login.html')
def Book_list(request):
    query = request.GET.get("q", "")
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'query': query})

def customer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        pincode = request.POST['pincode']

        # Create User object
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Create Customer object linked to User
        customer = Customer.objects.create(
            user=user,
            address=address,
            phone_number=phone,
            pincode=pincode
        )

        # Log in the user after registration
        login(request, user)
        return redirect('profile')
    else:
        return render(request, 'register.html')



def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = None
    return render(request, 'profile.html', {
        'user': request.user,
        'customer': customer,
    })


def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        reviews = book.reviews.all()
    except Book.DoesNotExist:
        return HttpResponse("Book not found")

    form = None
    if request.user.is_authenticated and hasattr(request.user, 'customer'):
        customer = request.user.customer
        existing_review = Review.objects.filter(book=book, customer=customer).first()

        if not existing_review:
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    new_review = form.save(commit=False)
                    new_review.book = book
                    new_review.customer = customer
                    new_review.save()
                    return redirect('book_detail', book_id=book.id)
            else:
                form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'book_detail.html', context)








        

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

    return redirect('cart_view')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('book_list')  

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



def place_order(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(customer=customer)

        if not cart_items.exists():
            return redirect('cart_view')

        order = Order.objects.create(customer=customer)
        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)

        cart_items.delete()

        return redirect('order_success',order_id=order.id)
    return redirect('cart_view')

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})


