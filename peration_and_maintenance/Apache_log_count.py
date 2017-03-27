#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import re #��������ƥ��ģ��
 
def count_patt(fname,patt):
    patt_dict = {} #����ͳ���ֵ䣬{IP������}
    cpatt = re.compile(patt) #��ȡ�������
    with open(fname) as fobj: #������־�ļ�
        for line in fobj:
            m = cpatt.search(line) #����ƥ������
            if m: #�������ֵ��ΪNoneֵ�û�
                key = m.group() #��ƥ�䵽��ֵ��ΪKEY
                patt_dict[key] = patt_dict.get(key,0) + 1 #���KEY�����ֵ��о���ֵΪ1������ͼ�1
    return patt_dict #�����ֵ�
 
 
if __name__ == '__main__':
    log_file = '/var/log/httpd/access_log' #��־�ļ�·��
    ip_patt = '^(\d+\.){3}\d+' #ƥ��IP ��x.x.x.x
    br_patt = 'Mozilla|Chrome' #ƥ������������

    print(count_patt(log_file,ip_patt)) #��ӡ�ֵ�
    print(count_patt(log_file,br_patt))
