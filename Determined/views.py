from itertools import chain
import sqlite3

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from Determined.forms import UserLoginForm, UserCreation
from data.graphs import (university_swp, course_selection, course_graphs,
    university_instructors, instructor_selection, instructor_graphs,
    get_course_instructors, get_instructor_courses)
from data.course import (get_all_courses, filter_course_term, check_course_pk,
    verify_course_table, update_courses,course_difference, delete_course)
from data.student import (swp_dropdowns, filter_swp_data, swp_redirect,
    verify_swp_table, update_students, check_student_product_sync, sync_students)
from users.models import User

def home(request):
    """Login funcationality for homepage

    Args:
        request ([django request]): Defualt request from django

    Returns:
        [render]: returns a render of the page
    """
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, "The email or password is invalid")
        elif not user.is_active:
            messages.error(request, "Sorry, your account is awaiting activation. Please await your activaiton email.")
        else: 
            login(request, user)
            return redirect('../dashboard/')
        return render(request, "login.html", context={"form":UserLoginForm()})
    else:
        if request.user.is_authenticated: 
            return redirect('../dashboard/')
        else: 
            return render(request, "login.html", context={"form":UserLoginForm()})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('../login/')
    #Forcing view
    view = request.GET['view'] if 'view' in request.GET else None
    if view not in ['course', 'instructor']:return redirect('../dashboard/?view=course')
    if view == 'course':
        graph_html = university_swp()
        courses = course_selection()
        #Course selected
        if 'id' in request.GET:
            course_id = request.GET['id']
            course_name = [x['name'] for x in courses if x['id'] == int(course_id)][0]
            course_swp, course_pass_fail, course_swp_count, course_grade = course_graphs(course_id)
            course_instructors = get_course_instructors(course_id)
            context = {"select": course_name, "university_swp": graph_html, "courses": courses, "course_swp": course_swp,
                "course_pass_fail": course_pass_fail, "course_swp_count":course_swp_count, "course_grade":course_grade,
                "username": request.user.name, 'view': view, "course_instructors":course_instructors}
        #Course non selected
        else: 
            context = {"select": "Select Course", 'view': view, 
                "university_swp": graph_html, "courses": courses,
                "username": request.user.name}
    #Instructor View
    else:
        graph_html = university_instructors()
        instructors = instructor_selection()
        #Instructor selected
        if 'id' in request.GET:
            instructor_id = request.GET['id']
            #Making sure valid instructor
            if instructor_id not in [x['name'] for x in instructors]: 
                return redirect('../dashboard/?view=instructor')
            else: 
                instructor_fname, instructor_lname = instructor_id.split()
                inst_swp, inst_pass_fail, inst_swp_count, inst_grade = \
                    instructor_graphs(instructor_fname, instructor_lname)
                courses = get_instructor_courses(instructor_fname, instructor_lname)
                context = {"select": instructor_id, "university_swp": graph_html, 
                    "courses": instructors, "course_swp": inst_swp,"course_pass_fail": inst_pass_fail,
                    "course_swp_count":inst_swp_count,"course_grade":inst_grade,
                    "username": request.user.name, 'view': view, "instructor_courses":courses}

        #Instructor non selected
        else: 
            context = {"select": "Select Instructor", 'view': view, "university_swp": graph_html,
            "courses": instructors, "username": request.user.name}
    return render(request, "dashboard.html", context=context)

def register(request):
    """Funcitionality for registration page

    Args:
        request ([django request]): Defualt request from django

    Returns:
        [render]: returns a render of the page
    """
    if request.method=="POST":
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created! Allow up to 7 days for your registration to be confirmed.")
            return redirect('/')
        elif 'email' in form.errors:
            messages.error(request, form.errors['email'][0]) 
        else:
            errors = "\n".join(list(chain(*form.errors.values())))
            messages.error(request, f"Errors found: {errors}")
    return render(request, "register.html")

def approve_users(request):
    if not request.user.is_authenticated:
        return redirect('../login/')
    if not request.user.is_admin:
        return redirect('../dashboard/')
    #Getting user model to fill table 
    users = User.objects.all()
    if request.method=="GET":
        return render(request, "table.html", context={"users":users, "username": request.user.name})
    else:
        #Approving / Denying users
        for t, d in request.POST.items():
            if 'email' in t:
                u = User.objects.get(email=d.replace("/",""))
            elif 'approval' in t: 
                if d == '1': 
                    u.is_active=True
                    u.save(update_fields=['is_active'])
                    u.email_account_approval()
                else: 
                    u.email_account_deny()
                    u.delete()
        messages.success(request, "Success!")
        return render(request, "table.html", context={"users":users, "username": request.user.name})

