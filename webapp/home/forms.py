"""User facing forms for making support requests (help/tools/data)."""

import logging
import traceback
from captcha import fields
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from utils.institution import is_institution_email
from utils import postal

from . import validators


logger = logging.getLogger('django')


def dispatch_form_mail(
        to_address=None,
        reply_to=None,
        subject=None,
        text=None,
        html=None):
    """Send mail to support inbox.

    This should probably be sent to a worker thread.
    """
    recipient = to_address or settings.EMAIL_TO_ADDRESS
    reply_to_value = [reply_to] if reply_to else None
    logger.info(f"Sending mail to {recipient}")
    email = EmailMultiAlternatives(
        subject,
        text,
        settings.EMAIL_FROM_ADDRESS,
        [recipient],
        reply_to=reply_to_value,
    )
    if html:
        email.attach_alternative(html, "text/html")

    tries = 0
    while True:
        try:
            if settings.EMAIL_HOST == 'mail.usegalaxy.org.au':
                # Special SMTP setup for GA mail server
                return postal.send_mail(email)
            return email.send()
        except Exception:
            logger.warning(f"Send mail error - attempt {tries}")
            tries += 1
            if tries < 3:
                continue
            return logger.error(
                "Error sending mail. The user did not receive an error.\n"
                + traceback.format_exc()
                + f"\n\nMail content:\n\n{text}"
            )


class OtherFieldFormMixin:
    """Handle validation/cleaning of 'other' fields.

    The inheriting class must define cls.OTHER_FIELDS as a tuple of field names
    for which a "field_other" field is expected. This field will be populated
    with the value of "other" if:
        not field
        str(field) == "0"

    Typically this is involves an "Other" radiobuttom with a value of "0".
    """

    def __init__(self, *args, **kwargs):
        """Assert required other fields."""
        super().__init__(*args, **kwargs)
        for field in self.OTHER_FIELDS:
            if f'{field}_other' not in self.fields:
                raise AttributeError(
                    f"Expected field '{field}_other' not found in form."
                    " Fields declared as OTHER_FIELDS must be accompanied by"
                    " an '_other' field to provide the 'other' value."
                )

    def clean(self):
        data = self.cleaned_data
        for field in self.OTHER_FIELDS:
            field_value = data.get(field)
            if not field_value or str(field_value) == '0':
                # User selected the 'other' field and typed a value
                other_value = data.get(f'{field}_other')
                logger.info(f"field_value: {field_value}")
                logger.info(f"other_value: {other_value}")
                if not other_value:
                    if self.fields[field].required:
                        self.add_error(
                            field,
                            ValidationError('This field is required'))
                        continue
                if type(other_value) == str:
                    data[field] = 'Other - ' + other_value
                else:
                    data[field] = other_value
        return data


class ResourceRequestForm(forms.Form):
    """Form for requesting a tool or dataset."""

    RESOURCE_CHOICES = (
        ('tool', 'Tool'),
        ('dataset', 'Dataset'),
    )

    name = forms.CharField()
    email = forms.EmailField()
    # tool/dataset
    resource_type = forms.ChoiceField(choices=RESOURCE_CHOICES)
    resource_name_version = forms.CharField()
    resource_url = forms.URLField(required=False)
    resource_justification = forms.CharField(required=False)

    # Fields for tool
    tool_toolshed_available = forms.BooleanField(required=False)
    tool_toolshed_url = forms.URLField(required=False)
    tool_test_data = forms.BooleanField(required=False)

    captcha = fields.ReCaptchaField()

    def dispatch(self):
        """Dispatch form content as email."""
        data = self.cleaned_data
        template = (
            'home/requests/mail/'
            f"{data['resource_type']}"
        )
        dispatch_form_mail(
            reply_to=data['email'],
            subject=(
                f"New {data['resource_type']}"
                " request on Galaxy Australia"
            ),
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )


