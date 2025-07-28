from django.db import models

# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=120,verbose_name="部门名称")

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=20,verbose_name="姓名")
    password = models.CharField(max_length=120,verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间",auto_now=True)
    depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE) #级联删除
    # depart = models.ForeignKey(to="Department",to_field="id",null=True,blank=True,on_delete=models.SET_NULL()) #置空删除
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    gender = models.IntegerField(verbose_name="性别",choices=gender_choices, default=1)