from django import forms
from .models import Merch, Category, Collection


class MerchSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].label = False
        self.fields["q"].widget.attrs.update({"class": "form-control"})


class MerchForm(forms.ModelForm):

    class Meta:
        model = Merch
        fields = ('product_name', 'slug',
                  'description', 'price', 'in_stock',
                  'hot_item', 'category', 'collection',
                  'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        collections = Collection.objects.all()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
