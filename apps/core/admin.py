from django.contrib import admin
from django.contrib.auth import admin as uadmin
from django.contrib.auth.models import User
from apps.core.models import UserProfile, AnswerLog, Problem, ProblemSet


class UserAdmin(uadmin.UserAdmin):
    class UserProfileInline(admin.StackedInline):
        model = UserProfile
        can_delete = False

    def get_profile(self, obj):
        return UserProfile.objects.get(user=obj)

    def get_name(self, obj):
        return obj.last_name + ' ' + obj.first_name
    get_name.admin_order_field = 'last_name'
    get_name.short_description = 'Name'

    def get_team_no(self, obj):
        return self.get_profile(obj).team_no
    get_team_no.short_description = 'Team NO'

    def get_progress_no(self, obj):
        return self.get_profile(obj).progress_no
    get_progress_no.short_description = 'Progress NO'

    def get_problem_set(self, obj):
        return self.get_profile(obj).problem_set
    get_problem_set.short_description = 'Problem Set'

    list_display = ('username', 'get_name', 'get_team_no', 'get_progress_no', 'get_problem_set', 'is_staff')
    list_filter = ('is_staff', )
    inlines = (UserProfileInline, )


class AnswerLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'time', 'ip', 'answer')


class ProblemSetAdmin(admin.ModelAdmin):
    class ProblemInline(admin.StackedInline):
        model = Problem

    def make_defaults(modeladmin, request, queryset):
        temp = list(queryset)
        if len(temp) != 1:
            return
        temp = temp[0]

        for s in ProblemSet.objects.all():
            if s.no == temp.no:
                continue

            for p in s.problems.all():
                p.delete()

            problems = temp.problems
            for p in temp.problems.all():
                Problem(no=p.no, css=p.css, title=p.title,
                        text1=p.text1, text2=p.text2,
                        image1=p.image1, image2=p.image2,
                        answer=p.answer, problem_set=s).save()

    make_defaults.short_description = "Change All Other ProblemSet to This Problem Set"

    list_display = ('no', 'description')
    inlines = (ProblemInline, )
    actions = [make_defaults, ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AnswerLog, AnswerLogAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
