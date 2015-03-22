from argparse import ArgumentParser
import os

from snapchat_bots.bot import SnapchatBot


class SenderBot(SnapchatBot):
    db_bot = None
    outfolder = None
    store = False
    add = False
    delete = False

    def on_snap(self, sender, snap):
        if self.story:
            self.post_story(snap)
        if self.store:
            snap.save(dir_name=os.path.join(self.outfolder, 'snaps'))

    def on_friend_add(self, friend):
        if self.add:
            self.add_friend(friend)

    def on_friend_delete(self, friend):
        if self.delete:
            self.delete_friend(friend)

    @staticmethod
    def get_screen_cmd(name):
        # Create cli-type arguments
        cmd = 'screen -S %s -d -m python %s' % (name, SenderBot.get_path())
        # Make sure we get the py file and not the pyc
        cmd = cmd.replace('.pyc', '.py')
        return cmd

    @staticmethod
    def get_path():
        return os.path.abspath(__file__)

# Running the bot
if __name__ == '__main__':
    parser = ArgumentParser("Storifier Bot")
    parser.add_argument('-u', '--username', required=True, type=str,
                        help="Username of the account to run the bot on")
    parser.add_argument('-p', '--password', required=True, type=str,
                        help="Password of the account to run the bot on")
    parser.add_argument('-of', '--outfolder', required=True, type=str, help="Folder to save logs and snaps")
    parser.add_argument('-s', '--store', action='store_true', default=False)
    parser.add_argument('-a', '--add', action='store_true', default=False)
    parser.add_argument('-d', '--delete', action='store_true', default=False)

    args = parser.parse_args()

    # Initialize the bot and configure
    bot = SenderBot(args.username, args.password)
    bot.outfolder = os.path.join(os.path.abspath(__file__ + '/../../../'), 'snaps/' + args.outfolder + '/')
    bot.store = args.store
    bot.add = args.add
    bot.delete = args.delete

    #Start the bot
    bot.listen()
