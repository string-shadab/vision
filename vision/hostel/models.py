from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

#################   Already Built Module Imports   ################

###################################################################


#####################  Working Modules Imports   ##################
from vision.generic_models import Name

###################################################################


PREFERENCE_CHOICE = (
	('1', '1',),
	('2', '2',),
	('3', '3',),
	('4', '4',),
	('5', '5',),
	('6', '6',),
	('7', '7',),
	('8', '8',),
	('9', '9',),
	('10', '10',),
)


class RoomType(Name):
	capacity = models.IntegerField(_("Capacity of room"), validators = [MinValueValidator(1)])
	minimun_seniority_required = models.IntegerField(_("Minimun Seniority Required"), validators = [MinValueValidator(0)])
	preference = models.CharField(_("Preference"), max_length = 5, choices = PREFERENCE_CHOICE)


class Hostel(Name):
    number_of_rooms = models.IntegerField(_("Total Number of rooms "), validators = [MinValueValidator(1)])
    


class HostelRooms(models.Model):
	hostel = models.ForeignKey(Hostel, related_name = 'rooms')
	room_type = models.ForeignKey(RoomType, related_name = 'hostel_rooms')
	count = models.IntegerField(_("Number of rooms"), validators = [MinValueValidator(1)])


class RoomNumber(models.Model):
	hostel_room = models.ForeignKey(HostelRooms, related_name = 'room_details')
	number = models.CharField(_("Room Number"), max_length = 5)
	allotment = models.ManyToManyField(User, related_name = 'rooms_student')


