import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelFormAdminView, UpdateAdminView
from mdeditor.fields import MDTextField
from mdeditor.widgets import MDEditorWidget
from django.conf import settings


class XadminMDEditorWidget(MDEditorWidget):
    def __init__(self,**kwargs):
        self.mdeditor_options=kwargs
        self.Media.js = None
        super(XadminMDEditorWidget,self).__init__(kwargs)


class MDeditorPlugin(BaseAdminPlugin):
    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'mdeditor':
            if isinstance(db_field, MDTextField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.mdeditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminMDEditorWidget(**param)}
        return attrs


xadmin.site.register_plugin(MDeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(MDeditorPlugin, CreateAdminView)
