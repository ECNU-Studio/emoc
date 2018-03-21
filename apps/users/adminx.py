# _*_ coding:utf-8 _*_
import xadmin
from xadmin import views
from .models import EmailVerifyRecord
from .models import Banner


class BaseSetting(object):
    # enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '时时课课后台管理系统'
    site_footer = '时时课课'
    # menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fas fa-envelope'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fas fa-images'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

xadmin.site.register(Banner, BannerAdmin)


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
