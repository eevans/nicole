
from django.forms import Form, CharField, Textarea, TextInput, IntegerField, \
                         HiddenInput

class BlogEntryForm(Form):
    entry_id = IntegerField(widget=HiddenInput(attrs={'value': 0}))
    title = CharField(widget=TextInput(attrs={'size': 60}), max_length=128)
    content = CharField(widget=Textarea(attrs={'rows': 24, 'cols': 80}))
    tags = CharField(widget=TextInput(attrs={'size': 40}), required=False, 
            max_length=128)

# vi:ai sw=4 ts=4 tw=0 et
