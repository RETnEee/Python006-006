from index.models import Comment, Film
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse
def film(request):
    f = Film.objects.filter(Q(name__exact=request.GET.get('q'))).first()
    c = Comment.objects.filter(Q(rank__gte=3)&~Q(filmname__exact=request.GET.get('q')))
    return render(request, "frontend/index.html", locals())