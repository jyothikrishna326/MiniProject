from django.contrib import admin
from App.models import Book,Author,Customer,Wishlist,CartItem,Order,OrderItem,Review
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Wishlist)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)