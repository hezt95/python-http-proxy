# -*- coding: utf-8 -*- 
import socket
import thread
import sys
import time
import re

def cli_proxy_recvdata(conn,addr):
	try:
		print 'Connected with ' + addr[0] + ':' + str(addr[1])		
		data = conn.recv(8196)
		return data
	except socket.error,msgRece:
		print 'something wrong in receieve(client to proxy)',msgRece		
		conn.close()
		sock.close()

def proxy_ser_socket(data):
	if (len(data)>0):
		#prosess the recvdata	
		datalist = re.split(r'\r\n', data) 
		Reqline = str(datalist[0])
		host = str(datalist[1])[6:]
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

		except socket.error, e:
			print 'Socket to server false:%s'%e			
		print 'Creat socket with server'
		print 'INFO:',Reqline
		
		try:
			sock.connect((host,80))
		except socket.error, e:
			print 'Connect to server false:%s'%e
		print 'Connect to server'
		try:
			print'Sending to server'
			sock.send(data)
		except socket.error,e:
			print 'Send to server false:%s'%e
			sock.close()
		return sock
		
	else:
		print 'Proxy cannot get data from client'

	
	
def recv_data_ser_send(sock_ser,sock_conn_cli,timeout=2):
	#it can make all data into one variable:final_total_data(str)
	#make socket non blocking
	sock_ser.setblocking(0)
	#total data partwise in an array
	total_data=[]
	data=''
	#beginning time
	begin=time.time()#get time now
	while 1:
		#if you got some data, then break after timeout
		if total_data and time.time()-begin > timeout:
			 break
		#if you got no data at all, wait a little longer, twice the timeout
		elif time.time()-begin > timeout*2:
			break
		#recv something
		try:
			data = sock_ser.recv(1024)
			total_data.append(data)
			#change the beginning time for measurement
			begin = time.time()
			#sleep for sometime to indicate a gap
			time.sleep(0.1)
		except:
			pass
	#join all parts to make final 'string'
	final_total_data = ''.join(total_data)
	return final_total_data

#调用函数
def main(host_proxy,port_proxy):
	#while 1:
		#client to proxy socket
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)	
		except socket.error, e:
			print 'socket client to proxy false:%s'%e
		print 'Socket client to proxy created'
		try:
			sock.bind((host_proxy, port_proxy))
		except socket.error , e:
			print 'Bind client to proxy failed:%s'%e
			sys.exit()
		print 'Socket client to proxy bind complete'
		sock.listen(5)
		print 'Socket client to proxy now listening'
		conn,addr = sock.accept()#connection
		
		recvdata_cli = cli_proxy_recvdata(conn,addr)#recieve data from client include the request line 
		sock_ser = proxy_ser_socket(recvdata_cli)
		final_total_data = recv_data_ser_send(sock_ser,conn,timeout=2)
		conn.send(final_total_data)
		conn.close()
		sock.close()

main('',55555)



