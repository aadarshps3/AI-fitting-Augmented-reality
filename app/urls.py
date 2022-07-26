from django.urls import path

from app import views, userviews, apiviews

urlpatterns = [
    path('', views.home, name='home'),
    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('register', views.register, name='register'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('product_add', views.product_add, name='product_add'),
    path('product_view', views.product_view, name='product_view'),
    path('product_edit/<int:id>/', views.update_product, name='product_edit'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('view_payment/', views.view_payment,name='view_payment'),
    path('delivery_detail/', views.delivery_detail,name='delivery_detail'),
    path('complete_delivery/<int:id>/', views.complete_delivery,name='complete_delivery'),
    path('user_view', views.user_view, name='user_view'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('complaint_view', views.complaint_view, name='complaint_view'),
    path('reply_complaint/<int:id>/', views.reply_complaint, name='reply_complaint'),

    path('user_home', userviews.user_home, name='user_home'),
    path('user_add_complaint', userviews.complaint_add_user, name='user_add_complaint'),
    path('user_view_complaint', userviews.complaint_view_user, name='user_view_complaint'),
    path('user_profile', userviews.user_profile, name='user_profile'),
    path('profile_update/<int:id>/', userviews.profile_update, name='profile_update'),

    path('user_product_view', userviews.user_product_view, name='user_product_view'),
    path('product_detail/<int:id>/', userviews.product_detail,name='product_detail'),
    path('add_to_cart/<pk>/', userviews.add_to_cart, name='add_to_cart'),
    path('cart/', userviews.cart, name='cart'),
    path('remove_single_item_from_cart/<pk>/', userviews.remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('remove_from_cart/<pk>/', userviews.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:id>/', userviews.checkout, name='checkout'),
    path('payment/<int:id>/', userviews.payment,name='payment'),
    path('order_status/', userviews.order_status, name='order_status'),
    path('a/', userviews.a, name='a'),






    path('user_registration',apiviews.user_registration,name='user_registration')
]
