from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class Name(models.Model):
	name = models.CharField(_("Name"), max_length = 200, blank = False, null = False)


	class Meta:
		abstract = True

	def __unicode__(self):
		return self.name

