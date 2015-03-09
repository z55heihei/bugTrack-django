# coding=utf-8
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from track.models import Modules
import  simplejson as josn

__author__ = 'zhangyw'


def __buildModulesListJson__(Modules,dic):
    modulesDict = {}
    print(Modules.modules)
    modulesDict["id"] = Modules.id
    modulesDict["module"] = Modules.modules
    dic["modules"].append(modulesDict)

@csrf_exempt
def creatModule(request):
    if request.method == "POST":
        if request.POST.has_key("module"):
            dict = {}
            dict["modules"] = []
            dic = {}
            moduleName = request.POST["module"]
            '''查询数据库是否存在该模块'''
            modules = Modules.objects.filter(modules = moduleName)

            if modules == None or (len(modules) <= 0):

                module = Modules()
                module.modules = moduleName
                module.save()

                modules = Modules.objects.get(modules = moduleName)

                dict["state"] = 1
                dic["id"] = modules.id
                dic["module"] = modules.modules
            else:
                dict["state"] = 2
                dict["message"] = "模块已经存在"

            dict["modules"].append(dic)
            doc = josn.dumps(dict)
            return HttpResponse(doc)
    else:
        return Http404


@csrf_exempt
def getModules(request):
    if request.method == "GET":
       dic = {}
       dic["modules"] = []

       modules = Modules.objects.all()
       count = modules.count()
       dic["count"] = count
       dic["state"] = 1

       for moduleItem in modules:
           __buildModulesListJson__(moduleItem,dic)

       doc = josn.dumps(dic)
       return HttpResponse(doc)
    else:
        return Http404

@csrf_exempt
def delModule(request):
    if request.method == "POST":
        if request.POST.has_key("moduleId"):
            dic = {}
            moduleId = request.POST["moduleId"]
            module = Modules.objects.filter(id = moduleId)

            if module != None and len(module) > 0:
                module = Modules.objects.get(id = moduleId)
                module.delete()

                dic["state"] = 1
                dic["message"] = "删除成功"

            doc = josn.dumps(dic)
            return HttpResponse(doc)
    else:
        return Http404