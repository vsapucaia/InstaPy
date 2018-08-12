from db.followings_3131 import followings
from db.followers_918 import followers


new = list(set(followings) - set(followers))

file = open('unfollow.py', 'w')
file.write(str(new))
