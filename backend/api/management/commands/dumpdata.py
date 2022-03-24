# from django.core import serializers
from django.core.management.base import CommandError
from django.core.management.commands.dumpdata import Command as Dumpdata

from api import utilities


class Command(Dumpdata):
    """
    https://docs.djangoproject.com/en/3.0/ref/django-admin/#dumpdata
    https://github.com/django/django/blob/master/django/core/management/commands/dumpdata.py

    Custom --pretty argument (old)
    Get readable data in the dumpdata output https://djangosnippets.org/snippets/10625/

    Usage example:
    python manage.py dumpdata api.question > ../data/questions.yaml
    python manage.py dumpdata api.question --format=yaml --output=../data/questions.yaml
    python manage.py dumpdata api.question --format=yaml-pretty --output=../data/questions.yaml
    python manage.py dumpdata api.question --format=yaml-pretty-flat --output=../data/questions.yaml
    """

    def handle(self, *app_labels, **options):
        # pretty: allow_unicode to have a clean and readable output
        # flat: output with 'model', 'pk' and 'fields' keys
        if options.get("format").startswith("yaml-"):
            # init
            if (len(app_labels) == 0) or (len(app_labels) > 1):
                raise CommandError("Error with app_labels. Only 1 'app.model' possible.")
            # get input model
            app_label, model_label = app_labels[0].split(".")
            # model = apps.get_app_config(app_label).get_model(model_label)
            # init output
            output = options["output"]
            stream = open(output, "w") if output else None
            # yaml + pretty : call django serializer
            if options.get("format") == "yaml-pretty":
                utilities.serialize_model_to_yaml(app_label, model_label, stream=stream or self.stdout)
            # yaml + pretty + flat : call pyyaml
            elif options.get("format") == "yaml-pretty-flat":
                utilities.serialize_model_to_yaml(app_label, model_label, flat=True, stream=stream or self.stdout)
        else:
            super(Command, self).handle(*app_labels, **options)
