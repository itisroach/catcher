import os
from dotenv import load_dotenv

load_dotenv()

def ReadEnvVar(name: str):
    value = os.getenv(name)

    return value