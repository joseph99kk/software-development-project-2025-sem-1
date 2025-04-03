from django.db import models

# Create your models here.

class Token(models.Model):
    id=models.Autofield(primary_key=True)
    token=models.CharField(max_length=255)
    created_at=models.DateTimeField()
    expires_at=models.DateTimeField()
    user_id=models.integerField()
    is_used=models.BooleanField(defaulf=False)


class User(models.Model):
    id =models.AutoField(primary_key=True)
    name=models.CharField(mav_length=255)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=10, null=True)
    program=models.CharField(max_length=255)
    year_of_study=models.CharField(max_length=255)
    college=models.CharField(max_length=255)
    school=models.CharField(max_length=255)



    def __str__(self) -> str:
        return self.name