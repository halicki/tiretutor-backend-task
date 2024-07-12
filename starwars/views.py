from django.shortcuts import render
from django.views.generic import ListView

from starwars.models import Collection


class CollectionsView(ListView):
    model = Collection
    template_name = "starwars/collections.html"
    context_object_name = "collections"

    def post(self, request):
        return render(request, "starwars/collections.html")