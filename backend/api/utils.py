from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)


def add_remove(self, request, target, obj, target_obj):
    """ Функция для подписок, пополнения корзины или лайков пользователем """

    SUCESS_ADD = {'detail': f"Success add to your {obj.__name__}'s list"}
    SUCESS_DELETE = {
        'detail': f"Success delete from your {obj.__name__}'s list"}
    ALREADY_IN_LIST = {'errors': f"Already in your {obj.__name__}'s list"}
    NOT_IN_LIST = {'errors': f"Not in your {obj.__name__}'s list"}

    user = self.request.user
    get_obj = get_object_or_404(target_obj, pk=self.kwargs.get(target))
    target_kwargs = {
        'user': user,
        target: get_obj
    }
    filtered = obj.objects.filter(**target_kwargs)

    if request.method == 'POST' and filtered.exists():
        return Response(ALREADY_IN_LIST, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        obj.objects.create(**target_kwargs)
        return Response(SUCESS_ADD, status=HTTP_201_CREATED)

    if request.method == 'DELETE' and filtered.exists():
        filtered.delete()
        return Response(SUCESS_DELETE, status=HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        return Response(NOT_IN_LIST, status=HTTP_400_BAD_REQUEST)
