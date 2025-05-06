from django.contrib import admin
from . models import CustomUser,Purchase
from game_app_staff.models import Staff,Game

# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['user','game','amount','payment_status']

class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email','phone']

class StaffAdmin(admin.ModelAdmin):
    list_display=['user','email','phone']
    
class GameAdmin(admin.ModelAdmin):
    list_display=['name','price','description','category','file','image']

admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Game,GameAdmin)
