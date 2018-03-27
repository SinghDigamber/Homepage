from django.shortcuts import render
from .models import Alternative, Сriterion, Mark, Vector, LPR, Result
from django.views.generic import ListView
# Create your views here.


class university_TItaPIndexView(ListView):
    model = Alternative
    template_name = "university_TItaP/index.html"
    context_object_name = "list"

    def get_queryset(self):
        result = {
            'items': [],
            'header': ["Имя"]
        }

        for vector in list(Сriterion.objects.filter()):
            result['header'].append(vector.CName)

        for item in list(Alternative.objects.all()):
            temp = []

            temp.append(str(item))
            for vector in list(Vector.objects.filter(IdAlt=item)):
                temp.append(vector.IdMark.MName)


            result['items'].append(temp)

        return result
