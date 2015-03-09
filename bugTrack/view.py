from django.shortcuts import render_to_response

__author__ = 'zhangyw'

def paramsTest(request):
    return render_to_response('ParamsFormTest.html')