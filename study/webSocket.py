import socket

HOST="0.0.0.0"
POST=8088
#application/json
#text/html
text_content = '''
HTTP/1.x 200
Content-Type: text/html

{
    name:yuan
    pwd:11
}
'''


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,POST))
count = 0
while True:
    s.listen(3)
    conn,addr = s.accept()
    request = conn.recv(1024).decode()
    method=request.split(" ")[0]
    src = request.split(' ')[1]
    count+=1
    print(count)
    print(addr)
    print(request)
    # if method=='GET':
    content=text_content
    # print('Connect by',addr)
    # print("Request id",request)
    conn.sendall(content.encode())
    conn.close()

