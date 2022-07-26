import random

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from app.forms import  CustomerForm


def login_view(request):
    print('hi')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        print('hi', username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                type = 'staff'
            elif user.is_user:
                type = 'user'
    try:
        result = user.is_authenticated
        data = {
            'status': True,
            'result': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'type': type
            }
        }

    except:
        data = {
            'status': False
        }
    return JsonResponse(data, safe=False)


def user_registration(request):
    result_data = None
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        FullName = request.POST.get('FullName')
        uname = FullName + str(random.randint(0,999))
        if form.is_valid():
            form = form.save(commit=False)
            form.username = uname
            form.is_active = True
            form.is_user = True
            form.save()
            result_data = True
    try:
        if result_data:
            data = {'result':True}
        else:
            print(list(form.errors))
            error_data = form.errors
            error_dict = {}
            for i in list(form.errors):
                error_dict[i] = error_data[i][0]

                data = {
                    'result':False,
                    'errors':error_dict
                }
    except:
        data = {
            'result':False
        }
    return JsonResponse(data,safe=False)



            # form = form.save(commit=False)
            # form.username = uname
            # form.is_active = True
            # form.is_user = True
            # form.save()
            # result_data = True

    # user = authenticate(request,username=username, password=password)
    # try:
    #     if result_data:
    #         data = {'result': True}
    #     else:
    #         print(list(form.errors))
    #         error_data = form.errors
    #         error_dict = {}
    #         for i in list(form.errors):
    #             error_dict[i] = error_data[i][0]
    #
    #             data = {
    #                 'result': False,
    #                 'errors': error_dict
    #             }
    # except:
    #     data = {
    #         'result': False
    #     }
    #
    # return JsonResponse(data, safe=False)
