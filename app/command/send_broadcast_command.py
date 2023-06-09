from command.command import Command


class SendBroadcastCommand(Command):
    def __init__(self, server, socket, message):
        self.server = server
        self.socket = socket
        self.message = message

    def execute(self):
        self.server.broadcast(self.socket, self.message)
