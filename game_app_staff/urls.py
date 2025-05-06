from django.urls import path
from . import views

urlpatterns = [
    path('staff_register',views.staff_register,name='staff_register'),
    path('staff_login',views.staff_login,name='staff_login'),
    path('staff_logout',views.staff_logout,name='staff_logout'),
    path('staff_profile',views.staff_profile,name='staff_profile'),
    path('staff_home',views.staff_home,name='staff_home'),
    path('staff_dashboard',views.staff_dashboard,name='staff_dashboard'),

    path('add_game',views.add_game,name='add_game'),
    path('edit_game/<int:game_id>/',views.edit_game,name='edit_game'),
    path('staff_game_list',views.staff_game_list,name='staff_game_list'),

    path('manage_purchase',views.manage_purchase,name='manage_purchase'),
    path('approve_purchase/<int:purchase_id>/',views.approve_purchase,name='approve_purchase'),
    path('reject_purchase/<int:purchase_id>/',views.reject_purchase,name='reject_purchase'),


]
