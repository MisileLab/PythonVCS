from pythonvcs.gitea import GiteaHandler
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "http://chizstudio.com:49158/", api_key, False)

for i in giteahandler.get_followers():
    print(i.name)

for i in giteahandler.get_followings():
    print(i.name)

giteahandler.unfollow_user("furluck_")
assert giteahandler.get_followings() == []
giteahandler.follow_user("furluck_")
assert giteahandler.get_followings() != []