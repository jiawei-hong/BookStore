from django.contrib import admin
from .models import Books


# Register your models here.


class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id')


admin.site.register(Books, BooksAdmin)
