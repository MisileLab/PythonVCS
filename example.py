from pythonvcs.gitea import GiteaHandler
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "https://gitea.chizstudio.com/", api_key, False)

a = giteahandler.get_teams()

if a is not None:
    for i in a:
        print(i.organization.username)