from orator.orm import has_many

from orm.db import Model


class Post(Model):
    @has_many
    def comments(self):
        from models.comment import Comments

        return Comments
