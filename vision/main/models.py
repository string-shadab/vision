from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext, ugettext_lazy as _
import os
from django.contrib.auth.models import User
import datetime
import time
from datetime import timedelta
import subprocess
# from eVidyalay_live.publisher.models import Publisher
from django.utils import timezone
# from eVidyalay_live.faculty.models import Faculty
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# from eVidyalay_live.forum.core.utils.models import AutoSlugField

#Path to Upload Property Images
file_storage = FileSystemStorage(location = settings.PATH_TO_UPLOAD_BOOK_FILES)
user_img_storage = FileSystemStorage(location = settings.PATH_TO_UPLOAD_BOOK_FILES)

COURSE_DURATION_CHOICES = (('sem', 'Semester'), ('year', 'Year'))
SEM_NO_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'))
YEAR_NO_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4') ) #, ('5', '5'), ('6', '6')

#PYJSWEEKDAYS = {'0' : '1', '1' : '2', '2' : '3', '3' : '4', '4' : '5', '5' : '6', '6' : '0'}
WEEKDAY_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

CATEGORY_CHOICES = ( ('B00', 'Civil Engineering'), ('B07', 'Mining Engineering'), ('B10', 'Computer Science & Engineering'), ('B11', 'Computer Science'), \
 ('B12', 'Comp. Engineering & Information Technology'), ('B13', 'Information Technology'), ('B14', 'Master of Computer Application'),  \
 ('B15', 'Computer Engineering'), ('B16', 'Information Science'), ('B20', 'Electrical Engineering'), ('B21', 'Electrical & Electronics Engineering'),  \
 ('B22', 'Instrumentation & Control Engineering'), ('B23', 'Instrumentation Engineering'), ('B30', 'Electronics Engineering'),  \
 ('B31', 'Electronics & Communication Engineering'), ('B32', 'Electronics & Instrumentation Engineering'), ('B33', 'Electronics & Telecommunication Engineering'),  \
 ('B34', 'Electronics, Instrumentation & Controll Engineering'), ('B35', 'Applied Electronics & Instrumentation Engineering'),  ('B40', 'Mechanical Technology'), \
 ('B41', 'Manufacturing Technology'), ('B42', 'Metallurgical Engineering'), ('B43', 'Mechanical & Industrial Engineering'),  ('B44', 'Production Engineering'), \
 ('B45', 'Industrial & Production Engineering'), ('B46', 'Production & Industrial Engineering'), ('B50', 'Bachelor of Pharmacy'),  ('B51', 'Chemical Engineering'), \
 ('B52', 'Bio-Chemical Engineering'), ('B53', 'Chemical & Alcohol Technology'), ('B54', 'Bio-Technology'),  ('B55', 'Chemical & Bio Engg,'), \
 ('B60', 'Textile Chemistry'), ('B61', 'Textile Technology'), ('B62', 'Man-made Fibre Technology'),  ('B63', 'Textile Engineering'), \
 ('B64', 'Carpet Technology'), ('B65', 'Bachelor of Fashion & Apparel Design (BFAD)'), ('B70', 'MBA'),  ('B72', 'MBA (Rural Development)'), \
 ('B74', 'BHMCT'), ('B80', 'Agricultural Engineering'), ('B81', 'Architecture'), ('B82', 'Food Technology & Engineering'),  ('B83', 'Sugar Technology'), \
 ('B84', 'Oil Technology'), ('B85', 'Paint Technology'), ('B86', 'Leather Technology'), ('B87', 'Plastic Technology'),  \
 ('B88', 'Ceramic Technology'), ('B89', 'Agriculture Engineering'))

GENDER_CHOICES = (
  ('1', 'Male'),
  ('2', 'Female'),
  ('3', 'Others')
)

CLASS_TYPE_CHOICES = (
  ('1', 'Lecture'),
  ('2', 'Tutorial'),
  ('3', 'Lab'),
  ('4', 'Others'),
  ('5', 'Lunch Break'),
  ('6', 'Break'),
)

NOTIFICATION_TYPE_CHOICES = (
  ('1', 'Class Update'),
  ('2', 'Campus Update')
)

EDUCATION_TYPE_CHOICES = (
  ('1', 'High School'),
  ('2', 'Intermediate')
)

def get_profile(self):
  # if self.groups.filter(name='publisher').exists():
  #   return Publisher.objects.get(user = self)
  if self.groups.filter(name='librarian').exists():
    return Librarian.objects.get(user = self)
  elif self.groups.filter(name='faculty').exists():
    return self.facultyprofile
  else:
    return self.profile
User.add_to_class("get_related_profile", get_profile)


class Institute(models.Model):
  name = models.CharField(_("Institute Name"), max_length = 200, blank = True, null = True)
  university = models.ForeignKey('University', blank = True, null = True)
  course = models.ForeignKey('Course', blank = True, null = True, related_name = 'courses')
  logo = models.FileField(upload_to = settings.PATH_TO_UPLOAD_INSTITUTE_LOGO, blank = True, null = True)
  is_allow_attendance_within_campus = models.BooleanField(_("Allow within Radius?"), default=True)
  campus_radius = models.IntegerField(_("Campus Radius (in mtrs)"), blank = True, null = True)

  def get_logo_url(self):
    if self.logo:
      return os.path.join(settings.MEDIA_URL, self.logo.url.split('media/')[1])
    return '/static/new_layout/images/logo-new.png'

  def __unicode__(self):
    return '%s' %(self.name)


