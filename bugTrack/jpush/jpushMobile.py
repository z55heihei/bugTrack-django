# coding=utf-8
__author__ = 'zhangyw'
import jpush as  jpush
from conf import app_key, master_secret
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def jpushios(obj):
    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    push.audience = jpush.all_

    name = Name(obj)
    project = Project(obj)
    content = obj.content
    version = Version(obj)
    urgency = Urgency(obj)
    module  = Module(obj)
    distribter = Distribter(obj)

    msgdict = [name, u'在', project,version,u'版本',module,u'中',u'发现一个',urgency,u'问题',u':',content]
    msg = ''.join(msgdict)

    push.audience = jpush.audience(
        jpush.alias(distribter)
    )
    ios_msg = jpush.ios(alert=msg, badge="+1", sound="a.caf", extras={'k':'v'})
    push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
    push.notification = jpush.notification(alert="", ios=ios_msg)
    push.platform = jpush.platform("ios")
    push.send()

def Distribter(obj):
    username = obj.distribter.username
    return username

def Module(obj):
    module = obj.module.modules
    return module

def Version(Bug):
    version = Bug.version.version
    return version

def Name(obj):
    name = obj.name.username
    return name

def Project(obj):
    project =  obj.project.project
    return project

def Urgency(obj):
    urgencyItem = {"1":u'低',"2":u'中',"3":u'高',"4":u'严重'}
    return urgencyItem[obj.urgency]
