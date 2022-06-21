from django import forms
class createListings(forms.Form):
    title = forms.CharField(label="Enter Title",max_length=64)
    text_desc = forms.CharField(label="Enter Description",max_length=256)
    start_bid= forms.FloatField(label="Enter Starting Bid")
    img_url = forms.CharField(label="Insert Images URL",max_length=256,required=False)
    
    