class QuotaRequestForm(OtherFieldFormMixin, forms.Form):
    """Form for requesting data quota."""

    name = forms.CharField()
    email = forms.EmailField()
    start_date = forms.DateField()
    duration_months = forms.IntegerField()
    disk_tb = forms.IntegerField()
    disk_tb_other = forms.IntegerField(required=False)
    description = forms.CharField()
    captcha = fields.ReCaptchaField()
    accepted_terms = forms.BooleanField()

    OTHER_FIELDS = ('disk_tb',)

    def dispatch(self):
        """Dispatch form content as email."""
        template = 'home/requests/mail/quota'
        dispatch_form_mail(
            reply_to=self.cleaned_data['email'],
            subject="New Quota request on Galaxy Australia",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {'form': self}),
        )


class SupportRequestForm(forms.Form):
    """Form to request for user support."""

    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

    def dispatch(self, subject=None):
        """Dispatch content via the FreshDesk API."""
        data = self.cleaned_data
        dispatch_form_mail(
            reply_to=data['email'],
            subject=subject or "Galaxy Australia Support request",
            text=(
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n\n"
                + data['message']
            )
        )


class BaseAccessRequestForm(forms.Form):
    """Abstract form for requesting access to a resource.

    Form fields in the format 'X_other' are substituted into the 'X' field
    on submission and excluded from dispatched email.
    """

    def clean_email(self):
        """Validate email address."""
        email = self.cleaned_data['email']
        if not is_institution_email(email):
            raise ValidationError(
                (
                    'Sorry, this is not a recognised Australian institution'
                    ' email address.'
                ),
                field="email",
            )
        return email

    def dispatch(self):
        """Dispatch form content as email."""
        template = 'home/requests/mail/access-request'
        context = {
            'data': {
                field.name: {
                    'label': field.label,
                    'value': self.cleaned_data[field.name],
                }
                for field in self
                if not (
                    field.name.endswith("_other")
                    and field.name[:-6] in self.OTHER_FIELDS
                )
            },
            'resource_name': self.RESOURCE_NAME,

        }
        dispatch_form_mail(
            reply_to=self.cleaned_data['email'],
            subject=f"New {self.RESOURCE_NAME} request on Galaxy Australia",
            text=render_to_string(f'{template}.txt', context),
            html=render_to_string(f'{template}.html', context),
        )

    def dispatch_warning(self, request):
        """Dispatch warning email to let user know their email is invalid."""
        template = 'home/requests/mail/invalid-institutional-email'
        dispatch_form_mail(
            to_address=self.cleaned_data['email'],
            subject=f"Access to {self.RESOURCE_NAME} could not be granted",
            text=render_to_string(f'{template}.txt', {'form': self}),
            html=render_to_string(f'{template}.html', {
                'form': self,
                'hostname': settings.HOSTNAME,
                'scheme': request.scheme,
            }),
        )


class AlphafoldRequestForm(BaseAccessRequestForm):
    """Form to request AlphaFold access."""

    RESOURCE_NAME = 'AlphaFold'

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()
    species = forms.CharField(required=False)
    domain = forms.CharField(required=False, label="Domain of study")
    proteins = forms.CharField(required=False, label="Target proteins")
    size_aa = forms.IntegerField(required=False, label="Size (AA)")
    count_aa = forms.IntegerField(required=False, label="Total count (AA)")


class FgeneshRequestForm(OtherFieldFormMixin, BaseAccessRequestForm):
    """Form to request AlphaFold access."""

    RESOURCE_NAME = 'Fgenesh++'
    SPECIES_CHOICES = (  # TODO: populate choices from remote API/GitHub?
        ('1', 'Caenorhabditis elegans (Non-redundant database)'),
        ('2', 'Gallus gallus domesticus (Non-redundant database)'),
        ('3', 'Gene matrix (522 species)'),
        ('0', 'Other, please specify'),
    )
    OTHER_FIELDS = ('species',)

    name = forms.CharField()
    email = forms.EmailField(validators=[validators.institutional_email])
    institution = forms.CharField()
    agree_terms = forms.BooleanField()
    agree_acknowledge = forms.BooleanField()
    species = forms.ChoiceField(choices=SPECIES_CHOICES)
    species_other = forms.CharField(required=False)


ACCESS_FORMS = {
    'alphafold': AlphafoldRequestForm,
    'fgenesh': FgeneshRequestForm,
}
