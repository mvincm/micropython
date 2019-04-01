# Complete project details at https://RandomNerdTutorials.com

import utime

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"></head>
  <body><h1>Hello, World! You are {counter} client today!</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

counter=0

while True:
  counter += 1
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Connection number',counter,' START time:',utime.ticks_ms()/1000)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response.format(counter=counter))
  conn.close()
  print('Connection number',counter,' STOP time:',utime.ticks_ms()/1000)