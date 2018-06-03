from django.shortcuts import render


def index(request):

    context = {
        "is_admin": request.user.is_superuser
    }

    return render(request, 'astrosat/index.html', context)
