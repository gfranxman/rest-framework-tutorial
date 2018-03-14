from django.db import models
from multiselectfield import MultiSelectField
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
MULTI_CHOICES = [('CA', 'California'),
                 ('OR', 'Oregon'),
                 ('WA', 'Washington'),
                 ('0', 'Zero'),
                 ('1', 'One'),
                 ('2', 'Two'),
                 ('3', 'Three'),
                 ('3.5', 'Three-point-five'),
                 ('10', 'Ten'),
                 ('True', 'True'),
                 ('False', 'False'),
                 ]


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100)
    owner = models.ForeignKey('auth.User',
                              related_name='snippets',
                              on_delete=models.CASCADE)
    highlighted = models.TextField()
    multiselect = models.CharField(choices=MULTI_CHOICES,
                                   max_length=100,
                                   default='')
    mselect = MultiSelectField(choices=MULTI_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

        # limit the number of instances retained
        snippets = Snippet.objects.all()
        if len(snippets) > 100:
            snippets[0].delete()
