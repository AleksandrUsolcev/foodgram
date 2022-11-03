from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)


def add_remove(self, request, target, obj, target_obj):

    SUCESS = {'detail': 'success'}
    IN_LIST = {'errors': 'already in list'}
    NOT_IN_LIST = {'errors': 'not in list'}

    user = self.request.user
    get_obj = get_object_or_404(target_obj, pk=self.kwargs.get(target))
    target_kwargs = {
        'user': user,
        target: get_obj
    }
    filtered = obj.objects.filter(**target_kwargs)

    if request.method == 'POST' and filtered.exists():
        return Response(IN_LIST, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        obj.objects.create(**target_kwargs)
        return Response(SUCESS, status=HTTP_201_CREATED)

    if request.method == 'DELETE' and filtered.exists():
        filtered.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        return Response(NOT_IN_LIST, status=HTTP_400_BAD_REQUEST)
