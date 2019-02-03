from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text = "Please enter the category name.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget = forms.HiddenInput(), required = False)

    #an incline class to provide additional information on the forms.
    class Meta:
        #provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "Please enter the title of the page.")
    url = forms.URLField(max_length = 200, help_text = "Please enter the URL of the page.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        #if url is not empty and doesn't start with 'http://',
        #then prepend 'http://'

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        #provide an association between the ModelForm and a model
        model = Page
        #what fields do we want to include in our form?
        #this way we don't need every field in the model present.
        #some fields may allow NULL values, so we may not want to include them.
        #here, we are hiding the foreign key.
        #we can either exclude the category field from the form,
        exclude = ("category",)
        #or spexify the fields to include(i.e. not include the category field)
        #fields = ("title", "url", "views")
