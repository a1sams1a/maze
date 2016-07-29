from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import UserProfile, ProblemSet


class Command(BaseCommand):
    help = 'Make initial users and problem sets'

    def handle(self, *args, **options):
        num_users = 31

        for i in range(1, num_users + 1):
            user = User.objects.create_user(username='team%02d' % i,
                                            first_name='Team %02d' % i,
                                            last_name='',
                                            email='team%02d@maze' % i,
                                            password='init')
            user.save()

            problem_set = ProblemSet(no=i, description='for Team %02d' % i)
            problem_set.save()

            profile = UserProfile(user=user, team_no=i, progress_no=1, problem_set=problem_set)
            profile.save()

