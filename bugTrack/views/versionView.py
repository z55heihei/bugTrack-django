# coding=utf-8
__author__ = 'zhangyw'

from  track.models import Version
import simplejson as json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def __buildVersionJson__(Version,dic):
    versionDict = {}
    versionDict["id"] = Version.id
    versionDict["version"] = Version.version
    dic["versions"].append(versionDict)

@csrf_exempt
def getVersions(request):
    if request.method == "GET":
        dic = {}
        dic["versions"] = []
        versions = Version.objects.all()
        if versions != None and len(versions) > 0:
            count = versions.count()
            dic["count"] = count
            dic["state"] = 1
            for versionItem in versions:
                __buildVersionJson__(versionItem,dic)
        doc = json.dumps(dic)
        return HttpResponse(doc)
    else:
        return Http404

@csrf_exempt
def delVersion(request):
    if request.method == "POST":
        dic = {}
        versionId = request.POST["versionId"]
        if versionId != "" and len(versionId) > 0:
            version = Version.objects.filter(id = versionId)
            if version != None and len(version) > 0:
                version.delete()
                dic["state"] = 1
                dic["message"] = "删除成功"
            else:
                dic["state"] = 2
                dic["message"] = "id错误"
            doc = json.dumps(dic)
            return HttpResponse(doc)
    else:
        return Http404

@csrf_exempt
def creatVersion(request):
    if request.method == "POST":
        dic = {}
        dic["versions"] = []
        if request.POST.has_key("version"):
            version = request.POST["version"]
            versions = Version.objects.filter(version = version)
            if versions == None or len(versions) <= 0:
                dic["state"] = 1
                versionItem = Version()
                versionItem.version = version
                versionItem.save()
                __buildVersionJson__(versionItem,dic)
            else:
                dic["state"] = 2
                dic["message"] = "版本已存在"
        else:
            dic["state"] = 2
            dic["message"] = "参数不存在"
        doc = json.dumps(dic)
        return HttpResponse(doc)
    else:
        return Http404
