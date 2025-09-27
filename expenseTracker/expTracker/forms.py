from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    long_term = forms.BooleanField(required=False)

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'interest_rate', 'date', 'end_date', 'long_term']
        
        widgets = {  
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'long_term': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        long_term = cleaned_data.get('long_term')
        start_date = cleaned_data.get('date')
        interest_rate = cleaned_data.get('interest_rate')
        end_date = cleaned_data.get('end_date')

        # If not long_term, make sure interest_rate and end_date are empty
        if not long_term:
            cleaned_data['interest_rate'] = None
            cleaned_data['end_date'] = None
        else:
            # Optional: Add validation for long_term fields
            if interest_rate is None:
                self.add_error('interest_rate', 'Interest rate is required for long-term expenses.')
            if end_date is None:
                self.add_error('end_date', 'End date is required for long-term expenses.')

        return cleaned_data
