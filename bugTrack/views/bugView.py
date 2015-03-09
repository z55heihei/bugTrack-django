__author__ = 'zhangyw'
# coding=utf-8

from track.models import Bug
import simplejson as json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


def __buildBugListJson__(Bug,dic):
    bugListDict = {}
    bugListDict["id"] = Bug.id
    bugListDict["project"] = Project(Bug)
    bugListDict["name"] = Name(Bug)
    bugListDict["distribter"] = Distribter(Bug)
    bugListDict["urgency"] = Urgency(Bug)
    bugListDict["content"] = Bug.content
    bugListDict["platform"] = Platform(Bug)
    bugListDict["module"] = Module(Bug)
    bugListDict["phone"] = Phone(Bug)
    bugListDict["version"] = Version(Bug)
    bugListDict["date"] = str(Bug.date)
    bugListDict["finish"] = Finish(Bug)
    dic["bugs"].append(bugListDict)

def Distribter(Bug):
    username = Bug.distribter.username
    return username

def Module(Bug):
    module = Bug.module.modules
    return module

def Version(Bug):
    version = Bug.version.version
    return version

def Name(Bug):
    name = Bug.name.username
    return name

def Project(Bug):
    project =  Bug.project.project
    return project

def Phone(Bug):
    phone = Bug.phone.phone.national_number
    return phone

def Platform(Bug):
    platformItem = {"1":"IOS","2":"Android"}
    return platformItem[Bug.platform]

def Finish(Bug):
    if Bug.state == 1:
        isFinishItem = "未解决"
    elif Bug.state == 2:
        isFinishItem = "正在解决"
    else:
        isFinishItem = "已解决"
    return isFinishItem

def Urgency(Bug):
    urgencyItem = {"1":"低","2":"中","3":"高","4":"严重"}
    return urgencyItem[Bug.urgency]


#获取bugs列表
@csrf_exempt
def getMyBugs(request):
    if request.method == "POST":
        if request.POST.has_key("username"):

            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            nameId = request.POST["username"]
            bugs = Bug.objects.filter(name = nameId)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)

        if request.POST.has_key("project"):
            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            projectId = request.POST["project"]
            bugs = Bug.objects.filter(project = projectId)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)

        if request.POST.has_key("version"):
            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            version = request.POST["version"]
            bugs = Bug.objects.filter(version = version)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)

        if request.POST.has_key("urgency"):
            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            urgency = request.POST["urgency"]
            bugs = Bug.objects.filter(urgency = urgency)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)

        if request.POST.has_key("platform"):
            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            platform = request.POST["platform"]
            bugs = Bug.objects.filter(plateform = platform)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)

        if request.POST.has_key("state"):
            dic = {}
            dic["state"] = 1
            dic["bugs"] = []

            state = request.POST["state"]
            bugs = Bug.objects.filter(state = state)
            count = bugs.count()
            dic["count"] = count

            for bugitem in bugs:
                __buildBugListJson__(bugitem,dic)
            doc = json.dumps(dic)
            return  HttpResponse(doc)
    else:
        return Http404

#bug发送
@csrf_exempt
def bugSend(request):
    if request.method == "GET":
         name = request.GET["name"]
         contnet = request.GET["content"]
         version = request.GET['version']
         date = request.GET["date"]
         finish = request.GET["finish"]

         dic = {}
         dic["state"] = 1
         dict = {}
         dic["bugs"] = []

         bug = Bug()
         bug.name = name
         bug.content = contnet
         bug.version = version
         bug.date = date
         bug.finish = finish
         bug.save()

         dict["name"] = name
         dict["content"] = contnet
         dict["version"] = version
         dict["date"] = date
         dict["finish"] = finish
         dic["bugs"].append(dict)

         doc = json.dumps(dic)
         return HttpResponse(doc)
    else:
        return Http404

#删除bug
@csrf_exempt
def delBug(request):
    if request.method == "POST":
         if request.POST.has_key("bugId"):
             id = request.POST["bugId"]
             dic = {}
             dic["bugs"] = []
             bugItem = Bug.objects.filter(id = id)

             if bugItem != None and len(bugItem):
                 dic["state"] = 1
                 bugItem.delete()
             else:
                 dic["state"] = 2
                 dic["mesage"] = "删除失败,id错误"

             doc = json.dumps(dic)
             return HttpResponse(doc)
    else:
        Http404

#修改bug状态
@csrf_exempt
def modifyBug(request):
    if request.method == "POST":
        if request.POST.has_key("bugId"):
            id = request.POST["bugId"]
            state = request.POST["state"]
            dic = {}
            dic["bugs"] = []
            bugItem = Bug.objects.filter(id = id)
            if bugItem != None and len(bugItem):
                dic["state"] = 1
                bugItem.state = None
                bug = bugItem[0]
                if state != "" and len(state):
                    bug.state = state
                    bug.save()
            else:
                dic["state"] = 2
                dic["mesage"] = "修改失败,id错误"

            doc = json.dumps(dic)
            return HttpResponse(doc)
    else:
        Http404
