import os
import time
from tempfile import gettempdir

from config import config
from config import lists

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

username = config["instagram"]["username"]
password = config["instagram"]["password"]

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'

session = InstaPy(username=username,
                  password=password,
                  headless_browser=False,
                  multi_logs=True)

try:
    session.login()

    # settings
    session.set_relationship_bounds(enabled=True,
				 potency_ratio=-1.21,
				  delimit_by_numbers=False,
				   max_followers=4590,
				    max_following=5555,
				     min_followers=45,
				      min_following=77)
    session.set_do_comment(True, percentage=10)
    session.set_comments(lists.comments)

    # actions
    session.like_by_tags(lists.tags, amount=2)

    # # defining generic environment
    # session.set_dont_include(lists.friends)
    # session.set_user_interact(amount=1, randomize=True, percentage=80)
    # session.set_do_follow(enabled=False)
    # session.set_do_like(True, percentage=90)
    # session.set_comments(lists.comments)
    # session.set_do_comment(enabled=True, percentage=30)
    #
    # # interacting with specific users
    # session.interact_by_users(lists.famous_people, amount=5, randomize=True)
    #
    # # Interact with the people that a given user is following
    # session.interact_user_followers(lists.famous_people, amount=10, randomize=True)
    #
    # # Interact with the people that a given user is following
    # session.interact_user_followers(lists.famous_people, amount=10, randomize=True)
    #
    # # Unfollow
    # custom_list = ["user_1", "user_2", "user_49", "user332", "user50921", "user_n"]
    # session.unfollow_users(amount=20, customList=(True, custom_list, "nonfollowers"), style="RANDOM",
    #                        unfollow_after=None, sleep_delay=600)


except Exception as exc:
    # if changes to IG layout, upload the file to help us locate the change
    if isinstance(exc, NoSuchElementException):
        file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
        with open(file_path, 'wb') as fp:
            fp.write(session.browser.page_source.encode('utf8'))
        print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
            '*' * 70, file_path))
    # full stacktrace when raising Github issue
    raise

finally:
    # end the bot session
    session.end()
