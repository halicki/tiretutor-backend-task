import django_tables2 as tables


class PersonTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap.html"
        orderable = False

    name = tables.Column()
    height = tables.Column()
    mass = tables.Column()
    hair_color = tables.Column()
    skin_color = tables.Column()
    eye_color = tables.Column()
    birth_year = tables.Column()
    gender = tables.Column()
    date = tables.Column()
    homeworld = tables.Column()
    count = tables.Column()
