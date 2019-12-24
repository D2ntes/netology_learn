from collections import Counter
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    if from_landing == 'original':
        counter_click['original'] += 1
    elif from_landing == 'test':
        counter_click['test'] += 1
    return render(request, 'index.html')



def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'original':
        counter_show['original'] += 1
        return render(request, 'landing.html')
    elif ab_test_arg == 'test':
        counter_show['test'] += 1
        return render(request, 'landing_alternate.html')



def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:

    original_conversion = 0 if counter_show['original'] is 0 \
        else counter_click['original'] / counter_show['original']

    test_conversion = 0 if counter_show['test'] is 0 \
        else counter_click['test'] / counter_show['test']

    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion
    })