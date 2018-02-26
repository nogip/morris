from abc import ABCMeta, abstractmethod


class IStorage(metaclass=ABCMeta):

    @abstractmethod
    def update(self, update_users):
        pass

    @abstractmethod
    def get_users_ids(self, **kwargs):
        pass
