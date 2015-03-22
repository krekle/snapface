# -*- coding: utf-8 -*-
import subprocess
import sys
from snapface.bots.bot import SenderBot

from snapface.database import (
    Column,
    db,
    Model,
    relationship,
    SurrogatePK,
)


class Bot(SurrogatePK, Model):
    __tablename__ = 'bot'
    name = Column(db.String(80), nullable=False)

    # Friend stuff
    add = Column(db.Boolean, default=False)
    delete = Column(db.Boolean, default=False)

    # Bot actions
    story = Column(db.Boolean, default=False)
    store = Column(db.Boolean, default=False)
    bot_pid = Column(db.String)
    # TODO: Add more actions

    # Store incomming
    store = Column(db.Boolean,
                   default=False)  # If the bot should save all incomming snaps to file, default botname in /static
    # Account
    username = Column(db.String, nullable=False)
    password = Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(Bot, self).__init__(**kwargs)

    def __repr__(self):
        return '<Bot({name})>'.format(name=self.name)

    def get_cmd_args(self):
        cmd_str = '-u %s -p %s -of %s' % (self.username, self.password, self.name)
        if self.store:
            cmd_str += ' --store'
        if self.add:
            cmd_str += ' --add'
        if self.delete:
            cmd_str += ' --delete'
        return cmd_str

    def start_bot(self):
        cmd_pwd = SenderBot.get_screen_cmd('snapface:%s' % self.name)
        cmd_args = self.get_cmd_args()
        cmd = cmd_pwd + ' ' + cmd_args
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Store the bots pid
        self.bot_pid = p.pid
        db.session.add(self)
        db.session.commit()

        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()


class Friend(SurrogatePK, Model):
    __tablename__ = 'friends'
    username = Column(db.String(80), unique=True, nullable=False)
    bot_id = Column('users', db.ForeignKey('bot.id'), nullable=False)
    bot = relationship('Bot', backref='friends')

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return 'Friend({name})'.format(name=self.username)
