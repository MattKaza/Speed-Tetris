# import getopt
# import paramiko
# import socket
# import threading

#
# def main():
#     # Create a socket object.
#     ssh_port = 22
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.bind(('', ssh_port))
#         sock.listen(100)
#         print('[+] Listening for connection ...')
#         client, addr = sock.accept()
#     except Exception as e:
#         print(f'[-] Connection Failed: {str(e)}')
#         return
#     print('[+] Connection Established!')
#     # Creating a paramiko object.
#     try:
#         Session = paramiko.Transport(client)
#         Session.add_server_key(HOST_KEY)
#         paramiko.util.log_to_file('filename.log')
#         server = Server()
#         try:
#             Session.start_server(server=server)
#         except paramiko.SSHException:
#             print('[-] SSH negotiation failed.')
#             return
#         chan = Session.accept(10)
#         print('[+] Authenticated!')
#         chan.send("Welcome to Buffy's SSH")
#         while 1:
#             try:
#                 command = raw_input('Enter command: ').strip('\n')
#                 if command != 'exit':
#                     chan.send(command)
#                     print chan.recv(1024) + '\n'
#                 else:
#                     chan.send('exit')
#                     print('[*] Exiting ...')
#                     session.close()
#                     raise Exception('exit')
#             except KeyboardInterrupt:
#                 session.close()
#     except Exception, e:
#         print(f'[-] Caught exception: {str(e)}')
#         try:
#             session.close()
#         except:
#             pass
# if __name__ == '__main__':
#     main()
