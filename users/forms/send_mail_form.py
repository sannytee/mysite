from django import forms


class MailForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)