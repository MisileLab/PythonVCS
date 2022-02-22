from pythonvcs.gitea import GiteaHandler, GiteaRepoOption
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "https://gitea.chizstudio.com/", api_key, False)
for i, i2 in enumerate(giteahandler.get_repositories()):
    print(i)
    print(i2.url)

a = giteahandler.create_repository(GiteaRepoOption(name="test"))

print(a.url)

for i in giteahandler.get_repositories():
    print(i.url)