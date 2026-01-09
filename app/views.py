from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.contrib import messages
from .models import Buyer, Artisan, Art, Account, Purchase, Payment
from django.core.mail import send_mail
import threading

# Create your views here.

def send_email_async(subject, message, from_email, recipient_list):
    threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        daemon=True
    ).start()

class Index(View):
    def get(self, request):
        return render(request, "index.html")


class Artisan_Login(View):
    def get(self, request):
        return render(request, "artisan_login.html")
    def post(self, request):
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not email or not password:
                messages.error(request, "Please fill in all fields.") #type:ignore
                return redirect("artisan_login")

            try:
                artisan = Artisan.objects.get(email=email)
                if artisan and check_password(password, artisan.password):
                    request.session['email'] = artisan.email #type:ignore
                    return redirect('artisans')
                else:
                    messages.error(request, "Incorrect email or password.")
                    return redirect("artisan_login")                
                
            except Artisan.DoesNotExist:
                messages.error(request, "Unknown User Credentials") #type:ignore
                return redirect("artisan_login")
            return render(request, "artisan_login.html")
                        

class SignUp(View):
    # Create new users
    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        if request.method == "POST":
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            role = request.POST.get('role')
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')

            if pwd1 and pwd2 and pwd1 != pwd2:
                messages.error(request, "The two passwords did not match.")
                return redirect("register")
            hashed_password = make_password(pwd1)
            if role == "Artisan":
                if Artisan.objects.filter(email=email).exists():
                    messages.error(request, f"The email address {email} already exist")
                    return redirect("register")
                else:


                    artisan = Artisan(
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        phone=phone,
                        address=address,
                        password=hashed_password
                    
                        )
                    artisan.save()
                    messages.success(request, "Account created successfully!")
                    return redirect("artisan_login")

            else:
                if Buyer.objects.filter(email=email).exists():
                    messages.error(request, f"The email address {email} already exist")
                    return redirect("register")
                else:
                    buyer = Buyer(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phone=phone,
                    address=address,
                    password=hashed_password
                )
                buyer.save()
                messages.success(request, "Account created successfully!")
                return redirect("buyer_login")

        return render(request, "register.html")

class DashboardArtisans(View):
    # Manage artisans functions
    def get(self, request):
        email = request.session.get('email')
        if not email:
            return redirect('artisan_login')
        if email is None:
            return redirect('artisan_login')

        user = Artisan.objects.get(email=email)
        arts = Art.objects.filter(artisan=user).order_by("-uploaded")
        account = Account.objects.filter(artisan=user).first()
        orders = Purchase.objects.filter(art__in=arts).order_by("-dateOfpurchase")
        payments = Payment.objects.filter(artisan=user).order_by("-date")
        context ={
            'user':user,
            'arts':arts,
            'account':account,
            'orders':orders,
            'payments':payments
        }
        return render(request, "artisans.html", context)

class AddCraft(View):
    # Add new designs
    def get(self, request):
        return render(request, "add_design.html")
    def post(self, request):
        email = request.session.get('email')
        if request.method == "POST":
            design = request.FILES.get('design')
            name = request.POST.get('name')
            price = request.POST.get('price')

            allowed_extensions = ['jpeg', 'jpg', 'png']
            if design:
                extension = design.name.split('.')[-1].lower()
                if extension not in allowed_extensions:
                    messages.error(request, "Invalid file format! Only file types jpeg, jpg, or png are allowed")
                    return redirect('add_design')
            
            user = Artisan.objects.get(email=email)
            craft = Art(
                artisan=user,
                art=design,
                art_name=name,
                price=price
            )
            craft.save()
            try:
                buyers = Buyer.objects.all()
                for each in buyers:
                    buyers_email = each.email
                    buyers_name = each.firstname
                    
                    subject = "New Art Design Available"
                    message = f"Greetings, {buyers_name}.\n You may be interested to see a new art posted on the Ebonyi State Art Market platform.\n We suggest you quickly login to check.\n Thanks, the team."
                    from_email = 'paulekung@yahoo.com'
                    recipient_list = [buyers_email]
                    send_email_async(subject, message, from_email, recipient_list)
            except Exception as e:
                    pass
            return redirect('artisans')
        return render(request, "add_design.html")

class UpdateArtisanProfile(View):
    def get(self, request, uuid):
        artisan = Artisan.objects.get(uuid=uuid)
        context = {
            'artisan':artisan
        }
        return render(request, "artisan_update.html", context)
    def post(self, request, uuid):
        artisan = Artisan.objects.get(uuid=uuid)
        if request.method=="POST":
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')

            artisan.firstname = firstname
            artisan.lastname = lastname
            artisan.email = email
            artisan.phone = phone
            artisan.address = address
            artisan.save()
            messages.success(request, "Profile updated successfully! Please login to your account to effect profile update")       
            return redirect("artisan_login")
            
        return render(request, "artisan_update.html")

class ArtisanAddPaymentAccount(View):
    def get(self, request):
        email = request.session.get('email')
        return render(request, "add_account.html")   
    def post(self, request):
        email = request.session.get('email')
        user = Artisan.objects.get(email=email)
        if request.method == 'POST':
            account_number = request.POST.get('account_number')
            account_name = request.POST.get('account_name')
            bank = request.POST.get('bank')

            if not account_number.isdigit():
                messages.error(request, f"Invalid account number {account_number}")
                return redirect('add_account')
            account = Account(
                artisan=user,
                account_number=int(account_number),
                account_name=account_name,
                bank=bank
            )
            account.save()
            return redirect('artisans')
        return render(request, "add_account.html")   

class ArtisanUpdateAccount(ArtisanAddPaymentAccount):
    def post(self, request):
        email = request.session.get('email')
        user = Artisan.objects.get(email=email)
        account = Account.objects.filter(artisan=user).first()
        if request.method == 'POST' and account:
            account_number = request.POST.get('account_number')
            account_name = request.POST.get('account_name')
            bank = request.POST.get('bank')

            if not account_number.isdigit():
                messages.error(request, f"Invalid account number {account_number}")
                return redirect('update_account')
            account.account_number = int(account_number)#type:ignore
            account.account_name = account_name
            account.bank = bank
            account.save()
            return redirect('artisans')
        return render(request, "add_account.html")


def logoutArtisan(request):
        logout(request)
        return redirect("artisan_login")

def logoutBuyer(request):
        logout(request)
        return redirect("buyer_login")

    
class Buyer_Login(View):
    def get(self, request):
        return render(request, "buyer_login.html")
    def post(self, request):
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not email or not password:
                messages.error(request, "Please fill in all fields.") #type:ignore
                return redirect("buyer_login")

            try:
                buyer = Buyer.objects.get(email=email)
                if buyer and check_password(password, buyer.password):
                    request.session['email'] = buyer.email #type:ignore
                    return redirect('buyers')
                else:
                    messages.error(request, "Incorrect email or password.")
                    return redirect("buyer_login")                
                
            except Buyer.DoesNotExist:
                messages.error(request, "Unknown User Credentials") #type:ignore
                return redirect("buyer_login")
            return render(request, "buyer_login.html")
    
class BuyerDashboard(View):
    def get(self, request):
        email = request.session.get('email')
        if not email:
            return redirect('buyer_login')
        if email is None:
            return redirect('buyer_login')

        user = Buyer.objects.get(email=email)
        arts = Art.objects.all().order_by("-uploaded")
        carts = Purchase.objects.filter(buyer=user).order_by("-dateOfpurchase")
        context ={
            'user':user,
            'arts':arts,
            'carts':carts
        }
        return render(request, "buyers.html", context)


class ConfirmAddToCart(View):
    def get(self, request, uuid):
        art = Art.objects.get(uuid=uuid)
        context = {
            'art':art
        }
        return render(request, "confirm_add_cart.html", context)
    
    def post(self, request, uuid):
        art = Art.objects.get(uuid=uuid)
        email = request.session.get('email')
        user = Buyer.objects.get(email=email)
        if request.method == "POST":
            confirmation = request.POST.get('confirmed')
            if confirmation:
                purchase = Purchase(
                    buyer=user,
                    art=art,
                    payment_status="Not Paid"

                )
                purchase.save() 
                return redirect('buyers')
        return render(request, "confirm_add_cart.html")

                        
class MakePayment(View):
    def get(self, request, uuid):
        cart = Purchase.objects.get(uuid=uuid)
        artsian = cart.art.artisan
        account = Account.objects.filter(artisan=artsian).first()
        context = {
            'cart':cart,
            'account':account
        }
        return render(request, "payment.html", context)
    
    def post(self, request, uuid):
        cart = Purchase.objects.get(uuid=uuid)
        artsian = cart.art.artisan
        email = request.session.get('email')
        buyer = Buyer.objects.get(email=email)

        if request.method == "POST":
            proof = request.FILES.get('proof')
             

            allowed_extensions = ['jpeg', 'jpg', 'png']
            if proof:
                extension = proof.name.split('.')[-1].lower()
                if extension not in allowed_extensions:
                    messages.error(request, "Invalid file format! Only file types jpeg, jpg, or png are allowed")
                    return redirect('payment') 
            
            payment = Payment(
                buyer=buyer,
                artisan=artsian,
                purchase=cart,
                payment_proof=proof
            )  
            cart.payment_status = "Paid"
            cart.save()
            payment.save()
            
            return redirect('buyers')
        return render(request, "payment.html")


class ConfirmPayment(View):
    def get(self, request, uuid):
        purchase = Purchase.objects.get(uuid=uuid)
        context = {
            'purchase':purchase
        }
        return render(request, "confirm_payment.html", context)
    
    def post(self, request, uuid):
        purchase = Purchase.objects.get(uuid=uuid)
        if request.method == "POST":
            confirmation = request.POST.get('confirmed')
            if confirmation:
                purchase.payment_status = "Verified"
                purchase.save() 
                return redirect('artisans')
        return render(request, "confirm_payment.html")

    




