from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import Contact
from .forms import NewUserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def akey(request):
    konekte = request.user.is_authenticated
    context = {
        'konekte': konekte
    }
    return render(request, 'base.html', context)

def konekte(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            non = request.POST.get("non")
            modpas = request.POST.get("modpas")
            user = authenticate(username=non, password=modpas)

            if user is not None:
                login(request, user)
                print('identifikasyon an fet')
                return redirect(akey)
            else:
                print('idantifyan yo pa korek...')

        context = {}
        return render(request, 'konekte.html', context)
    else:
        return redirect(akey)
@login_required
def dekonekte(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(akey)
    else:
        return redirect(akey)
    
    
def newuser(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            non = form.cleaned_data.get('non')
            modpas = form.cleaned_data.get('modpas')
            modpas2 = form.cleaned_data.get('modpas2')

            if User.objects.filter(username=non).exists():
                error_message = 'Ce nom d\'utilisateur est déjà utilisé.'
                context = {
                    'form': form,
                    'error_message': error_message
                }
                return render(request, 'newuser.html', context)

            user = User.objects.create_user(username=non, password=modpas)
            user.save()
            return redirect(akey)
        else:
            print('Le formulaire contient des erreurs')
    else:
        form = NewUserForm()
    context = {
        'form': form
    }
    return render(request, 'newuser.html', context)


def index(request):
    konekte = request.user.is_authenticated
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input:
        contacts = Contact.objects.filter(full_name__icontains=search_input)
    else:
        contacts = Contact.objects.all()
        search_input = ''
    return render(request, 'index.html', {'contacts': contacts, 'search_input': search_input, 'konekte': konekte})

@login_required
def addContact(request):
        if request.method == 'POST':
            user = request.user
            full_name = request.POST['fullname']
            email = request.POST['email']
            phone_number = request.POST['phone-number']
            
            if Contact.objects.filter(Q(full_name=full_name) | Q(email=email) | Q(phone_number=phone_number)).exists():
                error_message = 'Ce contact existe déjà.'
                context = {
                    'error_message': error_message
                }
                return render(request, 'new.html', context)

            new_contact = Contact(
                user=user,
                full_name=full_name,
                relationship=request.POST['relationship'],
                email=email,
                phone_number=phone_number,
                address=request.POST['address'],
            )
            new_contact.save()
            return redirect('/')

        return render(request, 'new.html')
 
    

@login_required
def editContact(request, pk):
    contact = Contact.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            contact.full_name = request.POST['fullname']
            contact.relationship = request.POST['relationship']
            contact.email = request.POST['email']
            contact.phone_number = request.POST['phone-number']
            contact.address = request.POST['address']
            contact.save()
            return redirect('/profile/' + str(contact.id))
        return render(request, 'edit.html', {'contact': contact})
    else:
        return redirect('konekte')
    
    
@login_required
def deleteContact(request, pk):
    contact = Contact.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            contact.delete()
            return redirect('/')
        return render(request, 'delete.html', {'contact': contact})
    else:
        return redirect('konekte')

def contactProfile(request, pk):
    contact = Contact.objects.get(id=pk)
    return render(request, 'contact-profile.html', {'contact': contact})
