from dotenv import load_dotenv


def load_env():
    ENV_PATH = "./config/.env"
    load_dotenv(dotenv_path=ENV_PATH)
