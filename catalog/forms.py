from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import BookInstance

from datetime import date, timedelta

# class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(
#         help_text="Enter a date between now and 4 weeks (default 3)."
#     )

#     def clean_renewal_date(self):
#         data = self.cleaned_data["renewal_date"]

#         if data < datetime.date.today():
#             raise ValidationError(_("Invalid date - renewal in past"))

#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

#         return data


class RenewBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {"due_back": _("New renewal date")}
        helo_text = {"due_back": _("Enter a date betwee now and 4 weeks (default 3).")}

    def clean_due_back(self):
        data = self.cleaned_data["due_back"]
        today_date = date.today()

        if data < today_date:
            raise ValidationError(_("Invalid date - renewal in past"))

        if data > today_date + timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        return data