class Subject(models.Model):
  institute = models.ForeignKey('Institute', blank = True, null = True)
  course_name = models.ForeignKey('Course', blank = True, null = True, related_name = 'subject_courses')
  branch = models.ForeignKey('Branch', blank = True, null = True, related_name = 'branch')
  sem_no = models.CharField(_("Semester"), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_("Year"), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  subject_name = models.CharField(_("Subject Name"), max_length = 200, blank = True, null = True)
  subject_code = models.CharField(_("Subject Code"), max_length = 200, blank = True, null = True)
  is_live = models.BooleanField(_("Make it live?"), default=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

  def get_obj_url(self):
    return '/subject/%s' %(self.id)

  def model_title(self):
    return 'Subject'

  def subject_notes(self):
    return SavedNotes.objects.exclude(is_live = False).filter(book__subject = self)

  def __unicode__(self):
    return self.subject_name #'%s - %s' %(self.subject_name, self.subject_code)


class Faculty(models.Model):
  user = models.OneToOneField(User, related_name = 'facultyprofile') #models.ForeignKey(User, unique=True)
  institute = models.ForeignKey(Institute, unique=False) # models.OneToOneField(Institute)
  logo = models.FileField(upload_to = settings.PATH_TO_UPLOAD_USER_IMAGES, blank = True, null = True)
  fax = models.CharField(_('Fax'), max_length = 200, blank = True, null = True)
  website = models.CharField(_('Website'), max_length = 200, blank = True, null = True)

  f_name = models.CharField(_('First Name'), max_length = 200, blank = True, null = True, default = '')
  l_name = models.CharField(_('Last Name'), max_length = 200, blank = True, null = True, default = '')
  gender = models.CharField(_('Gender'), choices = GENDER_CHOICES, max_length = 10, blank = True, null = True, default = '')
  subject = models.ManyToManyField(Subject, verbose_name = 'Subject Faculty', blank = True, related_name = 'subject_faculty')
  teacher_id = models.CharField(_('Teacher ID'), max_length = 200, blank = True, null = True)
  is_active = models.BooleanField(_('Currently Working?'), default=False)
  
  coorporate_address = models.TextField(blank=True, null=True)
  phone = models.CharField(_('Phone'), max_length = 200, blank = True, null = True)
  email = models.CharField(_('Email ID'), max_length = 200, blank = True, null = True)
  skype = models.CharField(_('Skype'), max_length = 200, blank = True, null = True)

  yt_access_token = models.CharField(_('YouTube Access Token'), max_length = 200, blank = True, null = True)
  yt_refresh_token = models.CharField(_('YouTube Refresh Token'), max_length = 200, blank = True, null = True)

  class Meta:
    verbose_name_plural = 'Faculty'

  def get_full_name(self):
    return '%s %s' %(self.f_name, self.l_name)

  def __unicode__(self):
    return '%s %s (%s)' %(self.f_name, self.l_name, self.teacher_id)

  def get_media_url(self):
    if self.logo:
      return os.path.join(settings.MEDIA_URL, self.logo.url.split('media/')[1])
    elif self.gender == '2':
      return '/static/img/af.png'
    return '/static/img/am.png'

  def get_subject_names(self):
    return '<br>'.join( self.subject.all().values_list('subject_name', flat = True) )



class NoAppRecord(models.Model):
  user = models.ForeignKey(User, blank = True, null = True)
  user_agent = models.CharField(_("User Agent"), max_length = 300, blank = True, null = True)
  ip_address = models.CharField(_("IP Address"), max_length = 50, blank = True, null = True)
  url_accessed = models.CharField(_("URL"), max_length = 50, blank = True, null = True)
  datetime_attempted = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)

  def __unicode__(self):
    return '%s' %(self.user.username)

class Visitor(models.Model):
  user = models.ForeignKey(User, null=False)
  session_key = models.CharField(null=False, max_length=40)
  is_mobile = models.BooleanField(default = False)
  last_seen = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
  is_logged_out = models.BooleanField(default = False)
  
  def __unicode__(self):
    return '%s' %(self.user.username)


class City(models.Model):
  name = models.CharField(_("City"), max_length = 200, blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.name)

class University(models.Model):
  name = models.CharField(_("University Name"), max_length = 200, blank = True, null = True)
  city = models.ForeignKey('City', blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.name)



class Course(models.Model):
  course_name = models.CharField(_("Course Name"), max_length = 200, blank = True, null = True)
  institute = models.ForeignKey('Institute', blank = True, null = True, related_name = 'institute')
  duration = models.CharField(_("Duration"), choices = COURSE_DURATION_CHOICES, max_length = 10, blank = True, null = True, default = "")
  sem_no = models.CharField(_("Semester"), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_("Year"), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  is_live = models.BooleanField(_("Make it live?"), default=True)

  def __unicode__(self):
    return '%s' %(self.course_name)

class Branch(models.Model):
  branch_name = models.CharField(_("Branch Name"), max_length = 200, blank = True, null = True)
  branch_code = models.CharField(_("Branch Code"), max_length = 200, blank = True, null = True)
  institute = models.ForeignKey('Institute', blank = True, null = True)

  class Meta:
    verbose_name_plural = 'Branches'

  def __unicode__(self):
    return self.branch_code #'%s (%s)' %(self.branch_name, self.branch_code)



class BookWriter(models.Model):
  writer_name = models.CharField(_("Writer Name"), max_length = 200, blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.writer_name)

class Category(models.Model):
  category = models.CharField(_("Category Title"), max_length = 200, blank = True, null = True)
  is_live = models.BooleanField(_("Make it live?"), default=True)

  def __unicode__(self):
    return '%s' %(self.category)

class TableContents(models.Model):
  book = models.ForeignKey('BookUpload', blank = True, null = True)
  chapter_no = models.IntegerField(_("Chapter No"), blank = True, null = True)
  chapter_title = models.CharField(_("Chapter name"), max_length = 200, blank = True, null = True)
  sub_heading_no = models.IntegerField(_("Heading No"), blank = True, null = True)
  sub_heading_title = models.CharField(_("Sub Heading Title"), max_length = 200, blank = True, null = True)
  parent = models.ForeignKey('TableContents', blank = True, null = True, related_name = 'sub_head')
  page_no = models.IntegerField(_("Page No"), blank = True, null = True)

  class Meta:
    verbose_name_plural = 'Table Contents'

  def __unicode__(self):
    if self.book:
      return 'Book(%s) - Chapter(%s)' %(self.book, self.chapter_no)
    return str(self.chapter_no)

class BookUpload(models.Model):
  book_name = models.CharField(_("Book Title"), max_length = 200, blank = True, null = True)
  book_writer = models.ForeignKey('BookWriter', blank = True, null = True)
  no_of_pages = models.IntegerField(_("Total No of Pages"), blank = True, null = True)
  edition = models.CharField(_("Edition"), max_length = 200, blank = True, null = True)
  pub_year = models.IntegerField(_("Published Year"), blank = True, null = True)
  subject = models.ManyToManyField('Subject', blank = True, related_name = 'subject_books')
  uploads = models.ForeignKey('BookImage', blank=True, null=True)
  is_novel = models.BooleanField(_("Novel?"), default=False)
  is_pd_stuff = models.BooleanField(_("Personality Development Stuff?"), default=False)
  category = models.ForeignKey('Category', blank = True, null = True, related_name = 'novel_category')
  is_live = models.BooleanField(_("Make it live?"), default=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  is_ques_paper = models.BooleanField(_("Is Question Paper?"), default=False)
  is_study_material = models.BooleanField(_("Is Study Material?"), default=False)
  ques_paper_year = models.CharField(_("Ques Paper Year"), max_length = 200, blank = True, null = True)
  pdf_first_uploaded = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True)

  # Data to be uploaded by the publisher
  # publisher = models.ForeignKey(Publisher, blank = True, null = True, related_name = 'publisher')
  book_cover = models.FileField(upload_to = settings.PATH_TO_UPLOAD_BOOK_COVER, blank = True, null = True)
  isb_no = models.CharField(_("ISB Number"), max_length = 200, blank = True, null = True, unique = True)
  price = models.IntegerField(_("Price"), blank = True, null = True)
  branch = models.CharField(_("Category"), choices = CATEGORY_CHOICES, max_length = 10, blank = True, null = True, default = "")

  # Exclude from Librarian Catalog
  is_excluded = models.BooleanField(_("Exclude"), default=False)

  class Meta:
    verbose_name_plural = 'Uploads Summary'

  def get_encpt_obj_id(self):
    #TODO: Encrypt ID and return
    return str(self.id)

  def model_title(self):
    if self.is_novel:
      return 'Novel'
    if self.is_pd_stuff:
      return 'PD'
    else:
      return 'Subject Book'

  def get_obj_url(self):
    if self.is_novel:
      return '/novel/%s' %(self.id)
    if self.is_pd_stuff:
      return '/pd/%s' %(self.id)
    else:
      return '/book/%s' %(self.id)

  def get_preview_url(self):
    if not self.is_novel and not self.is_pd_stuff:
      if self.uploads:
        return '/eV!dYalay3nCYpTm3d!@/uploads/books/%s' %(self.uploads.file.url.split('/')[-1])

  def registered_users(self):
    from eVidyalay_live.librarian.models import ChosenBook
    registered_users = 0
    books = ChosenBook.objects.filter(book = self, created_at__lte = datetime.datetime.now() - datetime.timedelta(settings.FREEZE_TIME))

    for each_book in books:
      registered_users += UserProfile.objects.exclude(is_live = False).filter(institute = each_book.librarian.institute,\
        sem_no = each_book.sem_no, branch = each_book.branch).count() #.exclude(is_faculty = True)

    return registered_users

  def __unicode__(self):
    return '%s by %s' %(self.book_name, self.book_writer)

  def book_cover_img(self):
    if self.book_cover:
      return os.path.join(settings.MEDIA_URL, self.book_cover.url.split('media/')[1])
    return os.path.join(settings.STATIC_URL, 'img/blank_cover.jpg')

  def expire_date(self):
    try:
      return self.pdf_first_uploaded + timedelta(days = 365)
    except:
      return '-'

  def save(self, *args, **kwargs):
    """
    Take the pdf file and make separate images for each page.
    """
    super(BookUpload, self).save(*args, **kwargs)
    try:
      fetch_images = False
      if self.pk and self.uploads:
        old_ins = BookUpload.objects.get(pk=self.pk)
        if not old_ins.uploads == self.uploads and (self.uploads and self.uploads.file.url.split('.')[1] == 'pdf'):
          fetch_images = True
          from pyPdf import PdfFileReader
          pdf = PdfFileReader(open(self.uploads.file.url))
          self.no_of_pages = pdf.getNumPages()

      if not self.pk and self.uploads:
        fetch_images = True

      # TODO - Remove this line before pushing it to production
      fetch_images = True # Remove

      if fetch_images:
        directory = "/".join(self.uploads.file.url.split('/')[:-1]) + '/book_' + str(self.id)
        command = 'convert ' + self.uploads.file.url + ' ' + "/".join(self.uploads.file.url.split('/')[:-1]) + '/book_' + str(self.id) + '/image.png'
        # print command
        if not os.path.exists(directory):
          os.makedirs(directory)
          os.chmod(directory, 777)
          subprocess.call(command)
        img_obj = os.system(command)
      super(BookUpload, self).save(*args, **kwargs)
    except Exception as e:
      print e

class BookImage(models.Model):
  file = models.FileField(upload_to = settings.PATH_TO_UPLOAD_BOOK_FILES, blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.file.url.split('/')[-1])
    

class UserProfile(models.Model):
  user = models.OneToOneField(User, related_name = 'profile') #models.ForeignKey(User, unique=True)
  f_name = models.CharField(_("First Name"), max_length = 200, blank = True, null = True, default = "")
  l_name = models.CharField(_("Last Name"), max_length = 200, blank = True, null = True, default = "")
  gender = models.CharField(_("Gender"), choices = GENDER_CHOICES, max_length = 10, blank = True, null = True, default = "")
  institute = models.ForeignKey('Institute', blank = True, null = True, related_name = 'student_institute')
  course = models.ForeignKey('Course', blank = True, null = True)
  sem_no = models.CharField(_("Semester"), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_("Year"), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  # subject = models.ForeignKey('Subject', verbose_name = "Subject Faculty", blank = True, null = True, related_name = 'subject_course')
  email_id = models.EmailField(_("Email"))
  # teacher_id = models.CharField(_("Teacher ID"), max_length = 200, blank = True, null = True)
  dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
  enrollment_no = models.CharField(_("Enrollment No"), max_length = 200, blank = True, null = True)
  # is_faculty = models.BooleanField(_("Faculty?"), default=False)
  profile_img = models.FileField(upload_to = settings.PATH_TO_UPLOAD_USER_IMAGES, blank = True, null = True)
  is_live = models.BooleanField(_("Make it live?"), default=True)
  branch = models.ForeignKey('Branch', blank = True, null = True, related_name = 'student_branch')
  current_city = models.ForeignKey('City', blank = True, null= True, related_name= 'user_current_city')
  native_city = models.ForeignKey('City', blank = True, null= True, related_name= 'user_home_city')
  contact = models.CharField(_("Contact Number"), max_length=10, blank=True, null=True)
  hobbies = models.TextField(_("Hobbies"), max_length=512, blank=True, null=True, default="")
  fav_games = models.TextField(_("Favourite Games"), max_length=512, blank=True, null=True, default="")
  about_me = models.TextField(_("About Me"), max_length=512, blank=True, null=True, default="")
  is_access_blocked = models.BooleanField(default = False) # Live Stream Access Blocked
  last_read_notification = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True) # last_read_notifications

  is_facerecog_enabled = models.BooleanField(default = False) # Live Stream Access Blocked

  institute_name = models.CharField(_("Institute Name"), max_length = 200, blank = True, null = True)
  institute_logo = models.FileField(upload_to = settings.PATH_TO_UPLOAD_INSTITUTE_LOGO, blank = True, null = True)
  institute_city = models.CharField(_("Institute City"), max_length = 200, blank = True, null = True)
  is_demo_user = models.BooleanField(default = False)

  # Fields to be used in discussion forum
  # slug = AutoSlugField(populate_from="user.username", db_index=False, blank=True)
  last_seen = models.DateTimeField(_("last seen"), auto_now=True)
  last_seen_friend_list=models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True)
  last_ip = models.GenericIPAddressField(_("last ip"), blank=True, null=True)
  topic_count = models.PositiveIntegerField(_("topic count"), default=0)
  comment_count = models.PositiveIntegerField(_("comment count"), default=0)
  last_post_hash = models.CharField(_("last post hash"), max_length=32, blank=True)
  last_post_on = models.DateTimeField(_("last post on"), null=True, blank=True)
  # location = models.CharField(_("location"), max_length=75, blank=True)
  # timezone = models.CharField(_("time zone"), max_length=32, default='UTC')
  # is_administrator = models.BooleanField(_('administrator status'), default=False)
  is_moderator = models.BooleanField(_('moderator status'), default=True)
  # is_verified = models.BooleanField(_('verified'), default=False)


  def __unicode__(self):
    return '%s %s' %(self.f_name, self.l_name)

  def get_institute_logo_url(self):
    if self.institute_logo:
      return os.path.join(settings.MEDIA_URL, self.institute_logo.url.split('media/')[1])
    return '/static/new_layout/images/logo-new.png'

  def get_absolute_url(self):
    return self.get_view_profile_url()

  def update_post_hash(self, post_hash):
    assert self.pk
    return bool(UserProfile.objects
                .filter(pk=self.pk)
                .exclude(
                    last_post_hash=post_hash,
                    last_post_on__gte = datetime.datetime.now() - timedelta(
                        minutes=settings.ST_DOUBLE_POST_THRESHOLD_MINUTES))
                .update(
                    last_post_hash=post_hash,
                    last_post_on = datetime.datetime.now()))

  def get_full_name(self):
    return self.f_name + ' ' + self.l_name

  def get_media_url(self):
    if self.profile_img:
      return os.path.join(settings.MEDIA_URL, self.profile_img.url.split('media/')[1])
    elif self.gender == '2':
      return '/static/img/af.png'
    return '/static/img/am.png'

  def get_view_profile_url(self):
    return '/profiles/%s/' %(self.user.username)

  def get_semester_string(self):
    if not int(self.sem_no) % 2 == 0:
      return 'July %s - December %s' %(datetime.date.today().year, datetime.date.today().year)
    else:
      return 'January %s - June %s' %(datetime.date.today().year, datetime.date.today().year)

  def attended_classes(self):
    data = {}
    for each_rec in StudentLiveEventCount.objects.filter(user = self.user):
      if not data.has_key(each_rec.event.id):
        data[each_rec.event.id] = {'name' : '', 'time' : []}
      data[each_rec.event.id]['name'] = each_rec.event.title
      data[each_rec.event.id]['time'].append( [each_rec.get_start_time(), each_rec.get_last_record_time()] )
    return data

  def get_classes_attended(self):
    count = 0
    try:
      event_count = StudentLiveEventCount.objects.filter(user = self.user).values_list('event_id', flat = True)
      return len(list(set(event_count)))
    except Exception as e:
      print e
      return 0

  def subject_list(self):
    return Subject.objects.filter(is_live = True).filter(Q(institute = self.institute) & Q(course_name = self.course) &\
      Q(branch = self.branch) &  Q(sem_no = self.sem_no) & Q(year_no = self.year_no) )

  def get_classes_attended_color(self):
    if self.get_classes_attended() >= 3 and self.get_classes_attended() <= 5:
      return 'row_yellow'
    elif self.get_classes_attended() > 5:
      return 'row_red'
    return ''

class UserAchievement(models.Model):
  userprofile = models.ForeignKey('UserProfile', blank = True, null= True, related_name= 'achivement_user_profile')
  title = models.CharField(_("Achievement Title"), max_length = 200, blank = True, null = True, default = "")
  description= models.CharField(_("Achievement Description"), max_length = 512, blank = True, null = True, default = "")
  achievement_date = models.DateField(verbose_name='Date of Achievement', null=True, blank=True)


def __unicode__(self):
  return '%s %s' %(self.title, self.userprofile)

class UserEducation(models.Model):
  userprofile = models.ForeignKey('UserProfile', blank=True, null=True, related_name='user_profile')
  education_type = models.CharField(_('Education'), choices=EDUCATION_TYPE_CHOICES, max_length=10, blank=True,null=True, default="")
  description = models.CharField(_("Achievement Description"), max_length=512, blank=True, null=True, default="")
  from_date = models.DateField(verbose_name='From Date', null=True, blank=True)
  to_date = models.DateField(verbose_name='To Date', null=True, blank=True)

def __unicode__(self):
  return '%s %s' % (self.education_type, self.userprofile)

class SavedNotes(models.Model):
  title = models.CharField(_("Note Title"), max_length = 100, blank = True, null = True)
  user = models.ForeignKey(User, blank = True, null = True)
  x1 = models.CharField(_("Coordinate X1"), max_length = 100, blank = True, null = True)
  x2 = models.CharField(_("Coordinate X2"), max_length = 100, blank = True, null = True)
  y1 = models.CharField(_("Coordinate Y1"), max_length = 100, blank = True, null = True)
  y2 = models.CharField(_("Coordinate Y1"), max_length = 100, blank = True, null = True)
  width = models.CharField(_("Image width(when note was taken)"), max_length = 100, blank = True, null = True)
  height = models.CharField(_("Image height(when note was taken)"), max_length = 100, blank = True, null = True)
  book = models.ForeignKey('BookUpload', blank = True, null = True)
  page_no = models.CharField(_("Page No"), max_length = 100, blank = True, null = True)
  image = models.FileField(upload_to = settings.PATH_TO_UPLOAD_NOTES, blank = True, null = True)
  is_live = models.BooleanField(_("Make it live?"), default=True)

  def __unicode__(self):
    return '%s - %s' %(self.title, self.user)

  def get_note_img_url(self):
    from eVidyalay_live.utils import get_encrypted_string
    return os.path.join( settings.MEDIA_URL , 'encyptnote', get_encrypted_string( self.image.url.split('media/')[1] ) )


class Game(models.Model):
  title = models.CharField(_("Game Title"), max_length = 100, blank = True, null = True)
  source = models.CharField(_("Game Source"), max_length = 200, blank = True, null = True)
  source_link = models.CharField(_("Game Source Link"), max_length = 1000, blank = True, null = True)
  embed_code = models.TextField(blank=True, null=True)
  is_live = models.BooleanField(_("Make it live?"), default=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

  def model_title(self):
    return 'Game'

  def __unicode__(self):
    return '%s - %s' %(self.title, self.source)

  def get_obj_url(self):
    return '/game/%s' %(self.id)

class Activity(models.Model):

  '''
  Class is in no use.....
  '''

  title = models.CharField(_("Activity Title"), max_length = 100, blank = True, null = True)
  venue = models.TextField(_("Venue"), blank=True, null=True)
  start_time = models.DateTimeField(_("Start Time"), blank=True, null=True)
  end_time = models.DateTimeField(_("End Time"), blank=True, null=True)
  description = models.TextField(_("Details"), blank=True, null=True)
  is_live = models.BooleanField(_("Make it live?"), default=True)
  is_event = models.BooleanField(_("Is it an event?"), default=False)
  poster = models.FileField(upload_to = settings.PATH_TO_UPLOAD_EVENT_POSTER, blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.title)

  def get_poster_url(self):
    return os.path.join(settings.MEDIA_URL, self.poster.url.split('media/')[1])




class FeedBack(models.Model):
  name = models.CharField(_("Name"), max_length = 200, blank = True, null = True, default = "")
  email_id = models.EmailField(_("Email"))
  subject = models.CharField(_("Subject"), max_length = 1000, blank = True, null = True, default = "")
  body = models.TextField(blank = True, null = True)

  def __unicode__(self):
    return '%s' %(self.name)

class StudentTeacherConversation(models.Model):
  parent = models.ForeignKey('AskTeacher', blank=True, null=True)
  is_teacher_reply = models.BooleanField(default=False)
  text = models.TextField(_("What's your reply"), blank = True, null = True)
  datetime = models.DateTimeField(auto_now=True)

  def __unicode__(self):
     return '%s' %(self.text)

class AskTeacher(models.Model):
  # from eVidyalay_live.faculty.models import Faculty
  name = models.CharField(_("Name"), max_length = 200, blank = True, null = True, default = "", editable=False)
  email_id = models.EmailField(_("Email"), editable=False)
  teacher = models.ForeignKey(Faculty, blank = True, null = True, related_name="teacher")
  question = models.TextField(_("What's your question"), blank = True, null = True)
  datetime = models.DateTimeField(auto_now=True)
  student = models.ForeignKey('UserProfile', blank = True, null = True, related_name="student", editable=False)

  def __unicode__(self):
    return '%s by %s' %(self.question, self.name)

  def get_reply_url(self, room_obj):
    from django.contrib.sites.models import Site
    return 'http://%s/chat/%s/' %(Site.objects.get_current().domain, str(room_obj))


class NotificationCategory(models.Model):
  title = models.CharField(_("Title"), max_length = 200, blank = True, null = True)
  icon_class = models.CharField(_("Icon Class"), max_length = 200, blank = True, null = True)
  notification_type = models.CharField(_("Notification Type"), choices = NOTIFICATION_TYPE_CHOICES, max_length = 10, blank = True, null = True)

  def __unicode__(self):
    return self.title

  # def get_notification_type_icon_class(self):
  #   if self.notification_type == '1':
  #     if self.title=
  #     return 'fa fa-clipboard green-icon'
  #   else:
  #     return 'fa fa-th orange-icon'
    

class NotificationRead(models.Model):
  notification = models.ForeignKey('Notification', blank = True, null = True, related_name='read_notifications')
  read_by = models.ForeignKey(User, blank = True, null = True)
  read_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False, null = False)

  def __unicode__(self):
    return '%s - %s' %(self.notification.title, self.read_by.username)

class Notification(models.Model):
  # from eVidyalay_live.faculty.models import Faculty
  title = models.CharField(_("Activity Title"), max_length = 100, blank = True, null = True)
  venue = models.TextField(_("Venue"), blank=True, null=True)
  start_time = models.DateTimeField(_("Start Time"), blank=True, null=True)
  end_time = models.DateTimeField(_("End Time"), blank=True, null=True)
  description = models.TextField(_("Details"), blank=True, null=True)
  summary = models.TextField(_("Summary"), blank=True, null=True, editable=False)
  upload = models.FileField(upload_to = settings.PATH_TO_UPLOAD_NOTI_FILE, blank = True, null = True)
  sem_no = models.CharField(_("Semester"), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_("Year"), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  for_staff_only = models.BooleanField(_("For Staff Only?"), default=False, editable = False)
  institute = models.ForeignKey('Institute', blank = True, null = True, related_name = 'institute_to_notify')
  category = models.ForeignKey('NotificationCategory', blank = True, null = True, related_name = 'notification_category')
  
  for_individual = models.BooleanField(_("For Individual?"), default=False, editable = False)
  individual_user = models.ForeignKey(User, blank = True, null = True, editable = False)

  content_type = models.ForeignKey(ContentType, blank = True, null = True, editable = False)
  object_id = models.CharField(max_length=255, blank = True, null = True, editable = False)
  related_object = GenericForeignKey('content_type', 'object_id')

  faculty = models.ForeignKey(Faculty, blank = True, null = True, related_name="faculty_notification")

  is_live = models.BooleanField(_("Live?"), default=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

  def __unicode__(self):
    return self.title

  def get_cat_url(self):
    return os.path.join(settings.MEDIA_URL, self.category.icon.url.split('media/')[1])

  def file_url(self):
    if self.upload:
      return os.path.join(settings.MEDIA_URL, self.upload.url.split('media/')[1])
    return None

  def get_time_string(self):
    if self.start_time and self.end_time:
      return '%s - %s' %( self.start_time.strftime('%I:%M %p'), self.end_time.strftime('%I:%M %p') )
    elif self.start_time:
      return 'Start Time: %s' %( self.start_time.strftime('%I:%M %p') )
    elif self.end_time:
      return 'End Time: %s' %( self.end_time.strftime('%I:%M %p') )
    return ''

  def get_date_string(self):
    if self.start_time and self.end_time:
      return '%s TO %s' %( self.start_time.strftime('%Y-%m-%d'), self.end_time.strftime('%Y-%m-%d') )
    elif self.start_time:
      return 'Start Date: %s' %( self.start_time.strftime('%Y-%m-%d') )
    elif self.end_time:
      return 'End Date: %s' %( self.end_time.strftime('%Y-%m-%d') )
    return ''

class BookRequest(models.Model):
  """
  Book Requested by Librarian...
  """
  book = models.ForeignKey(BookUpload, unique=False, blank=False, null=False)
  institute = models.ForeignKey(Institute, unique=False, blank=False, null=False)
  requested_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  is_completed = models.BooleanField(default=False, editable = True)
  completed_at = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True)
  is_denied = models.BooleanField(default=False, editable = True)
  denied_at = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True)

  def __unicode__(self):
    return '%s - %s' %(self.book, self.institute)

class TimeTable(models.Model):
  institute = models.ForeignKey(Institute, unique=False, blank=False, null=False)
  course_name = models.ForeignKey('Course', blank = True, null = True, related_name = 'tt_course')
  branch = models.ForeignKey('Branch', blank = True, null = True, related_name = 'tt_branch')
  sem_no = models.CharField(_('Semester'), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_('Year'), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  subject = models.ForeignKey('Subject', blank = False, null = False, related_name = 'tt_subject')
  weekday = models.IntegerField(blank = True, null = True, choices = WEEKDAY_CHOICES)
  time_start = models.TimeField(blank = True, null = True)
  time_end = models.TimeField(blank = True, null = True)
  class_type = models.CharField(_('Class Type'), choices = CLASS_TYPE_CHOICES, max_length = 10, blank = False, null = False, default = '1')
  is_live = models.BooleanField(_("Make it live?"), default=True)
  date_start = models.DateField(verbose_name='Start Date', null=True, blank=True)
  date_end = models.DateField(verbose_name='End Date', null=True, blank=True)

  # class Meta:
  #   ordering = ['weekday', 'time_start']

  def save(self, *args, **kwargs):
    self.course_name = self.subject.course_name
    self.branch = self.subject.branch
    super(TimeTable, self).save(*args, **kwargs)

  def __unicode__(self):
    return 'Course: %s - Subject: %s - SEM: %s - Day: %s' %(self.course_name, self.subject, self.sem_no, self.get_weekday_display() )

  def display_name(self):
    return 'Course: %s, Subject: %s [%s]' %(self.course_name, self.subject, self.get_weekday_display() )

  def student_list(self):
    return UserProfile.objects.exclude(user__is_active = False).filter(institute = self.institute,\
      course = self.course_name, sem_no = self.sem_no, year_no = self.year_no, branch = self.branch)

  def calendar_display(self):
    # return '%s, [Sem: %s]' %(self.course_name, self.sem_no)
    return '%s [%s]' %(self.subject, self.course_name)

  def get_weekday(self):
    return WEEKDAY_CHOICES[self.weekday]

  def is_otp_generated(self):
    otp_obj_list = AttendanceOTP.objects.exclude(is_expired = True)\
        .filter(timetable = self, created_at__date = datetime.datetime.now().date() ).order_by('-created_at')
    if len(otp_obj_list):
      otp_obj = otp_obj_list[0]
      currentdt = datetime.datetime.now() # timezone.now()

      if (currentdt - otp_obj.created_at).total_seconds() > settings.OTP_EXPIRY_MINS * 60:
        for each_obj in otp_obj_list:
          each_obj.is_expired = True
          each_obj.save()
        return False
      return True
    return False

  def otp_generated(self):
    otp_obj_list = AttendanceOTP.objects.exclude(is_expired = True)\
        .filter(timetable = self, created_at__date = datetime.datetime.now().date() ).order_by('-created_at')
    if len(otp_obj_list):
      return otp_obj_list[0].otp
    return 'OTP Expired!'

  def remaining_seconds(self):
    otp_obj_list = AttendanceOTP.objects.exclude(is_expired = True)\
        .filter(timetable = self, created_at__date = datetime.datetime.now().date() ).order_by('-created_at')
    if len(otp_obj_list):
      otp_obj = otp_obj_list[0]
      currentdt = datetime.datetime.now() # timezone.now()
      return int(settings.OTP_EXPIRY_MINS * 60 - (currentdt - otp_obj.created_at).total_seconds())
    return 0

  def get_time_string(self):
    if self.get_css_on_class_type() != 'normal_text':
      return ''
    return '%s - %s' %( self.time_start.strftime('%I:%M %p'), self.time_end.strftime('%I:%M %p') )

  def get_css_on_class_type(self):
    if self.class_type == '5':
      return 'turn_ninety'
    elif self.class_type == '6':
      return 'turn_ninety'
    return 'normal_text'

  def get_class_type_icon_class(self):
    if self.class_type == '1':
      return 'fa fa-clipboard green-icon'
    elif self.class_type == '2':
      return 'fa fa-th blue-icon'
    elif self.class_type == '3':
      return 'fa fa-flask orange-icon'
    if self.class_type == '5':
      return 'fa fa-cutlery red-icon'
    if self.class_type == '6':
      return 'fa fa-coffee'
    return 'fa fa-user-plus yellow-icon'

class YouTubeLiveEvent(models.Model):
  title = models.CharField(_("Event Title"), max_length = 100, blank = True, null = True)
  description = models.TextField(blank = True)
  yt_dump = models.TextField(blank = True)
  embed_code = models.CharField(_("Embed Code"), max_length = 100, blank = True, null = True)
  start_time = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True)
  is_draft = models.BooleanField(_("Draft? "), default=False,\
      help_text=_("Can make it live Later! Users will not see this record until this checkbox is checked."))
  is_public = models.BooleanField(_("Make it public?"), default=False)
  
  is_access_given = models.BooleanField(_("Give Access to All Students?"), default=False,\
    help_text=_("This will be visible to students in Old events Section. Uncheck to Revoke! Make sure that the Event is in Draft Mode!"))
  access_expires = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True, 
    help_text=_("Access will be expired after this time. Default: Today at 11:59:59PM. Leave blank for default value."))

  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  channel_id = models.CharField(_("Channel ID"), max_length = 100, blank = True, null = True)
  ####### target_audience ####### 
  institute = models.ForeignKey(Institute, unique=False, blank=True, null=True)
  course_name = models.ForeignKey('Course', blank = True, null = True, related_name = 'yt_course')
  branch = models.ForeignKey('Branch', blank = True, null = True, related_name = 'yt_branch')
  sem_no = models.CharField(_('Semester'), choices = SEM_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  year_no = models.CharField(_('Year'), choices = YEAR_NO_CHOICES, max_length = 10, blank = True, null = True, default = "")
  subject = models.ForeignKey('Subject', blank = True, null = True, related_name = 'yt_subject')

  def __unicode__(self):
    return str(self.id)

class AttendanceOTP(models.Model):
  timetable = models.ForeignKey('TimeTable', blank = True, null = True)
  faculty = models.ForeignKey('Faculty', blank = True, null = True)
  otp = models.CharField(_("OTP"), max_length = 300, blank = True, null = True)
  created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True, editable = False)
  is_expired = models.BooleanField(default = False)
  
  def __unicode__(self):
    return str(self.otp)

  def save(self, *args, **kwargs):    
    if not self.created_at:
      self.created_at = datetime.datetime.now()
    super(AttendanceOTP, self).save(*args, **kwargs)

  def remaining_seconds(self):
    currentdt = datetime.datetime.now() # timezone.now()
    return int(settings.OTP_EXPIRY_MINS * 60 - (currentdt - self.created_at).total_seconds())
    
