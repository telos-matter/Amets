from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse as rev
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .models import Profile as Prfl #I dont know why, but there were some namespacing problems
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def home (request):
    context = {'user': request.user}
    return render(request, 'index/home.html', context)


def sign_in (request):
    logout(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(rev('index:home'))
        else:
            return render(request, 'index/sign_in.html', {'error_message': 'Incorrect identifiers'})

    else:
        return render(request, 'index/sign_in.html')


def sign_up (request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {}

        error_message = Prfl.validateUsername(username)
        if error_message is not None:
            context['username_error'] = error_message
            
        error_message = Prfl.validateEmail(email)
        if error_message is not None:
            context['email_error'] = error_message
            
        error_message = Prfl.validatePassword(password)
        if error_message is not None:
            context['password_error'] = error_message
 
        if len(context) > 0:
            context['username_value'] = username
            context['email_value'] = email
            context['password_value'] = password  

            return render(request, 'index/sign_up.html', context)
        else:
            profile = Prfl.create(username, email, password)

            logout(request)
            login(request, profile.user)

            return HttpResponseRedirect(rev('index:home'))
        
    else:
        return render(request, 'index/sign_up.html')


def sign_out (request):
    logout(request)
    return HttpResponseRedirect(rev('index:home'))


def exercises(request):
    context = {'user': request.user}

    context['A1_list'] = Exercise.getLvlExercises(Exercise.ExerciseLevel.A1)
    context['A2_list'] = Exercise.getLvlExercises(Exercise.ExerciseLevel.A2)
    context['B1_list'] = Exercise.getLvlExercises(Exercise.ExerciseLevel.B1)
    context['B2_list'] = Exercise.getLvlExercises(Exercise.ExerciseLevel.B2)
    context['C1_list'] = Exercise.getLvlExercises(Exercise.ExerciseLevel.C1)
    
    return render(request, 'index/exercises.html', context)


def exercise(request, exercise_id):
    context = {'user': request.user}

    exercise = Exercise.objects.get(id= exercise_id)
    context['exercise'] = exercise

    if request.method == 'POST':
        exercise.doMagic(request, context)

        context['evaluated'] = True
    
    return render(request, 'index/exercise.html', context)



def exams (request):
    context = {'user': request.user}

    context['A1_list'] = Exam.getLvlExams(Exam.ExamLevel.A1)
    context['A2_list'] = Exam.getLvlExams(Exam.ExamLevel.A2)
    context['B1_list'] = Exam.getLvlExams(Exam.ExamLevel.B1)
    context['B2_list'] = Exam.getLvlExams(Exam.ExamLevel.B2)
    context['C1_list'] = Exam.getLvlExams(Exam.ExamLevel.C1)
    
    return render(request, 'index/exams.html', context)


def exam(request, exam_id):
    context = {'user': request.user}

    exam = Exam.objects.get(id= exam_id)
    context['exam'] = exam

    list = exam.getExercisesList()

    if request.method == 'GET':

        context['current_exercise_index'] = 0
        context['correct_answers'] = 0
        context['answers_count'] = 0
        context['exercise'] = list[0]

        context['finished'] = False

    else:
        index = int(request.POST['current_exercise_index'])

        correct_answers = int(request.POST['correct_answers'])
        answers_count = int(request.POST['answers_count'])
    
        list[index].doMagic(request, context)

        correct_answers = correct_answers +context['correct_answers']
        answers_count = answers_count +context['answers_count']

        context['correct_answers'] = correct_answers
        context['answers_count'] = answers_count
    
        index += 1

        if index >= len(list):
            context['finished'] = True
            context['passed'] = True if correct_answers >= int((60/100)*answers_count) else False

            if context['passed']:
                request.user.profile.passedExam()
                pass

        else:
            context['finished'] = False
            context['current_exercise_index'] = index
            context['exercise'] = list[index]
             
    return render(request, 'index/exam.html', context)


def resources (request):
    context = {'user': request.user}

    context['H_list'] = Resource.getTypeResources(Resource.ResourceType.H)
    context['T_list'] = Resource.getTypeResources(Resource.ResourceType.T)
    context['S_list'] = Resource.getTypeResources(Resource.ResourceType.S)
    context['N_list'] = Resource.getTypeResources(Resource.ResourceType.N)
    context['A_list'] = Resource.getTypeResources(Resource.ResourceType.A)
    context['G_list'] = Resource.getTypeResources(Resource.ResourceType.G)
    
    return render(request, 'index/resources.html', context)


def download (request, resource_id):
    resource = Resource.objects.get(id= resource_id)
    
    file = open(resource.resource_file.path, 'rb').read()

    response = HttpResponse(file, content_type = "x-pdf")
    response['Content-Disposition'] = 'attachment; filename=%s' % str(resource.resource_title) +'.pdf'
    return response


def profile(request, user_username):

    context = {}

    profile = User.objects.get(username= user_username).profile

    context['profile'] = profile
    context['user'] = request.user

    context['profile_owner'] = False
    if request.user.is_authenticated and user_username == request.user.username:
        context['profile_owner'] = True

    context['avatar_list'] = Prfl.getAvatarLinkList()

    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        error = profile.changePasswordOrError (old, new)
        if error is None:
            context['post_message'] = 'Password changed successfully'
        else:
            context['error_message'] = error

    return render(request, 'index/profile.html', context)


def feed (request):

    def get_query():
        return Post.getQuery()

    context = {}

    if request.method == 'POST':  
        try:
            request.POST['type']
            isThread = True
        except MultiValueDictKeyError:
            isThread = False
        title = request.POST['title']
        content = request.POST['content']

        error_message = Post.validateTitle(title)
        if error_message is not None:
            context['error_message'] = error_message

        error_message = Post.validateContent(content)
        if error_message is not None:
            context['error_message'] = error_message
        
        if len(context) == 0:
            Post.create(request.user, isThread, title, content)
            
            if isThread:
                context['post_message'] = 'Your Thread has been posted successfully.' 
            else:
                context['submit_message'] = 'Your News was submit to be verified.'

        else:
            context['type_value'] = isThread
            context['title_value'] = title
            context['content_value'] = content
            
    context['user'] = request.user
    context['post_list'] = get_query()
        
    return render(request, 'index/feed.html', context)


def post (request, id):
    context = {}

    user = request.user
    context['user'] = user

    post = Post.objects.get(pk= id)
    context['post'] = post

    if request.user.is_authenticated:
        context['post_owner'] = post.isPostedBy(('@'+user.username))
        context['user_reaction'] = Reaction.getProfileReaction(user, post)
    else:
        context['post_owner'] = False

    context['positive_count'] = Reaction.getPositiveCount(post)
    context['negative_count'] = Reaction.getNegativeCount(post)

    if request.method == 'POST':
        Reply.create(user, post, request.POST['content'])

    context['reply_list'] = Reply.getRepliesForPost(post)

    context['answered'] = Thread.isAnswered(post)

    return render(request, 'index/post.html', context) 


def search(request):

    def getValueOrNone(key):
        try:
            return request.GET[key]
        except MultiValueDictKeyError:
            return None

    def get_query():
        q = request.GET['q']

        f_date = getValueOrNone('f_date')
        s_date = getValueOrNone('s_date')
        by = getValueOrNone('by')
        order = getValueOrNone('order')
        type = getValueOrNone('type')
        t_state = getValueOrNone('t_state')
        n_state = getValueOrNone('n_state')
        if f_date is not None and s_date is not None and by is not None and order is not None and type is not None and (t_state is not None or n_state is not None):
            return Post.getQueryFilter(q, f_date, s_date, by, order, type, t_state, n_state)
        else:
            return Post.getQuerySearch(q)
            
    context = {}

    context['user'] = request.user
    context['post_list'] = get_query()
    context['search_value'] = request.GET['q']

    return render(request, 'index/search.html', context)    


def selectAvatar (request, avatar_order):
    avatar_order -= 1
    Profile.objects.get(user= request.user).selectAvatar(avatar_order)
    return HttpResponseRedirect(rev('index:profile', kwargs={'user_username': request.user.username}))


def delete (request, post_id):
    Post.objects.get(pk= post_id).delete()
    return HttpResponseRedirect(rev('index:feed'))


def like (request, post_id):
    Reaction.like(request.user, post_id)
    return HttpResponseRedirect(rev('index:post', kwargs={'id': post_id}))


def dislike (request, post_id):
    Reaction.dislike(request.user, post_id)
    return HttpResponseRedirect(rev('index:post', kwargs={'id': post_id}))


def select (request, reply_id, post_id):
    Reply.select(reply_id)
    return HttpResponseRedirect(rev('index:post', kwargs={'id': post_id}))


def forgot (request):
    return render(request, 'index/forgot.html')   


def about (request):
    return render(request, 'index/about.html')


def contact_us (request):
    return render(request, 'index/contact_us.html')


def use_conditions (request):
    return render(request, 'index/use_conditions.html')


def report_bug (request):
    context = {}
    context['user'] = request.user

    if request.method == 'POST':
        content = request.POST['content']
        Report.create(content)
        context['post_message'] = 'The bug has been reported, thank you.'

    return render(request, 'index/report_bug.html', context)


def donation (request):
    return render(request, 'index/donation.html')