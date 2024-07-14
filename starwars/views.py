from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .etl import fetch
from .models import Collection
from .tables import PersonTable


class CollectionsView(ListView):
    model = Collection
    template_name = "starwars/collections.html"
    context_object_name = "collections"

    def post(self, request):
        file_name = fetch()
        Collection(file=file_name).save()
        return redirect("collections")


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "starwars/collection_detail.html"
    context_object_name = "collection"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = self.request.GET.getlist("group")
        columns = [
            {"name": c, "active": c in group}
            for c in PersonTable.base_columns.keys()
            if c != "count"
        ]
        context["columns"] = columns

        data = self.object.get_data()
        if group:
            df_grouped = data.aggregate(key=group, aggregation=len, field="count")
            table = PersonTable(
                df_grouped.dicts(),
                exclude=[c["name"] for c in columns if not c["active"]],
            )
        else:
            table = PersonTable(data.dicts(), exclude=["count"])
            table.paginate(page=self.request.GET.get("page", 1), per_page=10)

        context["table"] = table
        return context
