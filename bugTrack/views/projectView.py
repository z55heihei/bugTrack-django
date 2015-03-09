# coding=utf-8
__author__ = 'zhangyw'
from  track.models import Project,Version
import simplejson as json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def __buildProjectJson__(Project,dic):
    projectDict = {}
    projectDict["id"] = Project.id
    projectDict["project"] = Project.project
    projectDict["version"] = Project.version.version
    dic["projects"].append(projectDict)

@csrf_exempt
def getProjects(request):
    if request.method == "GET":
        dic = {}
        dic["projects"] = []
        dic["state"] = 1

        project = Project.objects.all()
        if project != None and len(project):
            for projectItem in project:
                __buildProjectJson__(projectItem,dic)
        doc = json.dumps(dic)
        return HttpResponse(doc)
    else:
        return Http404

@csrf_exempt
def delProject(request):
    if request.method == "POST":
        if request.POST.has_key("projectId"):
            projectId = request.POST["projectId"]
            project = Project.objects.filter(id = projectId)
            dic = {}
            if project != None and len(project) > 0:
                project.delete()
                dic["state"] = 1
                dic["messgae"] = "删除成功"
            else:
                dic["state"] = 2
                dic["messgae"] = "暂无该项目"

            doc = json.dumps(dic)
            return HttpResponse(doc)
    else:
        return Http404

@csrf_exempt
def creatProject(requset):
    if requset.method == "POST":
        if requset.POST.has_key("project")\
            and requset.POST.has_key("version"):
            project = requset.POST["project"]
            version = requset.POST["version"]
            dic = {}
            dic["projects"] = []
            if project != "" and len(project) > 0 \
                    and version != "" and len(version):
                versions = Version()
                versions.version = version
                versions.save()
                dic["state"] = 1

                projects = Project()
                projects.project = project
                projects.version = versions
                projects.save()
                __buildProjectJson__(projects,dic)
            doc = json.dumps(dic)
        return HttpResponse(doc)
    else:
        Http404