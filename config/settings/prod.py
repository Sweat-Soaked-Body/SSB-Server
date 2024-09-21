from .base import *

environ.Env.read_env(os.path.join(BASE_DIR, 'prod.env'))
