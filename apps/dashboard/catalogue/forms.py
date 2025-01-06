from django import forms
from oscar.core.loading import get_model

AttributeOption = get_model('catalogue', 'AttributeOption')

class AttributeOptionForm(forms.ModelForm):
    class Meta:
        model = AttributeOption
        fields = ['option', 'price']
