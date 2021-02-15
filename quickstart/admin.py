from django.contrib import admin
from django.forms import ModelForm
from . import models
from quickstart.models import *
from django.contrib import admin
from datetime import timezone, datetime

from django.template.response import TemplateResponse
from quickstart.forms import MyPostAdminForm, MyFileAdminForm
from django.conf.urls import url
from django.contrib.contenttypes.admin import GenericTabularInline

class FileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['file_origin_name']}),
        ('Date information', {'fields': ['file_path']})
    ]

    list_display = ('file_origin_name', 'file_path', 'file_ext', 'is_img', 'create_date')

    def was_published_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'create_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '  '

    list_filter = ['create_date']

    search_fields = ['file_origin_name', 'create_date']


def make_published(modeladmin, request, queryset):
    queryset.update(count=5) # 3
make_published.short_description = "Mark selected stories as published"


import markdown

class CSSAdminMixin(object):
    class Media:
        css = {
            'all': ['css/admin/styles.css']
        }
        js = ['js/admin/styles.js']

class BlogAdmin(admin.ModelAdmin, CSSAdminMixin):

    actions = [make_published]
    # readonly_fields = ['use_yn']

    fields = [
                  'name'
                , 'content'
                , 'tagline'
                , 'tagline1'
                , 'taglineqwe'
                , 'FileEntry'
                , 'count'
                , 'view_count'
                , 'qwer_yn'
                , 'use_yn'

          ]

    readonly_fields = ('tagline1',)

    def tagline1(self, instance):
        return mark_safe(markdown.markdown(instance.tagline, extensions=["fenced_code"]))

    def get_urls(self):
        urls = super(BlogAdmin, self).get_urls()
        post_urls = [
            url(r'^status/$', self.admin_site.admin_view(self.post_status_view))
        ]
        return post_urls + urls

    def post_status_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            posts=Blog.objects.all()
        )
        print('context : ', context)
        return TemplateResponse(request, "admin/post_status.html", context)


from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe

class FileEntryAdmin(admin.ModelAdmin):
    form = MyFileAdminForm

    fieldsets = [
        (None, {'fields': ['file_ext']}),
        ('Date information', {'fields': ['file_path', 'new_name']})
    ]

    readonly_fields = ('new_name',)


    # list_display = ('file_origin_name', 'file_path', 'file_ext', 'is_img', 'create_date')

    # def was_published_recently(self):
    #     return self.create_date >= timezone.now() - datetime.timedelta(days=1)
    #
    # was_published_recently.admin_order_field = 'create_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = '  '
    #
    # list_filter = ['create_date']
    #
    # search_fields = ['file_origin_name', 'create_date']

class AddFileInline(admin.TabularInline):
    model = AddFile
    fk_name = "board"
    exclude = ['file_ext', 'file_name']

class BoardAdmin(admin.ModelAdmin):
    fields = ['title', 'content']

    inlines = [
        AddFileInline,
    ]


class FileInline(GenericTabularInline):
    model = File
    # form = TbattachFileForm
    ct_field = "content_type"
    ct_fk_field = "object_id"
    fk_name = "content_object"
    fields = ('file_path', )


class BoardTest1Admin(admin.ModelAdmin):
    fields = ['name']
    inlines = [
            FileInline,
    ]


admin.site.register(FileModel, FileAdmin)
# admin.site.register(models.Dog)
# admin.site.register(models.FileEntry, FileEntryAdmin)
# admin.site.register(models.Blog, BlogAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardTest1, BoardTest1Admin)
admin.site.register(AddFile)

admin.site.register(Academy)
admin.site.register(Teacher)
admin.site.register(Subject)