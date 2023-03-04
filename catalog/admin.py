from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *

class BookForm(forms.Form):

    summary = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Book
        fields = '__all__'
class BookInline(admin.StackedInline):
    model = Book
    pk_name = 'author'

class AuthorAdmin(admin.ModelAdmin):
    inlines = (BookInline,)

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    search_fields = ["title"]
    readonly_fields = ["avatar"]

    forms = BookForm()

    def avatar(self, book):
        return mark_safe("<img src = '/static/{img_url}' width = '120px'/>".format(img_url= book.image.name))

    class Media:
        css = {
            'all' : ('/static/css/admin.css',)
        }


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Comment)
admin.site.register(User)


