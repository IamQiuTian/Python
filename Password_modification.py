#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import sys #����ִ��ִ��ģ��
import paramiko #����ssh����ģ��
import threading #������߳�ģ��
 
def remote_comm(host,pwd,comm): 
    ssh = paramiko.SSHClient() #��ȡ�ͻ��˶���
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #ssh��¼ʱ�Զ�����YES
    ssh.connect(host,username='root',password=pwd) #���õ�¼�û�������
    stdin,stdout,stderr = ssh.exec_command(comm) #ִ������
    print(stdout.read(),) #��ӡ����ִ�еĽ��
    print(stderr.read(),) #��ӡ�������
 
if __name__ == '__main__':
    if len(sys,argv) != 4: #��������ʽ���ԵĻ����ʹ�ӡ��ȷ�������ʽ��Ϣ
        print("Usane:%s ipfile oldpass newpass") %sys.argv[0]
    else: #��������ʽ��ȷ���ͽ�����һ��ִ��
        ipfile = sys.argv[1] #��ȡip�ļ�
        oldpass = sys.argv[2] #��ȡ��ǰԶ�̷�����������
        newpass = sys.argv[3] #��ȡ�µ�����Ҳ����Ҫ�޸ĵ�����
        ch_pwd = 'echo %s | passwd --stdin root' %newpass #ִ�������޸ĵ�����
        fobj = open(ipfile) #��ip�ļ�
        for line in fobj: #����ip�ļ�
            ip = line.strip() #��ȡ�ļ���ÿ�е�IP
            t = threading.Thread(target=trmote_comm,args(ip,oldpass,ch_pwd)) #���������ݽ��������Զ��߳�ִ��
            t.start #ִ�г���