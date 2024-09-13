from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    COMPANY_TYPE = (
        ('private company', 'Private Company'),
        ('non-governmental', 'Non-Governmental'),
    )
    company_name = models.CharField(max_length=125, unique=True)
    company_type = models.CharField(choices=COMPANY_TYPE)
    company_email = models.EmailField(unique=True, max_length=125)
    company_phone = PhoneNumberField(blank=True, null=True)
    company_website = models.URLField(max_length = 200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='media/company_photos', blank=True, null=True)
    created_date = models.DateField(auto_now = True)
    


    def __str__(self) -> str:
        return self.company_name


class Office(models.Model):
    office_name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    created_date = models.DateField(auto_now = True)
    # office_department = models.ManyToManyField(Office, through='OfficeDepartment',  through_fields=('office','department'),related_name='office_department')

  
    def __str__(self) -> str:
        return self.office_name
       

class Department(models.Model):
    department_name = models.CharField(max_length=125)
    created_date = models.DateField(auto_now = True)


    def __str__(self) -> str:
        return self.department_name
    
class OfficeDepartment(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now = True)

    def __str__(self) -> str:
        return f'{self.office} {self.department}'