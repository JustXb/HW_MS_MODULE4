import os

c = get_config()

HUB_DATA_DIR = os.getenv("JUPYTERHUB_DATA_DIR", "/srv/jupyterhub-data")
WORK_DIR = os.getenv("JUPYTER_WORK_DIR", "/home/jovyan/work")


def env(name, default):
    return os.getenv(name, default)


c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.default_url = "/hub/spawn"
c.JupyterHub.db_url = f"sqlite:///{HUB_DATA_DIR}/jupyterhub.sqlite"
c.JupyterHub.cookie_secret_file = f"{HUB_DATA_DIR}/jupyterhub_cookie_secret"

c.JupyterHub.authenticator_class = "jupyterhub.auth.DummyAuthenticator"
c.JupyterHub.spawner_class = "jupyterhub.spawner.SimpleLocalProcessSpawner"
c.Authenticator.allow_all = True
c.Authenticator.allowed_users = {env("JUPYTERHUB_ADMIN_USER", "admin")}
c.DummyAuthenticator.password = env("JUPYTERHUB_ADMIN_PASSWORD", "admin")
c.ConfigurableHTTPProxy.check_running_interval = 15

c.Spawner.default_url = "/lab"
c.Spawner.notebook_dir = WORK_DIR
c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 120
c.Spawner.environment = {
    "POSTGRES_HOST": env("POSTGRES_HOST", "postgres"),
    "POSTGRES_PORT": env("POSTGRES_PORT", "5432"),
    "POSTGRES_DB": env("POSTGRES_DB", "oil_analytics"),
    "POSTGRES_USER": env("POSTGRES_USER", "admin"),
    "POSTGRES_PASSWORD": env("POSTGRES_PASSWORD", "admin"),
    "MINIO_ENDPOINT": env("MINIO_ENDPOINT", "http://minio:9000"),
    "MINIO_ACCESS_KEY": env("MINIO_ACCESS_KEY", "admin"),
    "MINIO_SECRET_KEY": env("MINIO_SECRET_KEY", "adminadmin"),
    "MINIO_BUCKET": env("MINIO_BUCKET", "oil-lake"),
}
