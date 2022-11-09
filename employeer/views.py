from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from home.models import Leaves

# Create your views here.

@login_required(login_url='user_login')
def dashboard(request):
    
    users = Account.objects.all().order_by('-id')
    username = request.user
    context = {
        'employee': users,
        'username': username,
    }
    user = Account.objects.get(user=username)

    if user.is_admin:
        return render(request, 'dashboard.html', context)
    else:
        messages.success(request, "Only admin can visit the admin dashboard")
        return redirect('/')


@login_required(login_url='user_login')
def requests(request):
    leaves = Leaves.objects.all().order_by('-id')
    return render(request, 'requests.html', {'username':request.user, 'leaves':leaves})


@login_required(login_url='user_login')
def new_employee(request):
    try:
        if request.method == "POST":
            username = request.POST['name']
            designation = request.POST['designation']
            email = request.POST['email']
            password = request.POST['password']
            is_admin = request.POST.get('is_admin')

            if is_admin:
                is_admin = True
            else:
                is_admin = False

            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            user_obj = Account.objects.create(user=myuser)
            user_obj.user = myuser
            user_obj.designation = designation
            user_obj.is_admin = is_admin
            user_obj.save()

            messages.success(request, "New employee has been created")
            
            return render(request, 'new_employee.html', {'username':request.user})
        else:
            return render(request, 'new_employee.html',{'username':request.user})
    except:
        messages.error(request, "Something went wrong please try again")
        return render(request, 'new_employee.html')


@login_required(login_url='user_login')
def approve_leave(request, leave_id):
    leave_obj = Leaves.objects.get(id=leave_id)
    leave_obj.status = 'approved'
    leave_obj.save()
    return redirect('requests')


@login_required(login_url='user_login')
def reject_leave(request, leave_id):
    leave_obj = Leaves.objects.get(id=leave_id)
    leave_obj.status = 'rejected'
    leave_obj.save()

    total_applied_leaves = leave_obj.applied_leaves
    user_obj = Account.objects.get(user=request.user)
    leaves = user_obj.leaves + total_applied_leaves
    user_obj.leaves = leaves
    user_obj.save()

    return redirect('requests')