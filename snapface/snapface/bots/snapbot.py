from argparse import ArgumentParser
import os
from snapface.dependency.snapchat_bots import SnapchatBot
from snapface.snapface.settings import PROJECT_ROOT


class Bot(SnapchatBot):
    # Friends
    add = True  # Auto add people who adds the bot
    delete = True  # Auto remove people who removes the bot
    friends = []
    # Bot actions
    storify = True  # If the bot should automaticly post incomming snaps to story
    # TODO: Add more actions
    # Store incomming
    store = False  # If the bot should save all incomming snaps to file, default botname in /static
    # Account
    username = None
    password = None

    def __init__(self):

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


if __name__ == '__main__':
    parser = ArgumentParser("Snapchat Bot")
    parser.add_argument('-u', '--username', required=True, type=str, help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str, help="Password of the account to run the bot on")

    args = parser.parse_args()

    bot = Bot(args.username, args.password)
    bot.listen(timeout=5)
