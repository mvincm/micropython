import network, utime, uselect, usocket

ssid = 'YourSSID'
password = 'YourPasswd'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

count = 0
while not station.isconnected():
	utime.sleep_ms(1)
	count += 1
	if count==10000:
		print('Not connected - give up!')
		break

CONTENT = b"""\
HTTP/1.0 200 OK

Hello world! You are #%d client today!
"""

def main():
    s = usocket.socket()

    full_addr = usocket.getaddrinfo("0.0.0.0", 80)
    print("Bind address information:", full_addr)
    addr = full_addr[0][-1]

    s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening...")

    counter = 0
        
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)

        client_stream = client_sock
        
        poll = uselect.poll()
        poll.register(client_stream, uselect.POLLIN)

        res = poll.poll(500)
        if not res:
          print("not ready - empty chrome connections")
          client_stream.close()
          continue

        favi = False
        
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
              break
            elif str(h).find("favicon.ico")==7:
              favi=True
              print("close connection for favicon")
              break
        if favi:
          client_stream.close()
          continue
          
        client_stream.write(CONTENT % counter)
        client_stream.close()
        counter += 1

main()