# -*- coding: utf-8 -*-
import os
import uuid
from dependency.snapchat_bots import SnapchatBot
from dependency.daemon import Daemon

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
    bot_id = Column(db.String(80))
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
        bot_id = uuid.uuid4().hex[0:4]
        super(Bot, self).__init__(**kwargs)

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

    # Start the snapbot
    def start(self):
        outfolder = os.path.join(os.path.abspath(__file__ + '/../../../'), 'snaps/' + self.username + '/')
        print outfolder
        daemon = SnapDaemon(touch(outfolder + 'daemon.pid'), stdin=touch(outfolder + 'stin.txt'), stdout=touch(outfolder + 'stout.txt'),
                            stderr=touch(outfolder + 'stderr.txt'))
        daemon.execute_daemon(self, 'start', daemon)

    # Stop the snapbot
    def stop(self):
        SnapDaemon(self.username, self, 'stop')

    def test_start(self):
        self.listen(10)

    # Callback for the daemon
    def run_daemon(self):
        try:
            if self.bot_id:
                pass
        except AttributeError:
            SnapchatBot.__init__(self.username, self.password)
        # Start the snapchatbot
        self.listen(5)



def touch(path):
    open(path, 'a').close()
    return path


class Friend(SurrogatePK, Model):
    __tablename__ = 'friends'
    username = Column(db.String(80), unique=True, nullable=False)
    bot_id = Column('users', db.ForeignKey('bot.id'), nullable=False)
    bot = relationship('Bot', backref='friends')

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return 'Friend({name})'.format(name=self.username)


# To run the snap as a daemon
class SnapDaemon(Daemon):
    # Referance to the snapbot
    bot = None

    def run(self):
        if self.bot:
            self.bot.run_daemon()

    @staticmethod
    def execute_daemon(bot, command, daemon):
        daemon = daemon
        if not bot:
            sys.exit(2)
            return None
        else:
            daemon.bot = bot
            if command:
                if 'start' == command:
                    daemon.start()
                elif 'stop' == command:
                    daemon.stop()
                elif 'restart' == command:
                    daemon.restart()
                else:
                    print "Unknown command"
                    sys.exit(2)
                sys.exit(0)
            else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)