""" Quickstart script for InstaPy usage """
# imports
from instapy import InstaPy
from instapy.util import smart_run

import random
from config import config
from config import lists

# username = os.environ['INSTA_USERNAME'] or config["instagram"]["username"]
# password = os.environ['INSTA_PASSWORD'] or config["instagram"]["password"]
username = config["instagram"]["username"]
password = config["instagram"]["password"]

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=username,
                  password=password,
                  headless_browser=True)

with smart_run(session):
    """ Activity flow """
    # settings
    session.set_relationship_bounds(
        enabled=False, potency_ratio=-1.21, delimit_by_numbers=False,
        max_followers=4590, min_followers=45, min_following=77
    )

    # Unfollow
    uc = 20  # unfollow count
    u_list = lists.next_to_unfollow(uc)  # unfollow list
    session.unfollow_users(amount=uc, customList=(True, u_list, "all"), unfollow_after=None, sleep_delay=600)

    print('>>>>> #VSF: FINISHED UNFOLLOW <<<<<')

    # defining generic environment
    session.set_dont_include(lists.friends)
    session.set_dont_like(lists.dont_likes)
    session.set_ignore_if_contains(lists.ignore_list)
    session.set_user_interact(amount=1, randomize=True, percentage=80)
    session.set_do_follow(enabled=False)
    session.set_comments(lists.comments)

    # REGULAR LIKES
    session.set_do_comment(enabled=True, percentage=60)
    session.like_by_tags(random.sample(lists.tags, 8), amount=10)

    print('>>>>> #VSF: FINISHED LIKE BY TAGS <<<<<')

    # # interacting with specific users (FAMOUS)
    # session.set_do_comment(enabled=True, percentage=30)
    # session.interact_by_users(random.sample(lists.famous_people, 1), amount=1, randomize=True)

    # interacting with specific users (BANDS)
    session.set_do_comment(enabled=False)
    session.set_do_like(True, percentage=90)
    session.interact_by_users(random.sample(lists.band_or_music, 5), amount=1, randomize=True)

    print('>>>>> #VSF: FINISHED LIKE BANDS <<<<<')

    # Interact with the people that a given user is following
    session.set_user_interact(amount=3, percentage=90, randomize=True)
    session.set_do_comment(enabled=True, percentage=30)
    session.set_do_like(True, percentage=90)
    session.interact_user_following(lists.indie_influencers, amount=3, randomize=True)
    print('>>>>> #VSF: FINISHED INTERACTING INFLUENCERS <<<<<')
    session.interact_user_following(random.sample(lists.band_or_music, 6), amount=3, randomize=True)
    print('>>>>> #VSF: FINISHED INTERACTING BANDS <<<<<')
