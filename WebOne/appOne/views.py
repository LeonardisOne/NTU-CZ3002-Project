from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .utilities import create_teams

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
# below is deprecated
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

import firebase_admin
from firebase_admin import auth, credentials, db

cred = credentials.Certificate("../cz3002-firebase-adminsdk-zn2kj-457d20ac3e.json")
firechat_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://cz3002.firebaseio.com/'
})
room_ref = db.reference('room-metadata')

#make sure you have form name whenever you are dealing with form.
# Create your views here.
@login_required
def index(request):


    return render(request, 'appOne/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

"""this is decorator, to highlight that user_logout
   happens only user logged in alr"""
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()
            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'appOne/registration.html',
                    {'user_form':user_form,
                     'profile_form':profile_form,
                     'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)

                if user.groups.filter(name = 'Professors').exists():
                    return HttpResponseRedirect(reverse('appOne:prof_page'))

                elif user.groups.filter(name = 'Students').exists():
                    return HttpResponseRedirect(reverse('appOne:student_page'))

                return HttpResponseRedirect(reverse('index')) #back to home page

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'appOne/login.html',{})

@permission_required('appOne.add_module', raise_exception=True)
def add_module(request):
    if request.method == 'POST':
        form = AddModuleForm(request.POST)

        if form.is_valid():
            module = form.save(commit=False)
            module.save()
            print("Done")
            # return redirect('/appOne/prof')
            return redirect('/appOne/prof')
    else:
        form = AddModuleForm()

    context = {
        'form': form,
    }

    return render(request, 'appOne/addmodule.html', context)

@permission_required('appOne.add_chapter', raise_exception=True)
def add_chapter(request, pk):
    module_stored = get_object_or_404(Module, module_name=pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        if request.method == 'POST':
            form = AddChapterForm(request.POST)

            if form.is_valid():
                chapter = form.save(commit=False)
                chapter.module = module_stored
                chapter.save()

                # return HttpResponseRedirect(reverse('index'))
                # return redirect(f'/appOne/modules/{pk}/manage_chapter/')
                return redirect('/appOne/prof')
        else:
            form = AddChapterForm()

        context = {
            'form': form,
            'module': module_stored
        }
        return render(request, 'appOne/addchapter.html', context)
    else:
        raise Http404(u"Access Denied")


@permission_required('appOne.add_question', raise_exception=True)
def add_question(request, pk, pq):
    module_stored = get_object_or_404(Module, module_name=pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        chapter_stored = get_object_or_404(Chapter, module = module_stored, chapter_name=pq)
        if request.method == 'POST':
            form = AddQuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.chapter = chapter_stored
                question.save()
                print(question.pk)
                # return HttpResponseRedirect(reverse('index'))
                return redirect(f'/appOne/modules/{pk}/chapters/{pq}/manage_question/')

        else:
            form = AddQuestionForm()

        context = {
            'form': form,
            'chapter': chapter_stored
        }

        return render(request, 'appOne/addquestion.html', context)
    else:
        raise Http404(u"Access Denied")

@permission_required('appOne.add_solution', raise_exception=True)
def add_solution(request, m_name, ch_name, q_num):
    module_stored = get_object_or_404(Module, module_name=m_name)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        chapter_stored = get_object_or_404(Chapter, module = module_stored, chapter_name=ch_name)
        question_stored = get_object_or_404(Question, chapter=chapter_stored, question_number=q_num)
        if request.method == 'POST':
            form = AddSolutionForm(request.POST)

            if form.is_valid():
                solution = form.save(commit=False)
                solution.question = question_stored
                solution.save()
                return redirect(f'/appOne/modules/{m_name}/chapters/{ch_name}/manage_question/')

        else:
            form = AddSolutionForm()

        context = {
            'form': form,
            'question': question_stored
        }

        return render(request, 'appOne/addsolution.html', context)
    else:
        raise Http404(u"Access Denied")

@permission_required('appOne.delete_module', raise_exception=True)
def delete_module(request, module_pk):
    module_stored = Module.objects.get(module_name=module_pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        module_stored.delete()

        return redirect('/appOne/prof/')
    else:
        raise Http404(u"Access Denied")


@permission_required('appOne.delete_chapter', raise_exception=True)
def delete_chapter(request, module_pk, chapter_name):
    print(module_pk)
    print(chapter_name)

    module_stored = get_object_or_404(Module, module_name=module_pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        chapter_stored = Chapter.objects.get(module=module_stored, chapter_name=chapter_name)

        print(chapter_stored)
        chapter_stored.delete()
        # return render(request, 'appOne/delete_chapter.html')
        # return redirect(f'/appOne/modules/{module_pk}/manage_chapter/')
        return redirect('/appOne/prof/')
    else:
        raise Http404(u"Access Denied")

@permission_required('appOne.delete_question', raise_exception=True)
def delete_question(request, module_pk, chapter_name, question_name):
    print(module_pk)
    print(chapter_name)

    module_stored = get_object_or_404(Module, module_name=module_pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        chapter_stored = get_object_or_404(Chapter, chapter_name=chapter_name)
        question_stored = Question.objects.get(question_name=question_name)
        question_stored.delete()

        return redirect(f'/appOne/modules/{module_pk}/chapters/{chapter_name}/manage_question/')
    else:
        raise Http404(u"Access Denied")

@permission_required('appOne.change_module', raise_exception=True)
def manage_module(request):

    module_list = Module.objects.filter()
    return render(request,'appOne/manage_module.html',{'module_list':module_list})

@permission_required('appOne.change_chapter', raise_exception=True)
def manage_chapter(request, pk):
    module_stored = get_object_or_404(Module, module_name=pk)
    chapter_list = Chapter.objects.filter(module=module_stored)
    return render(request,'appOne/manage_chapter.html',{'module_pk': pk})

@permission_required('appOne.change_question', raise_exception=True)
def manage_question(request, pk, pq):
    module_stored = get_object_or_404(Module, module_name=pk)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=pq)
    question_list = Question.objects.filter(chapter=chapter_stored)
    return render(request, 'appOne/manage_question.html',{'module_pk': pk, 'chapter_name': pq, 'question_list': question_list})
# def view_module(request):
#     return render(request,'appOne/view_module.html',{})

@login_required
def prof_page(request):

    prof = Professor.objects.get(user=request.user)

    module_list = Module.objects.filter(coordinator=prof)

    chapters_all_mods = []
    for module in module_list:
        mod_chapters = Chapter.objects.filter(module=module)
        chapters_all_mods.append(mod_chapters)

    context = {
        'module_list': module_list,
        'chapters_all_mods': chapters_all_mods
    }

    return render(request,'appOne/prof.html', context)

@login_required
def student_page(request):
    student = Student.objects.get(user=request.user)
    modules_taken = student.modules_taken.all()
    chapters_all_mods = []
    for module in modules_taken:
        mod_chapters = Chapter.objects.filter(module=module)
        chapters_all_mods.append(mod_chapters)

    context = {
        'modules_taken': modules_taken,
        'chapters_all_mods': chapters_all_mods
    }

    return render(request,'appOne/student.html',context)

@permission_required('appOne.can_publish_chapter', raise_exception=True)
def publish_chapter(request, pk, pq):
    module_stored = get_object_or_404(Module, module_name=pk)
    prof = Professor.objects.get(user=request.user)
    if prof == module_stored.coordinator :
        chapter_published = get_object_or_404(Chapter, module=module_stored, chapter_name=pq)

        if request.method == 'POST':
            form = PublishChapterForm(request.POST)

            if form.is_valid():
                chapter_published.end_datetime = form.cleaned_data['end_datetime']
                print(chapter_published.end_datetime)#debug
                alr_started = chapter_published.can_start
                chapter_published.can_start = True
                chapter_published.save()

                team_list = create_teams(chapter_published, alr_started)

                for team in team_list:
                    new_room_ref = room_ref.push()
                    team.room_id = new_room_ref.key
                    team.save()

                    new_room_ref.set({
                        'name' : team.chapter.chapter_name + ' ' + team.team_name,
                        'type' : 'public'
                    })

                return HttpResponseRedirect(reverse('appOne:prof_page'))

        else:
            form = PublishChapterForm()

        context = {
            'form': form,
            'chapter': chapter_published
        }

        return render(request, 'appOne/publish.html', context)
    else:
        raise Http404(u"Access Denied")

#import json
""" def question_result(request, q_name, ch_name, m_name):
    module_stored = get_object_or_404(Module, module_name=m_name)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=ch_name)
    question_stored = get_object_or_404(Question, chapter=chapter_stored, question_name=q_name) """

@permission_required('appOne.can_try_qn', raise_exception=True)
def start_question(request, ch_name, m_name):
    module_stored = get_object_or_404(Module, module_name=m_name)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=ch_name)

    student = Student.objects.get(user=request.user)
    try:
        team = student.joined_teams.get(chapter=chapter_stored)
    except:
        raise Http404(u"Access Denied")

    qn_list = Question.objects.filter(chapter=chapter_stored)

    context = {
        'qn_list': qn_list,
        'ch_name': ch_name,
        'm_name': m_name
    }

    return render(request,'appOne/start_quiz.html', context)

@permission_required('appOne.can_try_qn', raise_exception=True)
def view_chapter_result(request, ch_name, m_name):
    module_stored = get_object_or_404(Module, module_name=m_name)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=ch_name)

    student = Student.objects.get(user=request.user)
    try:
        team = student.joined_teams.get(chapter=chapter_stored)
    except:
        raise Http404(u"Access Denied")

    total_tried = len(team.qn_tried)
    qn_list = Question.objects.filter(chapter=chapter_stored)
    if total_tried != len(qn_list): #can change to check less than/more than separately
        raise Http404(u"Your team has not completed all questions!")

    qn_sol_list = []
    for question in qn_list:
        qn_sol = [question]
        solution = Solution.objects.get(question=question)
        qn_sol.append(solution)
        qn_sol_list.append(qn_sol)

    score = 0
    for index, ans in enumerate(team.qn_results):
        if ans == '1':
            score += 1
            qn_sol_list[index].append("Correct")
        else:
            qn_sol_list[index].append("Wrong")

    percent_score = format((score/total_tried)*100, '.1f')

    context = {
        'qn_sol_list': qn_sol_list,
        'score': score,
        'total_tried': total_tried,
        'percent_score': percent_score,
    }

    return render(request,'appOne/quiz_results.html', context)

@permission_required('appOne.can_try_qn', raise_exception=True)
def view_question(request, q_num, ch_name, m_name):
    module_stored = get_object_or_404(Module, module_name=m_name)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=ch_name)
    question_stored = get_object_or_404(Question, chapter=chapter_stored, question_number=q_num)

    student = Student.objects.get(user=request.user)
    try:
        team = student.joined_teams.get(chapter=chapter_stored)
    except:
        raise Http404(u"Access Denied")

    if len(team.qn_tried) + 1 < q_num :
        raise Http404(u"Please do questions in order")
    elif len(team.qn_tried) + 1 > q_num :
        raise Http404(u"You already done this question")

    if request.method == 'POST':
        ans_return = request.POST.get('ans_return')
        print(ans_return)
        solution = get_object_or_404(Solution, question=question_stored)
        team.qn_tried = team.qn_tried + "1"

        if ans_return == solution.solution_answer :
            team.qn_results = team.qn_results + "1"
            print("Answer is Correct")

        else:
            team.qn_results = team.qn_results + "0"
            print("Answer is Wrong")

        print(team.qn_tried)
        print(team.qn_results)
        team.save()

        return HttpResponseRedirect(reverse('appOne:start_question', kwargs={'m_name': m_name,
                                        'ch_name': ch_name}))

    else:
        students = team.student_set.all()
        student_list = list(students)
        print(student_list) # debug

        index = student_list.index(student) # get the index of student....
        ordering = (index + q_num ) % 5
        haveQuestion = False

        optionStr = ""
        display_str = ""
        if (ordering == 0):
            haveQuestion = True
            display_str = question_stored.question_name

        elif (ordering == 1):
            display_str = question_stored.question_optionA
            optionStr = "OPTION A"

        elif (ordering==2):
            display_str = question_stored.question_optionB
            optionStr = "OPTION B"

        elif (ordering==3):
            display_str = question_stored.question_optionC
            optionStr = "OPTION C"

        elif(ordering == 4):
            display_str = question_stored.question_optionD
            optionStr = "OPTION D"

        else:
            print("error")

        context = {
            'display_str' : display_str,
            'haveQuestion' : haveQuestion,
            'optionStr' : optionStr,
        }

    return render(request, 'appOne/quiz.html', context)


@login_required
def chat(request, pk, pq):
    module_stored = get_object_or_404(Module, module_name=pk)
    chapter_stored = get_object_or_404(Chapter, module=module_stored, chapter_name=pq)

    uid = request.user.username
    try:
        auth.create_user(uid=uid)
        print("add user")
    except:
        print("Existing user")
    custom_token = (auth.create_custom_token(uid)).decode()

    student = Student.objects.get(user=request.user)
    team = student.joined_teams.get(chapter=chapter_stored)
    room_id = team.room_id

    context = {
        'custom_token': custom_token,
        'room_id': room_id
    }

    return render(request, 'appOne/chat.html', context)
