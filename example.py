from pythonvcs.gitea import GiteaHandler, GiteaAPIError
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "https://gitea.chizstudio.com/", api_key, False)

theme = giteahandler.get_settings().theme
print(theme)

try:
    giteahandler.change_setting("theme", "gitea")
except GiteaAPIError as e:
    print(e.raw_data.content)

theme = giteahandler.get_settings().theme
print(theme)

giteahandler.change_setting("theme", "arc-green")

theme = giteahandler.get_settings().theme
print(theme)