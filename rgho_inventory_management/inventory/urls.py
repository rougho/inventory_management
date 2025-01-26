from django.contrib import admin
from django.urls import path
from .views import Index, SignUp, Dashboard, Category, Navbar, AddItem,SearchInventory, EditItem, DeleteItem, category_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('navbar/', Navbar.as_view(), name='navbar'),
    path('add-item/',AddItem.as_view(), name='add-item'),
    path('search/', SearchInventory.as_view(), name='search_inventory'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('category/<int:category_id>/',category_view, name='category_view'),


]
