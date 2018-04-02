from django.shortcuts import render
from .models import Alternative, Сriterion, Mark, Vector, LPR, Result
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
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
                temp.append(vector)

            result['items'].append(temp)

        return result

class VectorUpdateView(UpdateView):
    model = Vector
    template_name = "university_TItaP/vector_update.html"
    fields = ['IdAlt', 'IdMark']
    success_url = reverse_lazy('university_TItaP:index')

class VectorIndexView(ListView):
    model = Vector
    template_name = "university_TItaP/vector_index.html"
    context_object_name = "list"

    def get_queryset(self):
        temp = Vector.objects.get(pk=self.kwargs['pk'])
        return list(Vector.objects.filter(IdAlt=temp.IdAlt))
