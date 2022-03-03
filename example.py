from pythonvcs.gitea import GiteaHandler
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "https://gitea.chizstudio.com/", api_key, False)

for i in giteahandler.get_starred_repositories():
    print(i.name)
giteahandler.star_repository("MisileLaboratory", "base-repository")

for i in giteahandler.get_starred_repositories():
    print(i.name)
giteahandler.unstar_repository("MisileLaboratory", "base-repository")

for i in giteahandler.get_starred_repositories():
    print(i.name)
giteahandler.star_repository("MisileLaboratory", "base-repository")