from __future__ import unicode_literals


from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

#################   Already Built Module Imports   ################

###################################################################


#####################  Working Modules Imports   ##################
from vision.generic_models import Name

###################################################################


FATHERS_OCCUPATION_CHOICES = (
    ('1', 'Service', ),
    ('2', 'Business', ),
    ('3', 'None', ),
    ('4', 'Gov Job', ),
)

MOTHERS_OCCUPATION_CHOICES = (
    ('1', 'Service', ),
    ('2', 'Business', ),
    ('3', 'None', ),
    ('4', 'Gov Job', ),
    ('5', 'Housewife', ),
)


RELIGION_CHOICES = (
    ('1', 'Hindu', ),
    ('2', 'Muslim', ),
    ('3', 'Sikh', ),
    ('4', 'Christian', ),
)

NATIONALITY_CHOICES = (
    ('1', 'Indian', ),
    ('2', 'Others', ),
)

YEAR_CHOICES = []
for i in range(1990, datetime.now().year):
    str_year = str(i)
    YEAR_CHOICES.append((str_year, str_year))

YEAR_CHOICES = tuple(YEAR_CHOICES)


EDUCATION_RESULT_CHOICE = (
    ('1', 'Pass', ),
    ('2', 'Fail', ),
)


class Country(Name):
    pass

class State(Name):
    country = models.ForeignKey(Country, related_name = 'states')


class District(Name):
    state = models.ForeignKey(State, related_name = 'districts')


class Address(models.Model):
    """
        This model will contains correspondence 
        and permanant address of student
    """
    address_line_1 = models.CharField(_("Address Line 1"), max_length = 200, blank = False, null = False)
    address_line_2 = models.CharField(_("Address Line 2"), max_length = 200, blank = True, null = True)
    pin = models.CharField(_("Pin Code"), max_length = 10, blank = False, null = False)
    district = models.ForeignKey(District, related_name = 'students_addresses')



class GeneralInfo(models.Model):
    """
        This table will contain general info user 
        like fahter's name, mother's name, religion, nationality,
        father's occupation etc
    """
    student = models.OneToOneField(User, related_name = 'general_info') 
    fathers_name = models.CharField(_("Father's Name"), max_length = 200, blank = False, null = False)
    mothers_name = models.CharField(_("Mother's Name"), max_length = 200, blank = False, null = False)
    fathers_occupation = models.CharField(_("Father's Occupation"), choices = FATHERS_OCCUPATION_CHOICES ,max_length = 5, blank = False, null = False)
    mothers_occupation = models.CharField(_("Mother's Occupation"), choices = MOTHERS_OCCUPATION_CHOICES ,max_length = 5, blank = False, null = False)
    religion = models.CharField(_("Religion"), choices = RELIGION_CHOICES, max_length = 5, blank = False, null = False)
    nationality = models.CharField(_("Nationality"), choices = NATIONALITY_CHOICES, max_length = 5, blank = False, null = False)
    has_qualified_entrance = models.BooleanField(_('Has Student qualified the entrance examination?'), blank = False, null = False, default = False)
    thumb_impression = models.FileField(upload_to = settings.PATH_TO_UPLOAD_USER_THUMB_IMPRESSION, blank = True, null = True)
    correspondence_address = models.ForeignKey(Address, related_name = 'correspondence_address_general_info')
    permanant_address = models.ForeignKey(Address, related_name = 'permanant_address_general_info')


    def __init__(self, arg):
        super(GeneralInfo, self).__init__()
        self.arg = arg


class PreviousEducationDetails(models.Model):
    """
        This model will contains info of student's past
        qualified educations like High School, Intermediate
    """
    student = models.ForeignKey(User, related_name = 'education_details') 
    course = models.CharField(_('Course Name'), max_length = 50, blank = False, null = False)
    year_of_passing = models.CharField(_('Course Name'), choices = YEAR_CHOICES, max_length = 50, blank = False, null = False)
    board_or_university = models.CharField(_("Board or University"), max_length = 200, blank = False, null = False)
    college_name = models.CharField(_("College Name"), max_length = 200, blank = False, null = False)
    result = models.CharField(_('Result'), choices = EDUCATION_RESULT_CHOICE, max_length = 50, blank = False, null = False)
    percentage = models.FloatField(_('Result'), validators = [MinValueValidator(0), MaxValueValidator(100)])

    def __init__(self, arg):
        super(PreviousEducationDetails, self).__init__()
        self.arg = arg
        
        
