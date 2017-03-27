#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import select
import time

class PoolTimeServer(object):
    std_mask = select.POLLERR | select.POLLHUP | select.POLLNVAL  #���ĵĴ����¼�
	
    def __init__(self,sock):
        self.master_sock = sock #��ȡsocket
        self.all_socks = {self.master_sock.fileno():self.master_sock} #�洢���е�socket��KEY���ļ���������value�Ƕ�Ӧ���׽���
        self.buffers = {} #key���ļ���������value�ǿͻ��˷���������
        self.p = select.poll() #��ȡpoll����,������ע������ĵ��¼�
        self.watch_read(self.master_sock.fileno()) #��ȡ���е��ļ�������
    
    def watch_read(self,fd):
        self.p.register(fd,select.POLLIN | self.std_mask) #��pollע���ļ�������������ĵ��¼��Ƕ�ȡ
		
    def watch_write(self,fd):
         self.p.register(fd,select.POLLOUT| self.std_mask) #��pollע���ļ�������������ĵ��¼���д��
    
    def watch_both(self,fd):
         self.p.register(fd,select.POLLOUT | select.POLLIN | self.std_mask) #��pollע���ļ�������������ĵ��¼��Ƕ�ȡ��д��
    
    def fd2socket(self,fd):
        return self.all_socks[fd] #�����ļ���������Ӧ���׽���
		
    def new_conn(self,c_sock):
        fd = c_sock.fileno() #��ȡ�ͻ����׽��ֵ��ļ�������
        self.all_socks[c_sock.fileno()] = c_sock #KEY���ļ���������value�Ƕ�Ӧ�Ŀͻ����׽���
        self.buffers[fd] = "Welcome!\n" #����Ҫ��ÿ���ͻ��˷��͵�����
        self.watch_both(fd) #ʹ�� watch_both������pollע��ͻ����׽���
		
    def close_out(self,fd):
        self.fd2socket(fd).close() #�ر��׽���
        self.p.unregister(fd) #ע���ļ������������ڹ�ϵ�κ��¼�
        del self.buffers[fd] #����˿ͻ�����Ҫ���͵�����
        del self.all_socks[fd] #����˿ͻ��˵��׽���
		
    def read_event(self,fd):
        data = self.fd2socket(fd).recv(1024)
        if not data: #�������Ϊ�վ�ִ��close_out����
            self.close_out(fd)
        else:
            self.buffers[fd] += data #���տͻ��˷��͵��������ֵ���
            self.watch_both(fd) #���Ķ�ȡ��д���¼�
			
    def write_event(self,fd):
        if not self.buffers[fd]: #����ļ������������ڵĻ�
            self.watch_read(fd) #���Ķ��¼�
            return
        byte_send = self.fd2socket(fd).send('[%s] %s' % (time.ctime(),self.buffers[fd])) #��ͻ��˷�������,����ȡ���͵��ֽ���
        self.buffers[fd] = self.buffers[fd][byte_send:] #ȡ����δ���͵�����
        if not self.buffers[fd]: #������͵������ѿ�
            self.watch_read(fd) #�ͼ�����ϵ���¼�
			
    def error_event(self,fd):
        self.close_out(fd)
		
    def mainloop(self):
        while True:
            result = self.p.poll() #���ļ���������������ĵ��¼���������ִ�У���������ִ�У�Ҳ���ǲ�����ѭ��
            for fd,event in result: #fd���ļ���������event���¼�
                if fd == self.master_sock.fileno(): #����ļ��������Ƿ����socket���ļ����������������¿ͻ�������
                    cli_sock,cli_addr = self.fd2socket(fd).accept() #�ͽ��տͻ�������
                    cli_sock.setblocking(False) #���ͻ����׽�����Ϊ������״̬
                    self.new_conn(cli_sock) #��new_conn�������ؿͻ����׽���
                elif event & select.POLLIN: #����Ƕ��¼�
                    self.read_event(fd)
                elif event & select.POLLOUT: #�����д�¼�
                    self.write_event(fd)
                else: #�Ȳ��Ƕ�Ҳ����д���Ǿ��Ǵ����¼�
                    self.error_event(fd)
					
if __name__ == '__main__':
#�󶨷�����׽���
    host = ''
    port = 12345
    addr = (host,port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(1)
    s.setblocking(False) #���÷�����׽���Ϊ������״̬
    pts = PoolTimeServer(s)
    pts.mainloop()