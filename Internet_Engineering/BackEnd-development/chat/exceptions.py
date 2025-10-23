

class ChatRoomExistsError(Exception):
    def __init__(self, m):
        pass
        self.message = m

    def __str__(self):
        return self.message

