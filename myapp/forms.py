from django import forms
from myapp.models import Employee
class EmployeeForm(forms.ModelForm):
    def clean_esal(self):
        inputsal=self.cleaned_data['esal']
        if inputsal < 5000:
            raise forms.ValidationError('The minimum salary should be more than 5000')
        return inputsal
    class Meta:
        model=Employee
        fields='__all__'
