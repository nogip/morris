from abc import ABCMeta, abstractmethod


class IGroup(metaclass=ABCMeta):

    @abstractmethod
    def auth(self, token):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update_members(self):
        pass

    @abstractmethod
    def get_member_ids(self, category):
        pass

    @abstractmethod
    def set_exclude_ids(self, exclude):
        pass

    @abstractmethod
    def send(self, user_id, message, attachments):
        pass

    @abstractmethod
    def broadcast(self, users, message, attachments, sender_id=0):
        pass

    @abstractmethod
    def get_api(self):
        pass
