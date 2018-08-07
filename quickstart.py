import os
import time
from tempfile import gettempdir

from config import config
from config import insta_lists

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

insta_username = config["instagram"]["username"]
insta_password = config["instagram"]["password"]

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  multi_logs=True)

try:
    session.login()

    # settings
    session.set_relationship_bounds(enabled=True,
				 potency_ratio=-1.21,
				  delimit_by_numbers=True,
				   max_followers=4590,
				    max_following=5555,
				     min_followers=45,
				      min_following=77)
    session.set_do_comment(True, percentage=10)
    session.set_comments(insta_lists.comments)

    # actions
    session.like_by_tags(insta_lists.tags, amount=20)

    # interacting with specific users
    session.set_do_follow(enabled=False, percentage=50)
    session.set_comments(["Cool", "Super!"])
    session.set_do_comment(enabled=True, percentage=80)
    session.set_do_like(True, percentage=70)
    session.interact_by_users(['user1', 'user2', 'user3'], amount=5, randomize=True, media='Photo')

    # Interact with the people that a given user is following
    # set_do_comment, set_do_follow and set_do_like are applicable
    session.set_user_interact(amount=5, randomize=True, percentage=50, media='Photo')
    session.set_do_follow(enabled=False, percentage=70)
    session.set_do_like(enabled=False, percentage=70)
    session.set_comments(["Cool", "Super!"])
    session.set_do_comment(enabled=True, percentage=80)
    session.interact_user_followers(['natgeo'], amount=10, randomize=True)

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
