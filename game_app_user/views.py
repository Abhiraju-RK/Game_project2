from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from . models import CustomUser,Purchase
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from game_app_staff.models import Game,Staff
import stripe
from django.conf import settings
# Create your views here.

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def user_register(request):
    if request.method == "POST":
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        phone=request.POST.get("phone")

        if not username or not first_name or not last_name or not email or not password or not confirm_password or not phone:
            messages.error(request,"All field requires ")
            return redirect("user_register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email Already Taken !!")
            return redirect("user_register")
        if len(password)<5:
            messages.error(request,"Password Contain More than 5 charachter !!")
            return redirect("user_register")
        if confirm_password!=password:
            messages.error(request,"Confirm password Didnt match !!")
            return redirect("user_register")
        
        if len(phone)!=10 or not phone.isdigit():
            messages.error(request,"Phone mumber must be 10 digit!!")
            return redirect("user_register")
        
        user=CustomUser.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password,phone=phone)
        user.save()
        messages.success(request,f"{ user.username } register successfully ")
        return redirect("user_login")
    return render(request,"user_register.html")

def user_login(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user_obj=CustomUser.objects.get(email=email)
            username=user_obj.username
        except CustomUser.DoesNotExist:
            messages.error(request,'You are not a register user !!')
            return redirect('user_register')
        user=authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_staff:
                messages.error(request, "Staff members are not allowed to log in here.")
                return redirect("user_login")
            login(request,user)
            messages.success(request,"Logged Successfully ")
            return redirect("home")
        else:
            messages.error(request,"Cannot be loginn !!")
    return render(request,"user_login.html")

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def user_profile(request):
    user=request.user
    if request.method == "POST":
        if "user_profile" in request.POST:
            user.username=request.POST.get('username',user.username)
            user.fist_name=request.POST.get('fist_name',user.first_name)
            user.last_name=request.POST.get('last_name',user.last_name)
            user.email=request.POST.get('email',user.email)
            user.phone=request.POST.get('phone',user.phone)
            user.save()

            messages.success(request, "Profile updated successfully!")

        elif "update_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect!")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")

        return redirect('user_profile')
    return render(request, 'user_profile.html', {'user': user})
    
@login_required
def game_list(request):
    games=Game.objects.all().order_by('-created_at')
    return render(request,'game_list.html',{'games':games})

@login_required
def search_game(request):
    query=request.GET.get('q','').strip().capitalize()
    valid_categories = [choice[0] for choice in Game.CATEGORY_CHOICES]
    if query in valid_categories:
        games=Game.objects.filter(category=query).order_by('-created_at')
        if not games.exists():
            messages.error(request, "No games found in this category!") 
    else:
        messages.error(request, "Invalid Category!")  
        games = Game.objects.all().order_by('-created_at')
    return render(request,'game_list.html',{'games': games})

@login_required
def purchase_game(request,game_id):
    game=get_object_or_404(Game,id=game_id)
    
    if game.category.lower() == 'free':
        Purchase.objects.create(user=request.user, amount=0, game=game, payment_status='Approved')
        messages.success(request, "Free game added to your downloads!")
        return redirect('purchase_history')  # Redirect to purchase history

    elif game.category.lower() == 'premium':  # Correct category name
        Purchase.objects.create(user=request.user, game=game, amount=game.price, payment_status='Pending')
        messages.info(request, "Your purchase request has been sent for approval.")
        return redirect('purchase_history')  # Redirect to purchase history

    return redirect('game_list')
    
@login_required
def dummy_payment(request, purchase_id):
    purchase=get_object_or_404(Purchase,id=purchase_id)
    if purchase.payment_status!='Approved':
        messages.error(request, "Your purchase has not been approved yet!")
        return redirect('purchase_history')
    return render(request, 'dummy_payment.html', {'purchase': purchase})
    
@login_required
def payment_success(request, purchase_id):
    purchase=get_object_or_404(Purchase,id=purchase_id)
    game = purchase.game

    purchase.payment_status="Paid"
    purchase.save()

    messages.success(request, "Payment successful! You can now download your game.")
    return redirect('purchase_history')

@login_required
def payment_cancel(request, purchase_id):
    messages.error(request, "Payment cancelled.")
    return redirect('purchase_history')

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'purchase_history.html', {'purchases': purchases})

