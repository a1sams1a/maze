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


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('no', 'problem_set', 'title', 'text', 'answer')


class ProblemSetAdmin(admin.ModelAdmin):
    class ProblemInline(admin.StackedInline):
        model = Problem

    list_display = ('no', 'description')
    inlines = (ProblemInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AnswerLog, AnswerLogAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
