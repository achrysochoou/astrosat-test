from django.shortcuts import render


def astrosat_error(request, error_msg="", status_code=400):

    context = {
        "error_msg": error_msg,
        "status_code": status_code,
    }

    return render(request, 'astrosat/error.html', context)


def page_not_found(request):
    return astrosat_error(request, error_msg="Page not found.", status_code=404)


def server_error(request):
    return astrosat_error(request, error_msg="Server error.", status_code=500)


def permission_denied(request):
    return astrosat_error(request,error_msg="Permission denied.", status_code=403)


def bad_request(request):
    return astrosat_error(request, error_msg="Bad request", status_code=400)
