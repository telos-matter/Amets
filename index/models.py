from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, unique= True)
    profile_points = models.IntegerField(default= 0)

    class ProfileAvatar (models.TextChoices):
        AVATAR_0 = 'index/images/avatars/avatar_0.png'
        AVATAR_1 = 'index/images/avatars/avatar_1.png'
        AVATAR_2 = 'index/images/avatars/avatar_2.png'
        AVATAR_3 = 'index/images/avatars/avatar_3.png'
        AVATAR_4 = 'index/images/avatars/avatar_4.png'
        AVATAR_5 = 'index/images/avatars/avatar_5.png'
        AVATAR_6 = 'index/images/avatars/avatar_6.png'
        AVATAR_7 = 'index/images/avatars/avatar_7.png'
        AVATAR_8 = 'index/images/avatars/avatar_8.png'
        AVATAR_9 = 'index/images/avatars/avatar_9.png'
        AVATAR_10 = 'index/images/avatars/avatar_10.png'
        AVATAR_11 = 'index/images/avatars/avatar_11.png'
    profile_avatar = models.CharField (max_length= 255, choices= ProfileAvatar.choices, default= ProfileAvatar.AVATAR_0)

    def changePasswordOrError(self, old, new):
        if self.user.check_password(old):
            error = Profile.validatePassword(new)
            if error is None:
                self.user.set_password(new)
                self.user.save()
                self.save()
                return None
            else:
                return error
        else:
            return 'Current password is incorrect.'

    def selectAvatar (self, avatar_order):
        #I know this doesnt change the avatar it self just the link but hey, once again 0 time
        self.profile_avatar = self.ProfileAvatar.AVATAR_0.replace('0', str(avatar_order))
        self.save()

    def passedExam (self):
        self.profile_points += 100
        self.save()

    def liked(self):
        self.profile_points += 10
        self.save()

    def disliked(self):
        self.profile_points -= 5
        self.save()

    def answered(self):
        self.profile_points += 50
        self.save()

    @classmethod
    def create (cls, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()
            
        profile = Profile(user= user)
        profile.save()

        return profile

    @classmethod
    def getAvatarLinkList (cls):
        list = []
        for tuple in cls.ProfileAvatar.choices:
            list.append(tuple[0])
        return list

    @classmethod
    def validateUsername (cls, username):
        if len(username) == 0:
            return 'A username is required.'

        if len(username) < 3:
            return 'A username must be at least 3 characters long.'

        if '@' in username:
            return 'A username cannot contain the special character \'@\'.'

        try:
            User.objects.get(username= username)
            return 'This username is already taken!'
        except User.DoesNotExist:
            return None

    @classmethod
    def validateEmail (cls, email):
        if len(email) == 0:
            return 'An email is required.'

        tokens = email.split('@')

        if len(tokens) != 2 or len(tokens[0]) < 3 or not('.' in tokens[1]):
            return 'This is not a valid email.'

        try:
            User.objects.get(email= email)
            return 'This email is already taken!'
        except User.DoesNotExist:
            return None

    @classmethod
    def validatePassword (cls, password):
        if len(password) == 0:
            return 'A password is required.'

        if len(password) < 4:
            return 'A password must be at least 4 characters long.'

        return None

    def __str__(self):
        return str(self.user.username)


class Content (models.Model):
    content_text = models.TextField()

    def getTagList (self):
        tag_list = []
        for element in self.content_text.split():
            if element[0] == '#':
                tag_list.append(element.lower())
        
        return tag_list

    def hasTag (self, tag):
        return tag.lower() in self.getTagList()
    

class Post (models.Model):
    post_title = models.CharField(max_length= 255)
    post_content = models.ForeignKey(Content, on_delete= models.CASCADE)
    post_date = models.DateField(auto_now_add= True)
    post_poster = models.ForeignKey(Profile, on_delete= models.CASCADE)

    class PostType (models.TextChoices):
        THREAD = 'Thread'
        NEWS = 'News'        
    post_type = models.CharField (max_length= 8, choices= PostType.choices)

    class PostLanguage (models.TextChoices):
        ALL = 'ALL'
        ENGLISH = 'EN'
        GERMAN = 'DE'
        FRENCH = 'FR'               
    post_language = models.CharField (max_length= 3, choices= PostLanguage.choices, default= PostLanguage.ALL)

    @classmethod
    def create (cls, user, isThread, title, content):
        post_poster = Profile.objects.get(user= user)

        if isThread:
            post_type = cls.PostType.THREAD
            content += ' #Thread'
        else:
            post_type = cls.PostType.NEWS
            content += ' #News'

        post_content = Content(content_text = content)
        post_content.save()

        post = Post(post_title= title, post_content= post_content, post_poster= post_poster, post_type= post_type)
        post.save()

        if isThread:
            Thread.create(post)
        else:
            News.create(post)

        return post

    def getScore(self):
        return 1000 -((date.today() - self.post_date).days *100) +(Reaction.getPositiveCount(self) *75) -(Reaction.getNegativeCount(self) *25)

    def isPostedWithin(self, f_date, s_date):
        def createDate (str):
            return date(year= int(str[0:4]), month= int(str[5:7]), day= int(str[8:10]))
        f_date = createDate(f_date)
        s_date = createDate(s_date)
        return self.post_date >= f_date and self.post_date <= s_date

    def isPostValid(self, type, t_state, n_state):
        if type == 'both':
            return self.getPost().isPostValid(t_state, n_state)
        elif type == 'thread':
            if self.isThread():
                return self.getPost().isPostValid(t_state, n_state)
            else:
                return False
        elif type == 'news':
            if self.isNews():
                return self.getPost().isPostValid(t_state, n_state)
            else:
                return False
        else:
            return False

    def getTypeLabel(self):
        for tuple in self.PostType.choices:
            if self.post_type == tuple[0]:
                return tuple[1].upper().replace(' ', '_')

    def isThread(self):
        return self.post_type == self.PostType.THREAD

    def isNews(self):
        return self.post_type == self.PostType.NEWS

    def isPostedBy(self, poster):
        return self.post_poster.user.username == poster[1:]

    def hasTitle(self, title):
        return title.lower() in self.post_title.lower()

    def getPost(self):
        if self.isThread():
            return self.thread
        else:
            return self.news

    def getState(self):
        return self.getPost().post_state

    def getStateLabel(self):
        state = self.getState()
        for tuple in self.getPost().PostState.choices:
            if state == tuple[0]:
                return tuple[1].upper().replace(' ', '_')

    def getDisplayedContent(self):
        content = self.post_content.content_text
        if len(content) > 500:
            return content[:500] +'..'
        else:
            return content

    @classmethod
    def validateTitle (cls, title):
        if title == 'Your post title..':
            return 'Type a title for you post.'

        if len(title) == 0:
            return 'A title is required.'

        if len(title) < 3:
            return 'A title must be at least 3 characters long.'

        return None

    @classmethod
    def validateContent (cls, content):
        if content == 'Your post content. It can include #tags that help find it, by default, your post type tag is included..':
            return 'Type out the content for you post.'    

        if len(content) == 0:
            return 'A content is required.'

        return None

    @classmethod
    def getQuery(cls):
        query = []
        for post in Post.objects.all():
            if post.isNews() and not post.getPost().news_verified and not post.getPost().news_old:
                continue
            query.append(post)
        
        def key (element):
            return element.getScore()
        query.sort(reverse= True, key= key)

        return query

    @classmethod
    def getQuerySearch (cls, q):
        title_list=[]
        tag_list=[]
        poster_list=[]
        for element in q.split():
            if element[0] == '@':
                poster_list.append(element)
            elif element [0] == '#':
                tag_list.append(element)
            else:
                title_list.append(element)

        query = []
        for post in Post.getQuery():
            isValid = True

            for title in title_list:
                if not post.hasTitle(title):
                    isValid = False
                    break
                
            if isValid:
                for tag in tag_list:
                    if not post.post_content.hasTag(tag):
                        isValid = False
                        break

            if isValid:
                for poster in poster_list:
                    if not post.isPostedBy(poster):
                        isValid = False
                        break

            if isValid:
                query.append(post)

        return query

    @classmethod
    def getQueryFilter (cls, q, f_date, s_date, by, order, type, t_state, n_state):
        query = cls.getQuerySearch(q)

        for post in query[:]:
            if not post.isPostedWithin(f_date, s_date):
                query.remove(post)
                continue

            if not post.isPostValid(type, t_state, n_state):
                query.remove(post)
                continue

        if by == 'date':
            def key (element):
                return (date(year= 2020, month=1, day=1) - element.post_date).days
            query.sort(key= key)

        if order == 'inc':
            query.reverse()

        return query

    def __str__(self):
        return str(self.post_type) +': ' +str(self.post_title)
    

class Thread (models.Model):
    post = models.OneToOneField(Post, on_delete= models.CASCADE, unique= True)

    class PostState (models.TextChoices):
        NOT_ANSWERED = 'Open'      
        ANSWERED = 'Answered'            
    post_state = models.CharField (max_length= 12, choices= PostState.choices, default= PostState.NOT_ANSWERED)

    def answered (self):
        self.post_state = self.PostState.ANSWERED
        self.save()

    def isPostValid(self, t_state, n_state):
        if t_state == 'both':
            return True
        elif t_state == 'open':
            return self.post_state == self.PostState.NOT_ANSWERED
        elif t_state == 'answered':
            return self.post_state == self.PostState.ANSWERED
        else:
            return False

    @classmethod
    def create (cls, post):
        thread = Thread(post= post)
        thread.save()
        return thread

    @classmethod
    def isAnswered (cls, post):
        if post.isThread():
            return post.getPost().post_state == cls.PostState.ANSWERED         
        else:
            return False

    def __str__(self):
        return str(self.post.post_title) +' : ' +str(self.post_state)


class News (models.Model):
    post = models.OneToOneField(Post, on_delete= models.CASCADE, unique= True)
    news_verified = models.BooleanField(default= False)
    news_old = models.BooleanField(default= False) 

    class PostState (models.TextChoices):
        WILL_HAPPEN = 'Yet to happen'      
        HAPPENING = 'Happening today'   
        HAPPENED = 'Already happened'            
    post_state = models.CharField (max_length= 24, choices= PostState.choices, default= PostState.WILL_HAPPEN)

    def isPostValid(self, t_state, n_state):
        if n_state == 'all':
            return True
        elif n_state == 'yet_to_happen':
            return self.post_state == self.PostState.WILL_HAPPEN
        elif n_state == 'happening_today':
            return self.post_state == self.PostState.HAPPENING
        elif n_state == 'already_happened':
            return self.post_state == self.PostState.HAPPENED
        else:
            return False

    @classmethod
    def create (cls, post):
        news = News(post= post)
        news.save()
        return news

    def __str__(self):
        return str(self.post.post_title) +': ' +str(self.post_state)


class Reaction (models.Model):
    reaction_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reaction_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class ReactionType (models.TextChoices):
        POSITIVE = 'POS'
        NEGATIVE = 'NEG'        
    reaction_type = models.CharField (max_length= 3, choices= ReactionType.choices)

    class Meta:
        unique_together = ['reaction_profile', 'reaction_post']

    @classmethod
    def create (cls, profile, post, isPositive):
        if isPositive:
            reaction = Reaction(reaction_profile= profile, reaction_post= post, reaction_type= cls.ReactionType.POSITIVE)
            post.post_poster.liked()
        else:            
            reaction = Reaction(reaction_profile= profile, reaction_post= post, reaction_type= cls.ReactionType.NEGATIVE)
            post.post_poster.disliked()
        reaction.save()
        return reaction

    @classmethod
    def like (cls, user, post_id):
        profile = Profile.objects.get(user= user)
        post = Post.objects.get(id= post_id)

        try:
            Reaction.objects.get(reaction_profile= profile, reaction_post= post).delete()
        except Reaction.DoesNotExist:
            cls.create(profile, post, True)

    @classmethod
    def dislike (cls, user, post_id):
        profile = Profile.objects.get(user= user)
        post = Post.objects.get(id= post_id)

        try:
            Reaction.objects.get(reaction_profile= profile, reaction_post= post).delete()
        except Reaction.DoesNotExist:
            cls.create(profile, post, False)

    @classmethod
    def getPositiveCount (cls, post):
        return len(Reaction.objects.all().filter(reaction_post= post).filter(reaction_type= cls.ReactionType.POSITIVE))
    
    @classmethod
    def getNegativeCount (cls, post):
        return len(Reaction.objects.all().filter(reaction_post= post).filter(reaction_type= cls.ReactionType.NEGATIVE))

    @classmethod
    def getProfileReaction (cls, user, post):
        reactions = Reaction.objects.all().filter(reaction_profile= Profile.objects.get(user= user)).filter(reaction_post= post)
        if len(reactions) == 0:
            return 0
        elif reactions[0].reaction_type == cls.ReactionType.POSITIVE:
            return 1
        else:
            return -1


class Reply (models.Model):
    reply_post = models.ForeignKey(Post, on_delete= models.CASCADE)
    reply_poster = models.ForeignKey(Profile, on_delete= models.CASCADE)
    reply_content = models.ForeignKey(Content, on_delete= models.CASCADE)
    reply_date = models.DateField(auto_now_add= True)
    reply_selected = models.BooleanField(default= False)

    @classmethod
    def create (cls, user, post, content):
        reply_content = Content(content_text= content)
        reply_content.save()
        Reply(reply_post= post, reply_poster= Profile.objects.get(user= user), reply_content= reply_content,).save()

    @classmethod
    def getRepliesForPost (cls, post):
        return Reply.objects.filter(reply_post= post)

    @classmethod
    def select (cls, reply_id):
        reply = Reply.objects.get(id= reply_id)
        if reply.reply_post.isThread():
            reply.reply_selected = True
            reply.save()
            reply.reply_post.getPost().answered()
            reply.reply_poster.answered()
            

class Document (models.Model):
    class DocumentType (models.TextChoices):
        AUDIO = 'AUD'
        IMAGE = 'IMG'        
    document_type = models.CharField (max_length= 3, choices= DocumentType.choices)

    def upload_to (instance, filename):
        if ('.png' in filename) or ('.jpg' in filename):
            return 'index/static/index/documents/images/' +filename
        else:
            return 'index/static/index/documents/audios/' +filename
    document_file = models.FileField (upload_to= upload_to)

    def getPath (self):
        path = self.document_file.path
        return path[path.find('index/documents/'):]

    def isAudio (self):
        return self.document_type == self.DocumentType.AUDIO

    def __str__(self):
        return str(self.document_file.name)


class Question (models.Model):
    question_statement = models.TextField()
    question_documents = models.ManyToManyField(Document, blank= True)
    question_answers = models.CharField (max_length= 255)

    class QuestionType (models.TextChoices):
        INPUT = 'INP'
        TRUE_FALSE = 'TOF'        
        ONE_CHOICE = 'OIM'
    question_type = models.CharField (max_length= 3, choices= QuestionType.choices)

    def evaluate (self, answers):
        if self.question_type == self.QuestionType.INPUT:

            correct_answers = 0
            for index, value in enumerate(self.getAnswers()):
                if value == answers[index]:
                    correct_answers += 1
            
            return (correct_answers, len(self.getAnswers()), self.getAnswers())
                
        elif self.question_type == self.QuestionType.TRUE_FALSE:

            return ((1 if answers == self.question_answers else 0), 1, self.question_answers)

        elif self.question_type == self.QuestionType.ONE_CHOICE:

            return ((1 if answers == self.question_answers else 0), 1, self.question_answers)

    def getStatementAsList (self):
        list = []

        holder = []
        for element in self.question_statement.split():
            if element == '~' or element == '*':
                list.append(' ' +' '.join(holder) +' ')
                holder = []
                list.append(element)
            else:
                holder.append(element)

        if len(holder) != 0:
            list.append(' ' +' '.join(holder))

        return list

    def getAnswers (self):
        answers = []
        for answer in self.question_answers.split():
            if answer == '^':
                answers.append('')
            else:
                answers.append(answer)
        return answers

    def getAnswersIndexes (self):
        indexes = []
        for index, element in enumerate(self.getStatementAsList()):
            if element == '~':
                indexes.append((index +1))
        
        return indexes

    def __str__(self):
        return str(self.id) +': ' +str(self.question_type)


class Exercise (models.Model):
    exercise_title = models.CharField(max_length=255)
    exercise_statement = models.TextField()
    exercise_options = models.CharField (max_length= 255, blank= True) 
    exercise_documents = models.ManyToManyField(Document, blank= True)
    exercise_questions = models.ManyToManyField(Question)

    class ExerciseLevel (models.TextChoices):
        A1 = 'A1'
        A2 = 'A2' 
        B1 = 'B1'
        B2 = 'B2' 
        C1 = 'C1'       
    exercise_level = models.CharField (max_length= 2, choices= ExerciseLevel.choices)

    def doMagic (self, request, context):
        if self.getType() == Question.QuestionType.INPUT:

            user_answers = []
            questions_answers = []
            correct_answers = 0
            answers_count = 0

            for question in self.getQuestions():
                answers = []

                for index in question.getAnswersIndexes():
                    answers.append(request.POST[str(str(question.id) +'_' +str(index))])
                    
                evaluation = question.evaluate(answers)

                correct_answers += evaluation[0]
                answers_count += evaluation[1]
                questions_answers.append(evaluation[2])
                user_answers.append(answers)

            context['user_answers'] = user_answers
            context['questions_answers'] = questions_answers
            context['correct_answers'] = correct_answers
            context['answers_count'] = answers_count
                    
        elif self.getType() == Question.QuestionType.TRUE_FALSE:

            user_answers = []
            questions_answers = []
            correct_answers = 0
            answers_count = 0

            for question in self.getQuestions():

                answer = request.POST[str(question.id)]
                                       
                evaluation = question.evaluate(answer)

                correct_answers += evaluation[0]
                answers_count += evaluation[1]
                questions_answers.append(evaluation[2])
                user_answers.append(answer)
                    
            context['user_answers'] = user_answers
            context['questions_answers'] = questions_answers
            context['correct_answers'] = correct_answers
            context['answers_count'] = answers_count

        elif self.getType() == Question.QuestionType.ONE_CHOICE:

            user_answers = []
            questions_answers = []
            correct_answers = 0
            answers_count = 0

            for question in self.getQuestions():

                answer = request.POST[str(question.id)]

                for answer_index, value in enumerate(question.getAnswersIndexes()):
                    if str(value) == str(answer):
                        answer = str(answer_index +1)
                        break

                evaluation = question.evaluate(answer)

                correct_answers += evaluation[0]
                answers_count += evaluation[1]
                questions_answers.append(evaluation[2])
                user_answers.append(answer)
                    

            context['user_answers'] = user_answers
            context['questions_answers'] = questions_answers
            context['correct_answers'] = correct_answers
            context['answers_count'] = answers_count
   
    def getType (self):
        return self.exercise_questions.all()[0].question_type

    def hasOptions (self):
        return len(self.exercise_options) != 0

    def getQuestions (self):
        return self.exercise_questions.all()

    def getDocuments (self):
        return self.exercise_documents.all()

    @classmethod
    def getLvlExercises (cls, level):
        return Exercise.objects.all().filter(exercise_level= level)

    def __str__(self):
        return str(self.id) +': ' +str(self.exercise_level) +' ' +str(self.exercise_title)


class Exam (models.Model):
    exam_title = models.CharField(max_length=255)
    exam_exercises = models.ManyToManyField(Exercise)

    class ExamLevel (models.TextChoices):
        A1 = 'A1'
        A2 = 'A2' 
        B1 = 'B1'
        B2 = 'B2' 
        C1 = 'C1'       
    exam_level = models.CharField (max_length= 2, choices= ExamLevel.choices)

    def getExercisesList (self):
        return self.exam_exercises.all()

    @classmethod
    def getLvlExams (cls, level):
        return Exam.objects.all().filter(exam_level= level)

    def __str__(self):
        return str(self.id) +': ' +str(self.exam_level) +' ' +str(self.exam_title)


class Resource (models.Model):
    resource_title = models.CharField(max_length=255)

    def upload_to (instance, filename):
        return 'index/static/index/resources/' +filename
    resource_file = models.FileField (upload_to= upload_to)

    class ResourceType (models.TextChoices):
        H = 'History'
        T = 'Technology' 
        S = 'Science'
        N = 'Novel' 
        A = 'Article' 
        G = 'General'       
    resource_type = models.CharField (max_length= 24, choices= ResourceType.choices)

    @classmethod
    def getTypeResources (cls, type):
        return Resource.objects.all().filter(resource_type= type)
 
    def __str__(self):
        return str(self.resource_title)


class Report (models.Model):
    report_text = models.TextField()
    report_checked = models.BooleanField(default= False)
    
    @classmethod
    def create (cls, text):
        Report(report_text= text).save()
