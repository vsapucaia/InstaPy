import os
import time
from tempfile import gettempdir
import random

from config import config
from config import lists

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

# username = config["instagram"]["username"]
# password = config["instagram"]["password"]
# username = config["instagram"]["username"] if config["instagram"]["username"] else os.environ['INSTA_USERNAME']
# password = config["instagram"]["password"] if config["instagram"]["password"] else os.environ['INSTA_PASSWORD']
username = os.environ['INSTA_USERNAME']
password = os.environ['INSTA_PASSWORD']


# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'

session = InstaPy(username=username,
                  password=password,
                  headless_browser=True,
                  multi_logs=True, bypass_suspicious_attempt=False)

try:
    session.login()

    # settings
    session.set_relationship_bounds(
        enabled=False, potency_ratio=-1.21, delimit_by_numbers=False,
        max_followers=4590, max_following=5555, min_followers=45, min_following=77
    )

    # Unfollow
    # uc = 20  # unfollow count
    # u_list = lists.next_to_unfollow(uc)  # unfollow list
    # session.unfollow_users(amount=uc, customList=(True, u_list, "all"), unfollow_after=None, sleep_delay=600)

    # defining generic environment
    session.set_dont_include(lists.friends)
    # session.set_user_interact(amount=1, randomize=True, percentage=80)
    session.set_do_follow(enabled=False)
    session.set_comments(lists.comments)

    # actions
    session.set_do_comment(enabled=True, percentage=60)
    session.like_by_tags(random.sample(lists.tags, 6), amount=5)

    # # interacting with specific users (FAMOUS)
    # session.set_do_comment(enabled=True, percentage=30)
    # session.interact_by_users(random.sample(lists.famous_people, 1), amount=1, randomize=True)

    # interacting with specific users (BANDS)
    session.set_do_comment(enabled=False)
    session.set_do_like(True, percentage=90)
    session.interact_by_users(random.sample(lists.band_or_music, 5), amount=1, randomize=True)

    # Interact with the people that a given user is following
    session.set_do_comment(enabled=False)
    session.set_do_like(True, percentage=30)
    session.interact_user_following(random.sample(lists.band_or_music, 15), amount=2, randomize=True)

    # Interact with the people that follow a given user
    # session.interact_user_followers(lists.famous_people, amount=10, randomize=True)

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
