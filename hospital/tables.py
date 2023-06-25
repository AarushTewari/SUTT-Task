import django_tables2 as tables
from .models import Patient

class PatientTable(tables.Table):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'gender', 'email', 'address')