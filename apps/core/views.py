from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from apps.core.models import Problem, AnswerLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def main(request):
    profile = None
    if request.user and request.user.is_authenticated():
        profile = request.user.profile

    return render(request, 'main.html', {'profile': profile})


def login(request):
    if request.user and request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/core/')
        return render(request, 'login.html', {'fail': True})
    return render(request, 'login.html')


def logout(request):
    if not request.user or not request.user.is_authenticated():
        return redirect('/core/')

    auth.logout(request)
    return redirect('/core/')


@login_required(login_url='/core/login/')
def solve(request, no=-1):
    user = request.user
    if not user.profile or not user.profile.problem_set:
        return redirect('/core/')

    no = int(no)
    profile = user.profile
    if no < 1 or no > profile.progress_no:
        return redirect('/core/solve/%s' % (profile.progress_no))
    elif no > profile.problem_set.max_no:
        return render(request, 'complete.html', {'profile': profile})

    msg = 0
    problem = Problem.objects.filter(no=no, problem_set=profile.problem_set).first()
    if request.method == 'POST' and no == profile.progress_no:
        answer = request.POST.get('answer', '')

        ip = get_client_ip(request)
        log = AnswerLog(user=user, problem=problem, ip=ip, answer=answer)
        log.save()

        if answer == problem.answer:
            profile.progress_no += 1
            profile.last_success = timezone.now()
            profile.save()

            msg = 1
        else:
            msg = 2

    return render(request, 'solve.html',
                  {'no': no, 'profile': profile, 'problem': problem, 'msg': msg})
