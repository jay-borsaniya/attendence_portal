from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Account
from .models import Leaves,Attendence
from datetime import datetime, timedelta

# Create your views here.

@login_required(login_url='user_login')
def index(request):
    user = request.user
    is_admin = Account.objects.get(user=user).is_admin
    leaves = Account.objects.get(user=user).leaves
    attendence = Attendence.objects.filter(user=request.user).order_by('-id')

    if attendence:
        last_entry = Attendence.objects.filter(user=request.user).order_by('-id')[0]
    else:
        last_entry = None

    today = datetime.today().strftime("%Y-%m-%d")

    if last_entry:
        if str(last_entry.date) == str(today):
            punched_in_today = True
            if last_entry.out_time:
                punched_in_out_today = True
            else:
                punched_in_out_today = False
        else:
            punched_in_today = False
            punched_in_out_today = False
    else:
        punched_in_today = False
        punched_in_out_today = False

    return render(request, 'index.html', {'username':user,'leaves':leaves,'is_admin':is_admin,'attendence':attendence,'punched_in_today':punched_in_today,'punched_in_out_today':punched_in_out_today})


def user_login(request):

    if request.method == "POST":
        data = request.POST
        name = data['name']
        pass1 = data['password']
        user = authenticate(username=name, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You are now loged in")
            return redirect('index')
        else:
            messages.error(request, "Something went wrong please try again")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


@login_required(login_url='user_login')
def apply_leave(request):

    if request.method == "POST":
        user = request.user
        leave_reason = request.POST['reason']
        leave_type = request.POST['leave_type']
        leave_from_date = request.POST['from_date']
        leave_to_date = request.POST['to_date']
        
        date_format = "%Y-%m-%d"
        a = datetime.strptime(str(leave_from_date), date_format)
        b = datetime.strptime(str(leave_to_date), date_format)

        if leave_type == 'Full Day':
            if a == b:
                total_applied_leaves = 1
            else:
                applied_leaves.days = b - a 
                total_applied_leaves = applied_leaves.days
                total_applied_leaves = total_applied_leaves + timedelta(days=1)
                total_applied_leaves = total_applied_leaves.days
                print(total_applied_leaves)
        else:
            applied_leaves.days = b - a
            total_applied_leaves = applied_leaves.days
            total_applied_leaves = total_applied_leaves + timedelta(days=1)
            total_applied_leaves = float(total_applied_leaves.days/2)
            print(total_applied_leaves)

        user_obj = Account.objects.get(user=user)

        if total_applied_leaves <= 0:
            messages.error(request, 'Invalid dates, Please enter valid dates')
            return render(request, 'apply_leave.html')
        elif total_applied_leaves > user_obj.leaves:
            messages.error(request, 'You dont have enough leaves')
            return render(request, 'apply_leave.html')

        leaves_obj = Leaves.objects.create(user=user)
        leaves_obj.save()
        leaves_obj.leave_reason = leave_reason
        leaves_obj.leave_type = leave_type
        leaves_obj.leave_from_date = leave_from_date
        leaves_obj.leave_to_date = leave_to_date
        leaves_obj.applied_leaves = total_applied_leaves
        leaves_obj.status = 'pending'
        leaves_obj.save()

        leaves = user_obj.leaves - total_applied_leaves
        user_obj.leaves = leaves
        user_obj.save()

        leaves = Leaves.objects.filter(user=user).order_by('-id')
        context = {
            'leaves':leaves,
        }
        messages.success(request, "Your leave has been applied")
        return render(request, 'applied_leaves.html',context)

    else:
        return render(request, 'apply_leave.html')


@login_required(login_url='user_login')
def applied_leaves(request):

    user = request.user
    leaves = Leaves.objects.filter(user=user).order_by('-id')

    if not leaves:
        messages.error(request, "You don't have any leave history")
        return render(request,'applied_leaves.html')
    else:
        return render(request,'applied_leaves.html',{'leaves':leaves})


@login_required(login_url='user_login')
def cancelled_leaves(request, leave_id):
    leave_obj = Leaves.objects.get(id=leave_id)
    leave_obj.status = 'cancelled'
    leave_obj.save()
    total_applied_leaves = leave_obj.applied_leaves
    user_obj = Account.objects.get(user=request.user)
    leaves = user_obj.leaves + total_applied_leaves
    user_obj.leaves = leaves
    user_obj.save()
    messages.success(request, "Your leave has been cancelled")
    return redirect('applied_leaves')


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out")
    return render(request, 'login.html')


@login_required(login_url='user_login')
def change_password(request):

    if request.method == "POST":
        data = request.POST
        new_password = data['password']
        confirm_password = data['confirm_password']
        user = Account.objects.get(user__exact=request.user.id)

        if new_password == confirm_password:
            user = User.objects.get(username=request.user)
            user.set_password(new_password)
            user.save()
            #auth.Logout(request)
            messages.success(request, "Password updated successfully, Please login again")
            return redirect('index')
        else:   
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    else:   
        return render(request, 'change_password.html')


@login_required(login_url='user_login')
def punch_in(request):

    if request.method == 'POST':
        in_time = datetime.now().strftime("%H:%M:%S")
        attendence = Attendence.objects.create(user=request.user)
        attendence.punch_in = True
        attendence.in_time = in_time
        attendence.save()
        return redirect('index')
    else:
        return redirect('index')


@login_required(login_url='user_login')
def punch_out(request):

    if request.method == 'POST':
        out_time = datetime.now().strftime("%H:%M:%S")
        attendence = Attendence.objects.get(user=request.user, punch_in = True)
        attendence.out_time = out_time
        in_time = attendence.in_time

        in_time = datetime.strptime(str(in_time), "%H:%M:%S")
        out_time = datetime.strptime(str(out_time), "%H:%M:%S")

        working_hours = out_time - in_time
        working_hours = working_hours
        
        print(working_hours)

        attendence.working_hour = working_hours
        attendence.punch_in = False
        attendence.save()
        return redirect('index')
    else:
        return redirect('index')
