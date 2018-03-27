from django.contrib import admin
from .models import Alternative, Сriterion, Mark, Vector, LPR, Result
# Register your models here.


class AlternativeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['AName']}),
    ]
admin.site.register(Alternative, AlternativeAdmin)


class СriterionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['CName', 'CRange', 'CWeight', 'CType', 'OptimType', 'EdIzmer', 'ScaleType']}),
    ]
admin.site.register(Сriterion, СriterionAdmin)


class MarkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['IdCrit', 'MName', 'MRange', 'NumMark', 'NormMark']}),
    ]
admin.site.register(Mark, MarkAdmin)


class VectorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['IdAlt', 'IdMark']}),
    ]
admin.site.register(Vector, VectorAdmin)


class LPRAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['LName', 'LRange']}),
    ]
admin.site.register(LPR, LPRAdmin)


class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['IdLPR', 'IdAlt', 'Range', 'AWeight']}),
    ]
admin.site.register(Result, ResultAdmin)