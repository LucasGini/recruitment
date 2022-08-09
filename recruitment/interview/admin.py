from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from interview import models
from django.http import HttpResponse
from django.contrib import messages
# Register your models here.
from datetime import datetime
from .tasks import sen_dingtalk_message
from interview.models import Candidate
import logging
import csv
from interview.candidate_fieldset import default_fieldsets_frist, default_fieldsets_second, default_fieldsets
from jobs.models import Resume

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')


def notify_interviewer(modelamin, request, queryset):
    candidates = ""
    interviewer = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewer = obj.first_interviewer_user.useraname + ";" + interviewer
    sen_dingtalk_message.delay("候选人%s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewer))
    messages.add_message(request, messages.INFO, '已经成功发送面试通知')


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    logger.info("%s exported %s candidate records" %(request.user, len(queryset)))

    return response


export_model_as_csv.short_description = '导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)


class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv, notify_interviewer]

    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, 'export'))

    list_display = (
        'username', 'city', 'bachelor_school', 'get_resume', 'first_score', 'first_result', 'first_interviewer_user', 'second_score',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user')

    search_fields = ('username', 'phone', 'email', 'bachelor_school',)

    ordering = ('hr_result', 'second_result', 'first_result')

    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe('<a href="/resume/%s" target="_blank">%s</a>' % (resumes[0].id, '查看简历'))
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True

    default_list_editable = ['first_interviewer_user', 'second_interviewer_user']
    # readonly_fields = ['first_interviewer_user', 'second_interviewer_user']

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_name = []
        for g in user.groups.all():
            group_name.append(g.name)
        return group_name

    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return CandidateAdmin.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('frist_interviewer_user', 'second_interviewer_user',)
        return ()

    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_frist
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets


admin.site.register(models.Candidate, CandidateAdmin)