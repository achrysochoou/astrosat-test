from django.shortcuts import render


def test(request):

    context = { }

    return render(request, 'astrosat/test.html', context)
