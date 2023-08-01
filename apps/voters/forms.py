from django import forms
from django.core.exceptions import ValidationError
from .models import Voter, VotingPoint, Quarters
from django_select2.forms import Select2Widget

DEFAULT_ATTRS = {
    'autocomplete': 'off',
    'class': 'w-full border-2 bg-white border-white mt-3 text-gray mb-4 max-w-lg block focus:ring-indigo-500 focus:border-gray-500 sm:max-w-xs sm:text-sm rounded-full border-width-4'
}
TEXTAREA_ATTRS = {
    'autocomplete': 'off',
    'class': 'w-full border-2 border-white mt-1 text-white mb-4 max-w-lg block focus:ring-indigo-500 focus:border-gray-500 sm:max-w-xs sm:text-sm rounded-lg border-width-4'
}

def create_charfield(name, placeholder, min_length=None, max_length=None, type='text'):
    widget = forms.TextInput(attrs={
        **DEFAULT_ATTRS, 'placeholder': placeholder
    })
    if type =='textarea':
        widget = forms.Textarea(attrs={
            **DEFAULT_ATTRS, "rows": "2", 'placeholder': placeholder
        })


    return forms.CharField(
        min_length=min_length,
        max_length=max_length,
        widget=widget,
        required=True
    )

class VotersForm(forms.ModelForm):
    DOCUMENT_TYPES = [
        ('','Selecciona un tipo de documento'),
        ('CC','CEDULA DE CIUDADANIA'),
        ('CE','CEDULA DE EXTRANJERIA'),
    ]

    document_type = forms.ChoiceField(choices=DOCUMENT_TYPES, widget=forms.Select(attrs=DEFAULT_ATTRS), required=True)

    nuip = create_charfield('nuip', 'Ingrese el Numero de Identidad', min_length=7, max_length=10)

    full_name = create_charfield('full_name', 'Ingrese el Nombre completo')

    quarter = quarter = forms.ModelChoiceField(queryset=Quarters.objects.all().order_by('name'), empty_label="Selecciona un barrio o vereda", widget=Select2Widget(attrs=DEFAULT_ATTRS), required=True)

    address = forms.CharField(widget=forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Direccion (Opcional)', type: 'textarea', 'rows': 2}),max_length=150,required=False)
    
    phone = create_charfield('phone', 'Número de teléfono', min_length=10, max_length=10)

    voting_point = forms.ModelChoiceField(queryset=VotingPoint.objects.all(),empty_label="Selecciona un punto de votación", widget=Select2Widget(attrs=DEFAULT_ATTRS),required=True)  

    email = forms.EmailField(widget=forms.EmailInput(attrs={**DEFAULT_ATTRS, 'placeholder': 'Ingrese el Correo Electrónico'}), required=True)

    def clean_fields(self):
        super().clean_fields()
        
        document_type = self.cleaned_data.get('document_type')
        if document_type not in [doc_type[0] for doc_type in self.DOCUMENT_TYPES[1:]]: 
            self.add_error('document_type', "Por favor selecciona un tipo de documento valido.")
            
        nuip = self.cleaned_data.get('nuip')
        if not nuip.isdigit():
            self.add_error('nuip', "El Numero de identidad debe contener únicamente dígitos numéricos.")
        elif len(nuip) < 7 or len(nuip) > 10:
            self.add_error('nuip', "El Numero de identidad debe tener un mínimo de 7 y un máximo de 10 dígitos.")
        
        phone = self.cleaned_data.get('phone')
        if len(str(phone)) != 10 or not str(phone).startswith('3'):
            self.add_error('phone', "El número de telefono debe tener 10 digitos y comenzar con 3")
        
        address = self.cleaned_data.get('address')
        if address and len(address) > 150: 
            self.add_error('address', "La dirección debe tener un máximo de 150 caracteres.")

    class Meta:
        model = Voter
        fields = ['document_type', 'nuip', 'full_name', 'quarter', 'voting_point', 'phone', 'email', 'address']