from pythonvcs.gitea import GiteaHandler
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("gitea_token")

giteahandler = GiteaHandler("MisileLaboratory", None, "http://chizstudio.com:49158/", api_key, False)