#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债、可交换债的最新价进行"三线"和"高价折扣法"分析

__author__ = 'winsert@163.com'

import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")


from qqbot import _bot as bot
from sys import exit
from datetime import datetime

from cxcb import getCB #查询可转债模块
from cxhp import getHP #高价折扣模块
from cxwh import getWH #查询外汇模块
from cxjj import getJJ #查询基金模块
from cxqs import getQS #强赎模块
from cxindex import getIndex #指数模块

# 主程序
if __name__ == '__main__':
    
    startMsg = u'不挑戏，不逃戏，不入戏，不调戏'
    restStartMsg = 'Have a good Lunch !'
    restEndMsg = 'Good Afternoon !'
    endMsg =  "I will come back !"
    newPriceMsg =  u"没有可转债满足 买入条件。"
    HPriceMsg =  u"没有可转债满足 高价折扣法 。"
    WHmsg = u"外汇一切正常 !"
    JJmsg = u"基金一切正常 !"

    # 登录QQ
    bot.Login(['-q', '1569701115'])

    #接收信息的对象
    bl = bot.List('buddy', 'andy_python')
    if bl:
        b = bl[0]

    now_time = datetime.now()
    today_year = now_time.year
    today_month = now_time.month
    today_day = now_time.day
    #print today_year, today_month, today_day

    rest_starttime = datetime(today_year, today_month, today_day, 11, 29, 59) # 设定午间休息开始时间11:29:59。
    rest_endtime = datetime(today_year, today_month, today_day, 12, 59, 59) # 设定午间休息结束时间12:59:59。
    end_time = datetime(today_year, today_month, today_day, 14, 59, 59) # 设定程序每天运行的结束时间到当天的14:59:59。
    #print end_time

    print startMsg
    print
    bot.SendTo(b, startMsg)

    while datetime.now() < end_time:

        # 判断午体时间
        if datetime.now() >= rest_starttime and datetime.now() <= rest_endtime :
            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restStartMsg
            print 
            bot.SendTo(b, reststartMsg)

            time.sleep(5500)

            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restEndMsg
            print 
            bot.SendTo(b, restEndMsg)

        #print datetime.now()
        print time.asctime(time.localtime(time.time())) #显示查询时间

        # 三线分析：
        msglist = getCB() #查询是否有CB满足三线买入条件
        if len(msglist) == 0: #没有满足条件的CB
            print newPriceMsg
        else:    
            for msg in msglist: #有满足条件的CB
                print msg
                print
                bot.SendTo(b, msg)

        # 高价折扣法分析
        HPlist = getHP() #查询是否CB满足高价折扣法
        if len(HPlist) == 0: #没有满足高价折扣法的CB
            print HPriceMsg
            print
        else:
            for hpMsg in HPlist: #有满足高价折扣法的CB
                print hpMsg
                #print
                bot.SendTo(b, hpMsg)

        # 查询外汇价格是否低于预设值
        WHlist = getWH()
        if len(WHlist) == 0: #没有满足条件的外汇
            print WHmsg
            print
        else:
            for whMsg in WHlist: #有满足条件的外汇
                print whMsg
                bot.SendTo(b, whMsg)

        # 查询基金价格是否低于预设值
        JJlist = getJJ()
        if len(JJlist) == 0: #没有满足条件的基金
            print JJmsg
            print
        else:
            for jjMsg in JJlist: #有满足条件的基金
                print jjMsg
                bot.SendTo(b, jjMsg)

        time.sleep(150)  # 延时查询的秒数,300即延时5分钟查询一次。

    # 查询指数收盘的涨跌情况
    index = {u'上证50':'sh000016', u'沪深300':'sz399300', u'中证500':'sh000905', u'创业板':'sz399006', u'B股':'sh000003', u'国债':'sh000012'} #要查询的指数代码
    
    for k in index.keys():
        value = index.get(k)
        index_zz = getIndex(value)
        index_msg = k+' : '+index_zz
        print index_msg
        bot.SendTo(b, index_msg)

    #计算转债的强赎天数：
    qsMsgList = getQS()
    if len(qsMsgList) > 0:
        for qsMsg in qsMsgList:
            print qsMsg
            bot.SendTo(b, qsMsg)

    print time.asctime(time.localtime(time.time())) #显示查询时间
    bot.SendTo(b, endMsg)
    exit()
