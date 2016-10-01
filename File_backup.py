#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import time
import os
import tarfile
import hashlib
import pickle
 
def check_md5(fname): #MD5�����ļ�
    m = hashlib.md5() #��������
    with open(fname) as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #MD5��������
    return m.hexdigest() #�������ݼ��ܺ��MD5ֵ
 
def full_backup(): #��ȫ���ݺ���
    base_dir,back_dir = os.path.split(src_dir.rstrip('/')) #��/home/demo��/�Ų��Ϊ'/home', 'demo'
    back_name = '%s_full_%s.tar.gz' %(back_dir,time.strftime('%Y%m%d')) #���ñ����ļ�������
    full_path = os.path.join(dst_dir,back_name) #ƴ�ӱ����ļ����Ŀ��·��
 
    tar = tarfile.open(full_path,'w') #����tar.gz�ļ�
    tar.add(back_dir) #��demoĿ¼����ѹ������
    tar.close
 
    for path,dirs,files in os.walk(src_dir): #����Դ�����ļ�Ŀ¼
        md5dict = {}
        for each_file in files:
            full_name = os.path.join(path,each_file) #ƴ�ӱ����ļ��ľ���·��
            md5dict[full_name] = check_md5(full_name) #���ֵ䷽ʽ�洢�����ļ���MD5ֵ
    
    with open(md5file,'w') as fobj:
        pickle.dump(md5dict,fobj)
 
def incr_backup(): #��������
    new_md5 = {}
    with open(md5file) as fobj:
        old_md5 = pickle.load(fobj)
 
    base_dir,back_dir = os.path.split(src_dir.rstrip('/'))
    back_name = '%s_full_%s.tar.gz' %(back_dir,time.strftime('%Y%m%d'))
    full_path = os.path.join(dst_dir,back_name)
 
    for path,dirs,files in os.walk(src_dir):
        for each_file in files:
            full_name = os.path.join(path,each_file)
            new_md5[full_name] = check_md5(full_name)   
 
    with open(md5file,'w') as fobj:
        pickle.dump(new_md5,fobj)
    
    tar = tarfile.open(full_path)
    for key in new_md5:
        if old_md5.get(key) != new_md5[key]:
            tar.add(key.split(base_dir)[1].lstrip('/'))
    tar.close()
    
if __name__ == '__main__':
    src_dir = '/home/demo' #Դ�����ļ�Ŀ¼
    dst_dir = '/home/backup' #���ݺ��ļ���Ŀ¼
    md5file = '/home/backup/md5.data' #MD5У���ļ�
 
    if time.strftime('%a') == 'Mon': #�����ǰʱ��Ϊ��һ
        full_backup() #��ִ����ȫ����
    else:
        incr_backup() #�����ִ����������