def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('../login/') 
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('../login/')

def course_creation(request):
    if not request.user.is_authenticated:
        return redirect('../login/') 
    if not request.user.is_admin:
        return redirect('../dashboard/')
    # -- Modifiing Table --
    modify = True if 'modify' in request.GET or 'modify' in request.POST else False
    if modify:
        courses = get_all_courses()
        terms = [f"{x['term']} {x['year']}" for x in courses]
        terms = list(dict.fromkeys(terms))
        #Filtering by terms
        select_term_text = terms[0]
        term = request.GET['term'] if 'term' in request.GET else select_term_text
        if term != "All":
            courses = filter_course_term(courses, term)
        select_term_text = term
        context = {"courses":courses, "username": request.user.name, "modify":True, "terms":terms, "term_text":select_term_text }
    # -- Creating Table --
    else: 
        context = {"username": request.user.name, "modify":False}
    # -- Updating Database --
    if request.method == "POST":
        data = verify_course_table(request.POST)
        if modify:
            updated_rows, deleted_rows, original_rows = course_difference(courses, data)
            delete_course(deleted_rows)
            failed = update_courses(updated_rows, original_rows)
            if failed:
                dup = failed[0]
                messages.error(request, f"Course {dup[0]} during {dup[1]} {dup[2]} already exists!")
            else: 
                messages.success(request, "Courses have been updated!")
            context['courses'] = filter_course_term(get_all_courses(), term) if term != "All" else get_all_courses()
        #new course
        else: 
            failed_validation = check_course_pk(data)
            if failed_validation:
                dup = failed_validation[0]
                messages.error(request, f"Course {dup[0]} during {dup[1]} {dup[2]} already exists!")
            else:
                update_courses(data, None)
                messages.success(request, "Courses have been updated!")
        
    return render(request, "course.html", context=context)

def student_work(request):
    if not request.user.is_authenticated:
        return redirect('../login/') 
    #Force URL args
    if request.method =="GET" and not all(x in request.GET for x in ['dept', 'course', 'term', 'swp']):
        return redirect('../students/?dept=CPSC&course=3380 Operating Systems&term=Fall 2020&swp=Midterm')
    #Running sync then redirecting
    if all(x in request.GET for x in ['dept', 'course', 'term', 'swp', 'sync']):
        if request.GET['sync']:
            dept, course, term, swp = request.GET['dept'], request.GET['course'], request.GET['term'], request.GET['swp']
            sync_students(course, dept, term)
            messages.success(request, f"Students have been synced!")
            return redirect(f'../students/?dept={dept}&course={course}&term={term}&swp={swp}')
    #Checking if invalid url args -> redirecting
    dept, course, term, swp = request.GET['dept'], request.GET['course'], request.GET['term'], request.GET['swp']
    dropdowns = swp_dropdowns(dept, course, term, swp)
    redirect_url = swp_redirect(dept, course, term, swp, dropdowns)
    if redirect_url: return redirect(redirect_url)
    table_data = filter_swp_data(dept, course, term, swp)
    #Post
    if request.method=="POST":
        data = verify_swp_table(request.POST)
        failed = update_students(data, table_data)
        if not failed: 
            dropdowns = swp_dropdowns(dept, course, term, swp)
            table_data = filter_swp_data(dept, course, term, swp)
            messages.success(request, "Student work products have been updated!")
        else: 
            messages.error(request, f"Course {failed[3]}-{failed[2]} does not exist for {failed[8]} {failed[9]}. Please create the course first")
    #Page render
    student_sync = check_student_product_sync(course, dept, term)
    dropdown_title = {'dept':dept, 'course':course, 'term':term, 'swp':swp}
    context = {'table_data':table_data, 'dropdown':dropdowns, 'drop_title':dropdown_title, "username": request.user.name, "student_sync": student_sync}
    return render(request, "student.html", context=context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('../login/')
    if request.method == "POST":
        user = request.user
        user.name = request.POST['username'] if request.POST['username'] else user.name
        user.email = request.POST['email'].strip() if request.POST['email'] else user.email
        user.first_name = request.POST['first_name'].strip() if request.POST['first_name'] else user.first_name
        user.last_name = request.POST['last_name'].strip() if request.POST['last_name'] else user.last_name
        user.save()
        messages.success(request, "Your user profile has been updated!")
    return render(request, "profile.html", context={"username": request.user.name}) 
    
