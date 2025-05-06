from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path("home",views.home,name='home'),
    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('user_profile',views.user_profile,name='user_profile'),

    path('game_list',views.game_list,name='game_list'),
    path('search_game',views.search_game,name='search_game'),
    path('purchase_game/<int:game_id>/', views.purchase_game, name='purchase_game'),
    path('payment_success/<int:purchase_id>/', views.payment_success, name='payment_success'),
    path('dummy_payment/<int:purchase_id>/',views.dummy_payment, name='dummy_payment'),
    path('payment_cancel/<int:purchase_id>/', views.payment_cancel, name='payment_cancel'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
]