class Attendance(models.Model):
  timetable = models.ForeignKey('TimeTable', blank = True, null = True, related_name="attendance_timetable")
  student = models.ForeignKey(User, blank = True, null = True, related_name="attendance_user")
  is_present = models.BooleanField(default = False)
  is_manual = models.BooleanField(default = False)
  otp_validated = models.ForeignKey(AttendanceOTP, blank = True, null = True, related_name="attendance_otp") 
  faculty = models.ForeignKey('Faculty', blank = True, null = True, related_name="attendance_faculty")
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  created_date = models.DateField(auto_now_add=True, blank=True, null=True)

  def __unicode__(self):
    return str(self.id)

  def save(self, *args, **kwargs):
    description = ''
    title = ''
    present_str = 'absent'
    created_str = 'Created'
    by_str = 'Face Recog'
    if self.pk:
      created_str = 'Updated'

    if self.is_present:
      present_str = 'present'

    if self.is_manual:
      by_str = self.faculty.get_full_name()

    title = '[' + created_str + ']: Attendance Marked as ' + present_str + '!'
    description = 'Attendance for Class: ' + self.timetable.display_name() + ' is marked ' + present_str + ' by ' + by_str + \
      ' at ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notification = Notification.objects.create( title = title, for_individual = True, individual_user = self.student,\
      category = NotificationCategory.objects.get(id = 2), related_object = self, description = description, is_live = True)
    super(Attendance, self).save(*args, **kwargs)

class StudentLiveClassAcess(models.Model):
  class_obj = models.ForeignKey(YouTubeLiveEvent, blank = True, null = True)
  student = models.ForeignKey(UserProfile, blank = True, null = True)
  access_expires = models.DateTimeField(auto_now_add=False, auto_now = False, blank=True, null=True, 
    help_text=_("Access will be expired after this time. Default: Today at 11:59:59PM. Leave blank for default value."))

  def __unicode__(self):
    return str(self.student)

class StudentLiveEventCount(models.Model):
  user = models.ForeignKey(User, blank = True, null = True)
  event = models.ForeignKey(YouTubeLiveEvent, blank = True, null = True)
  start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
  last_record_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

  def __unicode__(self):
    return str(self.user.id)

  def get_start_time(self):
    if self.start_time:
      return self.start_time.strftime('%d-%m-%Y %H:%M:%S')
    return ' - '

  def get_last_record_time(self):
    if self.last_record_time:
      return self.last_record_time.strftime('%d-%m-%Y %H:%M:%S')
    return ' - '


