from io import StringIO
from django.core.management.commands.dumpdata import Command as Dumpdata


class Command(Dumpdata):
    """
    Get readable data in the dumpdata output
    https://djangosnippets.org/snippets/10625/
    """
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--pretty', default=False, action='store_true',
            dest='pretty', help='Avoid unicode escape symbols'
        )

    def handle(self, *args, **kwargs):
        captcha_stdout = StringIO()
        old_stdout = self.stdout
        self.stdout = captcha_stdout
        super(Command, self).handle(*args, **kwargs)
        captcha_stdout.seek(0)
        data = captcha_stdout.read()
        data = data.encode()
        if kwargs.get('pretty'):
            data = data.decode("unicode_escape").encode("utf-8")
        old_stdout.write(data.decode('utf-8'))
