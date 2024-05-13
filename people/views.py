from rest_framework import viewsets

from .models import Person
from .serializers import PersonSerializers, PersonDetailSerializers


# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return PersonSerializers
        else:
            return PersonDetailSerializers
