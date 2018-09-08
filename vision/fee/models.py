from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


#################   Already Built Module Imports   ################


###################################################################


#####################  Working Modules Imports   ##################
from vision.generic_models import Name


from vision.institute.models import SessionCourse

###################################################################

class FeeType(Name):
	def __unicode__(self):
		return "%s Fee"%(self.name)



class CourseFeeDetail(models.Model):
	course = models.ForeignKey(SessionCourse, related_name = 'course_fee_details')
	fee_type = models.ForeignKey(FeeType, related_name = 'fee_cources')
	amount = models.IntegerField(_("Fee Amount"), validators = [MinValueValidator(0), MaxValueValidator(100)])
	is_installments_allowed = models.BooleanField(_("Is student allowed to submit fee in installments"), default = False)
	number_of_installments = models.IntegerField(_("Number of Installments"), validators = [MinValueValidator(1)], default = 1)



class Installments(models.Model):
	course_fee_detail = models.ForeignKey(CourseFeeDetail, related_name = 'course_fee_installments')
	installment_number = models.IntegerField(_("Installment Number"), validators = [MinValueValidator(1)])
	amount = models.IntegerField(_("Installment Amount"), validators = [MinValueValidator(0)])
	deadline = models.DateTimeField(auto_now = False, auto_now_add = False)


class StudentFeeSubmission(object):
	fee_installment = models.ForeignKey(Installments, related_name = 'installments_submitted_by_students')
	student = models.ForeignKey(User, related_name = "fee_submitted")
	