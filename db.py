import redis

from abc import ABC, abstractmethod


class DB(ABC):
    @abstractmethod
    def set_task(self, task_id: str, status: str) -> None:
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> str:
        pass

    @abstractmethod
    def delete_task(self, task_id) -> None:
        pass


class RedisDB(DB):
    def __init__(self):
        self.__db = redis.Redis()

    def set_task(self, task_id, status):
        self.__db.mset({task_id: status})

    def get_task(self, task_id):
        response = self.__db.mget(task_id)[0].decode('utf-8')
        if response is None:
            return 'Task does not exist'
        return response

    def delete_task(self, task_id):
        self.__db.delete(task_id)
        return True
