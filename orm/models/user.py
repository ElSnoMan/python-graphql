from orator.orm import has_many

from orm.db import Model


class User(Model):
    @has_many
    def posts(self):
        from models.post import Post

        return Post

    @has_many
    def comments(self):
        from models.comment import Comments

        return Comments
