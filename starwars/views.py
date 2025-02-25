from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .models import Collection
from .service import fetch_collection
from .tables import PersonTable, PersonTableWithCount


class CollectionsView(ListView):
    model = Collection
    template_name = "starwars/collections.html"
    context_object_name = "collections"

    def post(self, request):
        fetch_collection()
        return redirect("collections")


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "starwars/collection_detail.html"
    context_object_name = "collection"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the selected columns from the query string
        group = self.request.GET.getlist("group")

        # Create a list of dictionaries with the column names and whether they are active
        columns = [
            {"name": c, "active": c in group}
            for c in PersonTable.base_columns.keys()
            if c != "count"
        ]
        context["columns"] = columns

        # Get the data from the collection
        data = self.object.get_data()
        if group:
            # Group the data by the selected columns
            df_grouped = data.aggregate(key=group, aggregation=len, field="count")
            table = PersonTableWithCount(
                df_grouped.dicts(),
                exclude=[c["name"] for c in columns if not c["active"]],
            )
        else:
            # Show the data as is
            table = PersonTable(data.dicts())
            table.paginate(page=self.request.GET.get("page", 1), per_page=10)

        context["table"] = table
        return context
