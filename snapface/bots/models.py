# -*- coding: utf-8 -*-
from dependency.snapchat_bots import SnapchatBot
import daemon

from snapface.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Bot(SurrogatePK, Model, SnapchatBot):
    __tablename__ = 'bot'
    name = Column(db.String(80), nullable=False)
    # Friend stuff
    add = Column(db.Boolean, default=False)
    delete = Column(db.Boolean, default=False)

    # Bot actions
    story = Column(db.Boolean, default=False)
    store = Column(db.Boolean, default=False)
    # TODO: Add more actions

    # Store incomming
    store = Column(db.Boolean,
                   default=False)  # If the bot should save all incomming snaps to file, default botname in /static
    # Account
    username = Column(db.String, nullable=False)
    password = Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(Bot, self).__init__(**kwargs)
        # db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Bot({name})>'.format(name=self.name)

    '''
    Snap specific methods
    '''
    ## Event handlers
    def on_snap(self, sender, snap):
        if self.storify:
            self.post_story(snap)
        if self.store:
            snap.save(dir_name=os.path.join(PROJECT_ROOT, 'snaps'))

    def on_friend_add(self, friend):
        if self.add:
            self.add_friend(friend)

    def on_friend_delete(self, friend):
        if self.delete:
            self.delete_friend(friend)

    def run_daemon(self):
        with daemon.DaemonContext():
            bot = SnapchatBot(self.username, self.password)
            bot.listen()


class Friend(SurrogatePK, Model):
    __tablename__ = 'friends'
    username = Column(db.String(80), unique=True, nullable=False)
    bot_id = Column('users', db.ForeignKey('bot.id'), nullable=False)
    bot = relationship('Bot', backref='friends')

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return 'Friend({name})'.format(name=self.username)