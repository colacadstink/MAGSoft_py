# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import timedelta, datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.base import ModelBase

PHONE_VALIDATOR = RegexValidator(regex=r'^[-+0-9]{10,}$')


class KeyValueModel(ModelBase):
    def __len__(cls):
        return cls.objects.count()

    def __getitem__(cls, key):
        try:
            return cls.objects.get(key=key).value
        except ObjectDoesNotExist:
            raise KeyError(key)

    def __setitem__(cls, key, value):
        cls.objects.update_or_create(key=key, value=value)

    def __delitem__(cls, key):
        count = cls.objects.filter(key=key).delete()[0]
        if count != 1:
            raise KeyError(key)

    def __iter__(cls):
        return cls.objects.all()

    def __contains__(cls, key):
        return cls.objects.filter(key=key).count() == 1


class Alerts(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.ForeignKey('Users', models.CASCADE, to_field='email', db_column='email')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=5000)
    location = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'alerts'


class Badges(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.ForeignKey('Users', models.DO_NOTHING, to_field='email', db_column='email')
    zip = models.IntegerField()
    extra = models.SmallIntegerField()
    shirt = models.IntegerField()
    badgename = models.CharField(db_column='badgeName', max_length=255)  # Field name made lowercase.
    spam = models.IntegerField()
    badgeadded = models.IntegerField(db_column='badgeAdded')  # Field name made lowercase.
    badgedata = models.CharField(db_column='badgeData', max_length=255)  # Field name made lowercase.
    year = models.SmallIntegerField()

    class Meta:
        db_table = 'badges'
        unique_together = (('email', 'year'),)


class Canroompreauth(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'canRoomPreAuth'


class Passwordreset(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.OneToOneField('Users', models.CASCADE, db_column='email')
    resetstring = models.CharField(db_column='resetString', max_length=64)  # Field name made lowercase.
    generated = models.DateTimeField()

    class Meta:
        db_table = 'passwordReset'


class Roominfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.ForeignKey('Users', models.DO_NOTHING, to_field='email', db_column='email')
    year = models.IntegerField()
    night = models.CharField(max_length=255)
    numnights = models.IntegerField(db_column='numNights')  # Field name made lowercase.
    roomnumber = models.CharField(db_column='roomNumber', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'roomInfo'
        unique_together = (('email', 'year', 'night'),)


class Roommates(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.ForeignKey('Users', models.DO_NOTHING, to_field='email', db_column='email')
    year = models.IntegerField()
    wantstoroom = models.IntegerField(db_column='wantsToRoom')  # Field name made lowercase.
    likes = models.CharField(max_length=10000)
    dislikes = models.CharField(max_length=10000)
    nights = models.CharField(max_length=3)
    smallroom = models.CharField(db_column='smallRoom', max_length=8)  # Field name made lowercase.
    atrium = models.CharField(max_length=8)
    parties = models.IntegerField()
    allergies = models.CharField(max_length=1000)
    comments = models.CharField(max_length=10000)

    class Meta:
        db_table = 'roommates'
        unique_together = (('email', 'year'),)


class Settings(models.Model, metaclass=KeyValueModel):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    comment = models.CharField(max_length=255)

    class Meta:
        db_table = 'settings'


class Tab(models.Model):
    tid = models.AutoField(primary_key=True)
    email = models.ForeignKey('Users', models.DO_NOTHING, to_field='email', db_column='email')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    when = models.CharField(max_length=10)
    housecharge = models.IntegerField(db_column='houseCharge')  # Field name made lowercase.
    notes = models.CharField(max_length=4095)

    class Meta:
        db_table = 'tab'


class Users(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    first_name = models.CharField(db_column='firstName', max_length=255)  # Field name made lowercase.
    last_name = models.CharField(db_column='lastName', max_length=255)  # Field name made lowercase.
    is_staff = models.BooleanField(db_column='isAdmin', default=False)  # Field name made lowercase.

    limbopassword = models.CharField(db_column='limboPassword', default='', max_length=128)  # Field name made lowercase.
    phone = models.CharField(max_length=31, blank=False, validators=[PHONE_VALIDATOR])
    emergencyname = models.CharField(db_column='emergencyName', max_length=255, blank=False)  # Field name made lowercase.
    emergencyphone = models.CharField(db_column='emergencyPhone', max_length=31, blank=False, validators=[PHONE_VALIDATOR])  # Field name made lowercase.
    dob = models.DateField(blank=False)
    profilepic = models.CharField(db_column='profilePic', default='', max_length=512)  # Field name made lowercase.
    canroom = models.BooleanField(db_column='canRoom', default=False)  # Field name made lowercase.
    newuser = models.BooleanField(db_column='newUser', default=True)  # Field name made lowercase.

    is_active = True
    is_anonymous = False
    is_authenticated = True

    def clean(self):
        if self.phone==self.emergencyphone:
            raise ValidationError("You cannot be your own emergency contact!")

    def create(self, validated_data):
        #TODO: Test this logic; eventually replace it with a canLogin flag.
        if datetime.today() - validated_data.dob < timedelta(years=18):
            validated_data.limbopassword=validated_data.password
            validated_data.password=''
        super(Users, self).create(validated_data)

    def get_full_name(self):
        return self.first_name+" "+self.last_name

    def get_short_name(self):
        return self.first_name

    def get_alerts(self):
        return Alerts.objects.all().filter(email=self.email)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'phone', 'emergencyname', 'emergencyphone', 'dob']

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    class Meta:
        db_table = 'users'
