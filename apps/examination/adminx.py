# _*_ coding:utf-8 _*_
import xadmin
from .models import Examination


class ExaminationAdmin(object):
    list_display = ['name', 'edit_questionnaire', 'show_questionnaire']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'
    # 不显示字段
    exclude = ['take_nums']
    # 根据更新时间倒序
    ordering = ['-update_time']

    def queryset(self):
        # super调用方法
        qs = super(ExaminationAdmin, self).queryset()
        qs = qs.filter(is_published=False)
        return qs