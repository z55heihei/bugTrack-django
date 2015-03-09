__author__ = 'zhangyw'
# coding=utf-8

from track.models import User,Team
import simplejson as json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

#用户注册
@csrf_exempt
def register(request):
    if request.method == "POST":
         username = request.POST["username"]
         password = request.POST["password"]
         email = request.POST['email']
         teamId = request.POST['team']

         dic = {}
         dict = {}
         dict["userInfo"] = []

         #查询数据库有没有这个用户
         currentUser = User.objects.filter(username = username)
         team = Team.objects.get(id = teamId)
         print(team)

         if (currentUser != None) and len(currentUser) > 0:
              dict["state"] = 2
              dict["message"] = "已经注册"
         else:
              user = User()
              user.username = username
              user.password = password
              user.email = email
              user.team = team
              user.save()
              # 字典组成

              dict["state"] = 1
              dic["username"] = username
              dic["email"] = email
              dic["team"] = team.team

         dict["userInfo"].append(dic)

         doc = json.dumps(dict)
         return HttpResponse(doc)
    else:
        return Http404

#用户登录
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        dic = {}
        dict = {}
        dict["userInfo"] = []

        #查询数据库有没有这个用户
        user = User.objects.filter(username = username,password = password)
        if user != None and len(user) > 0:
             user = user[0]
             dict["state"] = 1
             dic["username"] = user.username
             dic["email"] = user.email
             dic["team"] = user.team.team
        else:
             dict["state"] = 2
             dict["message"] = "用户名或者密码错误"

        dict["userInfo"].append(dic)
        doc = json.dumps(dict)
        return HttpResponse(doc)
    else:
        return Http404


#修改用户
@csrf_exempt
def modifyUser(request):
    if request.method == "POST":
        username = request.POST["oriusername"]
        password = request.POST["oripassword"]
        email = request.POST["oriemail"]

        newusername = request.POST["newusername"]
        newpassword = request.POST["newpassword"]
        newemail = request.POST["newemail"]

        dic = {}
        dict = {}
        dic["userInfo"] = []

        user = User.objects.filter(username = username,password = password,email = email)

        if user != None and len(user):
            user = user[0]

            user.username = None
            user.password = None
            user.email = None

            if len(username) > 0:
               user.username = newusername
            if len(password) > 0:
               user.password = newpassword
            if len(email) > 0:
               user.email = newemail
            user.save()

            dic["state"] = 1
            dict["username"] = newusername
            dict["email"] = newemail
            dict["team"] = user.team.team
        else:
            dic["state"] = 2
            dic["message"] = "修改失败，用户名或者密码错误"

        dic["userInfo"].append(dict)
        doc = json.dumps(dic)
        print(dic)
        return HttpResponse(doc)

    else:
        return Http404


#获取所有用户
@csrf_exempt
def allUser(request):
    if request.method == "GET":
        dic = {}
        dic["users"] = []

        users = User.objects.all()
        if len(users) > 0:
          for userItem in users:
             dictItem = {}
             dictItem["id"] = userItem.id
             dictItem["username"] = userItem.username
             dictItem["email"] = userItem.email
             dic["users"].append(dictItem)
             dic["state"] = 1
        else:
            dic["state"] = 2
            dic["message"] = "暂无人员"

        doc = json.dumps(dic)
        return HttpResponse(doc)
    else:
        return Http404


# 删除用户
@csrf_exempt
def delUser(request):
    if request.method == "POST":
        dic = {}
        userId = request.POST["userId"]
        if userId != "" and len(userId) > 0:
            user = User.objects.filter(id = userId)
            if user != None and len(user) > 0:
                user.delete()
                dic["state"] = 1
                dic["message"] = "删除成功"
            else:
                dic["state"] = 2
                dic["message"] = "id不存在"

            doc = json.dumps(dic)
            return HttpResponse(doc)
    else:
        return Http404
