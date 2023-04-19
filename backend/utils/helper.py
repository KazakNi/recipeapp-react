from reportlab.pdfgen import canvas
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from recipes.models import Recipe
from api.serializers import RecipeReadSerializer
import io
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


def create_or_delete(id, request, Model):
    user = request.user
    recipe = Recipe.objects.get(id=id)
    if request.method == 'POST':
        instance, created = Model.objects.get_or_create(
            recipe=recipe, author=user)
        if created:
            serializer = RecipeReadSerializer(
                recipe, many=False, context={'request': request,
                                             'recipes_limit': 1})
            return Response(serializer.data)
        return Response({'message': 'Рецепт уже был добавлен!'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        obj = get_object_or_404(Model, author=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def cart_to_pdf_dump(query):
    buffer = io.BytesIO()
    x = canvas.Canvas(buffer)
    x.setFont('Arial', 16)
    my_text = []
    ingredients = {}
    ings_meas = {}
    for q in query:
        a = ingredients.get(q['ingredients__name'], None)
        if a is not None:
            ingredients[q['ingredients__name']] += q['amount']
        else:
            ingredients[q['ingredients__name']] = q['amount']

        ings_meas[q['ingredients__name']] = q['ingredients__measurement_unit']
    for name, amount in ingredients.items():
        line = (name + ' —' + f' {amount} ' + f' ({ings_meas[name]})')
        my_text.append(line)
    my_text = '\n'.join(my_text)
    textobject = x.beginText(250, 800)
    textobject.textLine('Ингредиенты')
    x.drawText(textobject)
    textobject = x.beginText(20, 780)
    textobject.textLine('_______________________________________________')
    x.drawText(textobject)
    textobject = x.beginText(28, 750)
    for line in my_text.splitlines(False):
        textobject.textLine(line.rstrip())
    x.drawText(textobject)
    x.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='shopping_cart.pdf')
