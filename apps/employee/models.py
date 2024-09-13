from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from apps.company.models import OfficeDepartment
from kaazinihrms import settings
from datetime import datetime

class Employee(models.Model):
    MARITAL_STATUS = (
        ('single', 'Single'),
        ('married', 'Married'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, editable=False)
    employee_email = models.EmailField()
    employee_phone = PhoneNumberField()
    employee_dob = models.DateField(default=datetime.now, blank=True)
    place_of_birth = models.CharField(max_length=150) 
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS)
    profile_pic = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    office_department = models.ForeignKey(OfficeDepartment, on_delete=models.CASCADE, default=1)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subordinates', blank=True, null=True)
    home_town = models.CharField(max_length=150)
    date_joined = models.DateField(auto_now = True)
  
    
    def __str__(self) -> str:
        return f'{self.user.username} {self.user.second_name}'
    
    @property
    def employee_age(self):
        return datetime.now().year - int(self.employee_dob.strftime('%Y'))
    

class EmployeeTitle(models.Model):
    EDUCATION_LEVEL = (
        ('doctorate degree', 'Doctorate Degree'),
        ('masters degree', 'Masters Degree'),
        ('bachelors degree', 'Bachelors Degree'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    )
    title_name = models.CharField(max_length=150)
    education_level = models.CharField(max_length=150, choices=EDUCATION_LEVEL, blank = False, default='certificate')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title_name
    

class EmployeeContract(models.Model):
    CONTRACT_STATUS = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    EMPLOYEMENT_TYPE = (
        ('hire', 'Hire'),
        ('contract', 'Contract'),
    )
    COMMITMENT_TYPE = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    )
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    title = models.ForeignKey(EmployeeTitle, on_delete=models.CASCADE, default=1)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(default=datetime.now, blank=True)
    probation_start = models.DateField(default=datetime.now, blank=True)
    probation_end = models.DateField(default=datetime.now, blank=True)
    type_of_employement = models.CharField(max_length=100, choices=EMPLOYEMENT_TYPE, default='Hire')
    type_of_commitment = models.CharField(max_length=100, choices=COMMITMENT_TYPE, default='Full Time')
    contract_status = models.CharField(max_length=100, choices=CONTRACT_STATUS, default='pending')
    date_created = models.DateField(auto_now = True)

    def __str__(self) -> str:
        return f'{self.employee} - {self.title.title_name}'
    