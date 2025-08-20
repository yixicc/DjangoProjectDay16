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
    create_time = models.DateTimeField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE) #级联删除
    # depart = models.ForeignKey(to="Department",to_field="id",null=True,blank=True,on_delete=models.SET_NULL()) #置空删除
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    gender = models.IntegerField(verbose_name="性别",choices=gender_choices, default=1)

class PrettyNum(models.Model):
    mobile = models.CharField(max_length=20,verbose_name="号码")
    price = models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2,default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级")
    )
    level = models.IntegerField(verbose_name="级别",choices=level_choices, default=1)
    status_choices = (
        (1,"未占用"),
        (2,"已占用")
    )
    status = models.IntegerField(verbose_name="占用状态",choices=status_choices, default=1)

class Admin(models.Model):
    '''管理员'''
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    def __str__(self):
        return self.username


class Task(models.Model):
    """任务"""
    level_choices = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
    )

    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题",max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人",to="Admin",on_delete=models.CASCADE)


class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1,"待支付"),
        (2,"已支付"),
    )

    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)