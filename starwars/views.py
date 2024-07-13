from django.shortcuts import redirect
from django.views.generic import ListView

from starwars.models import Collection
from .etl import fetch


class CollectionsView(ListView):
    model = Collection
    template_name = "starwars/collections.html"
    context_object_name = "collections"

    def post(self, request):
        file_name = fetch()
        Collection(file=file_name).save()
        return redirect("collections")
