"""
URL configuration for BOOKSTORE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.login,name='home'),
    path('Book_list/',views.Book_list,name='Book_list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/',views.customer_register,name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('book_detail/<int:book_id>/',views.book_detail,name='book_detail'),
    path('add-to-cart/<int:book_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('wishlist_view/',views.wishlist_view,name='wishlist_view'),
    path('add_to_wishlist/<int:book_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('place_order/',views.place_order,name='place_order'),
    path('order_success/<int:order_id>/',views.order_success,name='order_success'),
    
    

]




if settings.DEBUG:urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
