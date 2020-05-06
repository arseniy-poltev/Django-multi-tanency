from itertools import chain

from django.shortcuts import render, redirect
from django.contrib import messages
from app_django.models import Admin, Employee
from app_django.forms import LoginForm, RegistrationForm
from app_django.forms import AddEmployeeForm, DeleteEmployeeForm
from app_django.forms import ModifyEmployeeForm
from dynamic_db_router import in_database

base_table = "default"
employee_db = "admindata"


@in_database(base_table)
def login(request):
    if 'username' in request.session:
        return redirect('logout')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password_hash']
            admin = Admin.objects.filter(username=un).first()
            if admin and admin.check_password(pw):
                request.session['username'] = un
                return redirect('menu')
            else:
                messages.error(request, 'Invalid user')
                return redirect('logout')
        else:
            messages.error(request, 'Invalid form data')
            return redirect('logout')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'title': 'Login', 'form': form})


@in_database(base_table)
def register(request):
    if 'username' in request.session:
        return redirect('logout')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            admin = Admin.objects.filter(username=un).first()
            if admin:
                messages.info(request, 'Admin already exists. Only one admin is allowed')
                return redirect('login')
            else:
                pw = form.cleaned_data['password_hash']
                pw2 = form.cleaned_data['password2']
                if pw != pw2:
                    messages.error(request, "Passwords don't match")
                    return redirect('register')
                else:
                    admin = Admin(username=un)
                    admin.set_password(pw)
                    admin.save()
                    messages.info(request, 'Admin added')
                    return redirect('login')
        else:
            messages.info(request, 'Invalid form')
            return redirect('login')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'title': 'Register', 'form': form})


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    request.session.flush()
    return redirect('login')


def menu(request):
    if 'username' in request.session:
        return render(request, 'menu.html', {'title': 'Menu'})
    else:
        return redirect('logout')


def add_employee(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = AddEmployeeForm(request.POST)
            if form.is_valid():
                n = form.cleaned_data['name']
                a = form.cleaned_data['age']
                e = form.cleaned_data['ed']
                r = form.cleaned_data['role']
                if r == 'customer':
                    add_db = 'customerdata'
                else:
                    add_db = 'admindata'
                with in_database(add_db, write=True):
                    emp = Employee(name=n, age=a, ed=e, role=r)
                    emp.save()
                    messages.info(request, 'Employee added')
                    return redirect('menu')
            else:
                messages.info(request, 'Invalid form')
                return redirect('logout')
        else:
            form = AddEmployeeForm()
            return render(request, 'add_employee.html', {'title': 'Add Employee', 'form': form})
    else:
        messages.error(request, 'Invalid user')
        return redirect('logout')


def delete_employee(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = DeleteEmployeeForm(request.POST)
            if form.is_valid():
                with in_database(employee_db, write=True):
                    id = int(form.cleaned_data['id'])
                    emp = Employee.objects.get(id=id)
                    emp.delete()
                    messages.info(request, 'Employee deleted')
                    return redirect('menu')
            else:
                messages.error(request, 'Invalid form')
                return redirect('menu')
        else:
            form = DeleteEmployeeForm()
            return render(request, 'delete_employee.html', {'title': 'Delete Employee', 'form': form})
    else:
        messages.error(request, 'Invalid user')
        return redirect('logout')


def modify_employee(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = ModifyEmployeeForm(request.POST)
            if form.is_valid():
                id = int(form.cleaned_data['id'])
                with in_database(employee_db, write=True):
                    emp = Employee.objects.get(id=id)
                    ed = form.cleaned_data.get('ed')
                    role = form.cleaned_data.get('role')
                    if ed: emp.ed = ed
                    if role: emp.role = role
                    emp.save()
                    messages.info(request, 'Employee modified')
                    return redirect('menu')
            else:
                messages.error(request, 'Invalid form')
                return redirect('menu')
        else:
            form = ModifyEmployeeForm()
            return render(request, 'modify_employee.html', {'title': 'Modify Employee', 'form': form})
    else:
        messages.error(request, 'Invalid user')
        return redirect('logout')


def display_employees(request):
    search_param = request.GET['s']
    if search_param == 'customer':
        emp_db = 'customerdata'
    else:
        emp_db = 'admindata'
    if 'username' in request.session:
        with in_database(emp_db):
            employees = Employee.objects.all()

            if employees:
                return render(request, 'display_employees.html',
                              {'title': 'Display Employees', 'employees': employees})
            else:
                return render(request, 'no_employees.html', {'title': 'No Employees'})
    else:
        messages.error(request, 'Invalid user')
        return redirect('logout')
