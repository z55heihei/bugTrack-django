__author__ = 'zhangyw'
# coding=utf-8
import simplejson as json

def __buildSuccJson__():
    rtnDic = {}
    rtnDic["state"] = 1
    doc = json.dumps(rtnDic)
    return doc

def __buildFailJson__(failReason=None):
    rtnDic = {}
    rtnDic["state"] = 2
    if failReason != None:
        rtnDic["failReason"] = failReason
    doc = json.dumps(rtnDic)
    return doc