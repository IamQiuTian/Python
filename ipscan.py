#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os #����ϵͳ����ִ��ģ��
import threading #������߳�ģ��
def ping(ip): #����ping�������������ip����
    res = os.system('ping -c2 %s &> /dev/null' %ip) #ִ��ping��������ip����
    if res: #�������ֵΪ1���ͱ�ʾ�����Ǵ��״̬
        print('%s:down') %ip
    else: #�����������
        print('%s:up') %ip
		
for i in range(1,255):
    ipaddr = '10.141.50.%s' %ip #ʹ��forѭ������10.141.50.1-255
    t = threading.Thread(target=ping,args=(ipaddr)) #���ö��̣߳���ipaddr���ݽ�����������
    t.start() #ִ�г���
