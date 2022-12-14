from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from interview.models import DEGREE_TYPE
# Create your models here.


JobTypes = [
    (0, '技术类'),
    (1, '产品类'),
    (2, '运营类'),
    (3, '设计类')
]

Cities = [
    (0, '北京'),
    (1, '上海'),
    (2, '深圳')
]


class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name='职位类别')
    job_name = models.CharField(max_length=256, blank=False, verbose_name='职位名称')
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name='工作地点')
    job_reponsibility = models.TextField(max_length=1024, verbose_name='职位职责')
    job_requirement = models.TextField(max_length=1024, verbose_name='职位要求', blank=False)
    creator = models.ForeignKey(User, verbose_name='创建人', on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(verbose_name='创建日期', default=timezone.now)
    modified_date = models.DateTimeField(verbose_name='修改时间', default=timezone.now)

    class Meta:
        verbose_name = '职位'
        verbose_name_plural = '职位列表'


class Resume(models.Model):
    username = models.CharField(max_length=128, verbose_name='姓名')
    applicant = models.ForeignKey(User, verbose_name='申请人', null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=128, verbose_name='城市')
    phone = models.CharField(max_length=128, verbose_name='手机号')
    email = models.EmailField(max_length=128, verbose_name='邮箱')
    apply_position = models.CharField(max_length=128, verbose_name='应聘职位')
    born_address = models.CharField(max_length=128, blank=True, verbose_name='生源地')
    gender = models.CharField(max_length=128, blank=True, verbose_name='性别')

    picture = models.ImageField(upload_to='images/', blank=True, verbose_name='个人照片')
    attachment = models.FileField(upload_to='file/', blank=True, verbose_name='简历附件')

    # 学习与学历信息
    bachelor_school = models.CharField(max_length=128, blank=True, verbose_name='本科学校')
    master_school = models.CharField(max_length=128, blank=True, verbose_name='研究生学校')
    doctor_school = models.CharField(max_length=128, blank=True, verbose_name='博士生学校')
    major = models.CharField(max_length=128, blank=True, verbose_name='专业')
    degree = models.CharField(max_length=128, choices=DEGREE_TYPE, blank=True, verbose_name='学历')
    create_date = models.DateTimeField(verbose_name='创建日期', default=timezone.now)
    modified_date = models.DateTimeField(verbose_name='修改日期', default=timezone.now)

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name='自我介绍')
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name='工作经历')
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name='项目经历')

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = '简历列表'