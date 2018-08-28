from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator



#################   Already Built Module Imports   ################
from vision.main.models import Course
from vision.main.models import Branch


###################################################################


#####################  Working Modules Imports   ##################

###################################################################

SESSION_CHOICE = []
for i in range(2010, datetime.now().year + 6):
    str_year = str(i)
    SESSION_CHOICE.append((str_year, str_year +'-'+ str(i+1)))

SESSION_CHOICE = tuple(SESSION_CHOICE)


class SessionCourse(models.Model):
    course = models.ForeignKey(Course, related_name='course_sessions')
    session = models.CharField(_("Session"), max_length = 15, choices = SESSION_CHOICE)
    is_admission_still_open = models.BooleanField()

    

class CounsellingSchedule(models.Model):
    course = models.ForeignKey(Course, related_name='course_counselling')
    start_datetime = models.DateTimeField(auto_now_add = False, auto_now = False)
    end_datetime = models.DateTimeField(auto_now_add = False, auto_now = False)
    student_list = JSONField()

        

class StudentCounsellingChoice(models.Model):
    student = models.ForeignKey(User, related_name='counselling_choices')
    branch = models.ForeignKey(Branch, related_name='branch_choosed_by')
    choice = models.IntegerField(_("Choice"), validators = [MinValueValidator(1)])

