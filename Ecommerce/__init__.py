# import celery
from __future__ import absolute_import
from .celery import app as celery_app

# Auto initialize celery worker
# Example: celery -A proj worker -l info
# PS.: normal way is activate venv and use command inside terminal

# from subprocess import call
#
# call("chmod +x Ecommerce/script/celery_worker.sh", shell=True)
# call("./Ecommerce/script/celery_worker.sh", shell=True)

# call([".", "venv_Ecommerce/bin/activate"])
# call(["celery", "-A", "Ecommerce worker -l info"])
# call(["ls", "-l"])

