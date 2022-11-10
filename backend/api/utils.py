from io import BytesIO

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)


def add_remove(self, request, target, obj, target_obj):
    """ Функция для подписок, пополнения корзины или лайков пользователем """

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
    if request.method == 'POST':
        obj.objects.create(**target_kwargs)
        serializer = self.serializer_class(get_obj)
        return Response(serializer.data, status=HTTP_201_CREATED)

    if request.method == 'DELETE' and filtered.exists():
        filtered.delete()
        return Response(SUCESS_DELETE, status=HTTP_204_NO_CONTENT)
    if request.method == 'DELETE':
        return Response(NOT_IN_LIST, status=HTTP_400_BAD_REQUEST)

    return True


def shopping_list_pdf(cart):
    """ Выгрузка списка покупок в pdf """

    buffer = BytesIO()
    can = Canvas(buffer)

    SANS_REGULAR = settings.STATIC_ROOT + '/fonts/OpenSans-Regular.ttf'
    SANS_REGULAR_NAME = 'OpenSans-Regular'
    SANS_BOLD = settings.STATIC_ROOT + '/fonts/OpenSans-Bold.ttf'
    SANS_BOLD_NAME = 'OpenSans-Bold'

    FILE_NAME = 'shopping_list.pdf'

    pdfmetrics.registerFont(TTFont(SANS_REGULAR_NAME, SANS_REGULAR))
    pdfmetrics.registerFont(TTFont(SANS_BOLD_NAME, SANS_BOLD))
    can.setTitle('Список покупок')

    can.setFont(SANS_BOLD_NAME, 32)
    can.drawString(100, 750, 'foodgram')
    can.setFont(SANS_REGULAR_NAME, 13)
    can.drawString(100, 725, 'Ваш продуктовый помощник')
    can.line(100, 715, 500, 715)
    can.setFont(SANS_BOLD_NAME, 13)
    can.drawString(393, 700, 'cписок покупок')
    can.setFont(SANS_REGULAR_NAME, 10)

    padding_top = 680
    page_number = 1
    steps = len(cart)
    last_step = steps - 1
    for step, ingredient in enumerate(cart):
        ingredient = list(ingredient.values())
        if step == last_step and steps >= 3:
            x = padding_top - 20
            can.line(100, x, 500, x)
            can.setFont(SANS_BOLD_NAME, 13)
            can.drawString(362, x - 15, 'приятного аппетита')
            can.setFont(SANS_REGULAR_NAME, 10)
        if padding_top <= 80:
            can.showPage()
            can.line(100, 770, 500, 770)
            can.setFont(SANS_BOLD_NAME, 13)
            can.drawString(393, 755, 'cписок покупок')
            can.setFont(SANS_REGULAR_NAME, 10)
            page_number += 1
            padding_top = 735
            can.drawString(100, 780, f'стр. {page_number}')
        product = ingredient[0]
        unit = ingredient[1]
        total = ingredient[2]
        string = f'{step+1}. {product[0:48]} ({unit[0:10]}) — {total}'
        can.drawString(100, padding_top, string)
        padding_top -= 19

    can.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=FILE_NAME)
