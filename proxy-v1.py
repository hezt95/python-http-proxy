# -*- coding: utf-8 -*- 
import socket
import thread
import sys
import time
import re



def cli_proxy_socket(host_proxy,port_proxy):
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

	global addr
	conn,addr = sock.accept()
	return conn
#keep talking
def cli_proxy_data(conn,addr):
	try:
		print 'Connected with ' + addr[0] + ':' + str(addr[1])		
		recvdata_cli = conn.recv(81960)
		######
		#recvdatas += recvdata
		if (len(recvdata_cli)>0):	
			proxy_ser(recvdata_cli)		
			
		else:
			print 'Socket client to proxy trans complete'
	except socket.error,msgRece:
		print 'something wrong in receieve(client to proxy)',msgRece		
		conn.close()
		sock.close()
	return recvdata_cli
def proxy_ser(recvdata_cli):
	recvdatalist = re.split(r'\r\n', recvdata_cli) 
	Reqline = str(recvdatalist[0])
	try:
		sock_ser = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock_ser.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	except socket.error, e:
		print 'socket to server false:%s'%e

	print 'socket to server'
	
	print 'INFO:',Reqline
	host_ser = str(recvdatalist[1])[6:]
	print host_ser
	try:
		sock_ser.connect((host_ser,80))
	except socket.error, e:
		print 'connect to server false:%s'%e
	
	print 'connect to server'
	try:
		print'sending to server'
		senddata_ser = recvdata_cli
		sock_ser.send(senddata_ser)
	except socket.error,e:
		print 'send to server false:%s'%e
		sock_ser.close()

	recv_timeout(sock_ser,timeout=2)



def recv_timeout(the_socket,timeout=2):
	#make socket non blocking
	the_socket.setblocking(0)
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
			data = the_socket.recv(8192)
			if data:
				total_data.append(data)
				#change the beginning time for measurement
				begin = time.time()
			else:
				#sleep for sometime to indicate a gap
				time.sleep(0.1)
		except:
			pass
	#join all parts to make final 'string'
	global final_total_data
	final_total_data = ''.join(total_data)

	
def proxy_cli_data(conn_cli_pro,final_total_data):
	print final_total_data
	conn.send(final_total_data)


conn = cli_proxy_socket('',55555)
cli_proxy_data(conn,addr)
proxy_cli_data(cli_proxy_socket,final_total_data)



