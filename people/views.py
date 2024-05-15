from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Person
from .serializers import PersonSerializers, PersonDetailSerializers


# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list' or self.action =='search':
            return PersonSerializers
        else:
            return PersonDetailSerializers
        
    @action(detail=False, methods=['get'],serializer_class=PersonSerializers)  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            self.queryset = Person.objects.filter(name__icontains=query)
        else:
            self.queryset = []
        
        return super().list(request, *args, **kwargs)