from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('login/', views.loginPage, name='login'),
	path('register/', views.registerPage, name='register'),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.store, name="store"),
    path('contact/', views.contactView, name="contact"),
    path('success/', views.successView, name="success"),
    path('about/', views.about, name="about"),
    path('product/<str:pk>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('dashboard/', views.dashboardView, name='dashboard'),
    path('order_list/', views.orderList, name='order_list'),
    path('order_item_list/<str:pk>', views.orderItemList, name='order_item_list'),
    path('customer_list/', views.customerList, name='customer_list'),

    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('create_order_items/<str:order_pk>/', views.createOrderItems, name="create_order_items"),
    path('delete_order_item/<str:order_item_pk>/', views.deleteOrderItem, name="delete_order_item"),

    path('create_shipping/<str:shipping_create_pk>/', views.createShippingInformation, name="create_shipping"),
    path('update_shipping/<str:shipping_update_pk>/', views.updateShippingInformation, name="update_shipping"),

    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('place_order/<str:pk>/', views.placeOrder, name='place_order'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),
    path('create_customer/', views.createCustomer, name="create_customer"),

    path('user/', views.userView, name='user'),
    path('account_settings/', views.accountSettings, name="account_settings"),
    path('order_details/<str:pk>', views.customerOrderDetails, name='order_details'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_done.html"), 
        name="password_reset_complete"),

]
