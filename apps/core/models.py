from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ProblemSet(models.Model):
    no = models.IntegerField(unique=True)
    description = models.CharField(max_length=100)

    @property
    def max_no(self):
        return self.problems.count()

    def __unicode__(self):
        return 'Set %s' % self.no


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    team_no = models.IntegerField(unique=True)
    progress_no = models.IntegerField(default=1)
    problem_set = models.ForeignKey(ProblemSet, null=True, blank=True)
    last_success = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return 'Team %s (Solved: %s)' % (self.team_no, self.progress_no)


class Problem(models.Model):
    no = models.IntegerField()
    title = models.CharField(max_length=300)
    text = models.TextField()
    answer = models.CharField(max_length=100)
    problem_set = models.ForeignKey(ProblemSet, related_name='problems')

    def __unicode__(self):
        return 'Problem %s of Set %s' % (self.problem_set, self.no)

    class Meta:
        unique_together = ('no', 'problem_set')


class AnswerLog(models.Model):
    user = models.ForeignKey(User, related_name='answer_logs')
    problem = models.ForeignKey(Problem)
    time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    answer = models.CharField(max_length=100)

    def __unicode__(self):
        return 'User %s: Trial for Problem %s as %s' % (self.user, self.problem, self.answer)
