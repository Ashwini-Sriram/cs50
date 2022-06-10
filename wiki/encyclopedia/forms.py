from django import forms

class search_form(forms.Form):
    search=forms.CharField(max_length=64,widget=forms.TextInput(attrs={'class':'search','placeholder':'Search Encyclopedia'}))

class create_form(forms.Form):
    title = forms.CharField(max_length=64,widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    text = forms.CharField(max_length=400000,widget=forms.Textarea(attrs={'placeholder':'Enter text'})) 

