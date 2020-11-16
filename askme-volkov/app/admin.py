from django.contrib import admin
from app.models import Author
from app.models import Question
from app.models import Answer
from app.models import Tag
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass
class QuestionAdmin(admin.ModelAdmin):
    pass
class AnswerAdmin(admin.ModelAdmin):
    pass
class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag, TagAdmin)