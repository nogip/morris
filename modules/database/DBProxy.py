from modules.database.interfaces.IStorage import IStorage


class DBProxy(IStorage):

    __database__ = None

    def __init__(self, db_class):
        self._db = db_class
        self._db.init_db()

    def update(self, update_users):
        upd_users_ids = [user.id for user in update_users]
        cur_count = self._db.count()
        if len(upd_users_ids) != cur_count:
            cur_users_ids = set(self._db.get_members_ids())
            difference = cur_users_ids.symmetric_difference(upd_users_ids)
            if len(cur_users_ids) > len(upd_users_ids):
                for user_id in difference:
                    self._db.delete_member(user_id)
            else:
                for user in update_users:
                    if user.id in difference:
                        self._db.add_member(user)
            self._count = self._db.count()

    def get_users_ids(self, **kwargs):
        return self._db.get_members_ids(**kwargs)

    def get_member(self, uid):
        return self._db.get_member(uid)

if __name__ == '__main__':
    db = DBProxy()
    db.update()
    print(db.get_users_ids())