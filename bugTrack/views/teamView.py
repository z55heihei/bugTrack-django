# coding=utf-8
__author__ = 'zhangyw'
from track.models import Team
import simplejson as json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


def __bulidTeamsJson__(Team,dic):
    teamDict = {}
    teamDict["id"]  = Team.id
    teamDict["team"] = Team.team
    dic["teams"].append(teamDict)


@csrf_exempt
def getTeams(request):
    if request.method == "GET":
        dic = {}
        dic["teams"] = []
        dic["state"] = 1
        team = Team.objects.all()
        if team != None and len(team):
            dic["count"] = team.count()
            for teamItem in team:
                __bulidTeamsJson__(teamItem,dic)
        doc = json.dumps(dic)
        return HttpResponse(doc)
    return Http404

@csrf_exempt
def delTeam(request):
    if request.method == "POST":
        if request.POST.has_key("teamId"):
            dic = {}
            teamId = request.POST["teamId"]
            team = Team.objects.filter(id = teamId)
            if team != None and len(team) > 0:
                team.delete()
                dic["state"] = 1
                dic["messge"] = "删除成功"
            doc = json.dumps(dic)
            return HttpResponse(doc)
    return Http404

@csrf_exempt
def creatTeam(request):
    if request.method == "POST":
       dic = {}
       if request.POST.has_key("team"):
           team = request.POST["team"]
           if team != "" and len(team) > 0:
               teamItem = Team()
               teamItem.team = team
               teamItem.save()

               dic["state"] = 1
               dic["messge"] = "创建团队成功"
           else:
               dic["state"] = 2
               dic["messge"] = "team 参数缺失"

           doc = json.dumps(dic)
           return HttpResponse(doc)
    else:
       return Http404