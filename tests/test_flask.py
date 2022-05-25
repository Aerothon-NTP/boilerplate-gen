import os
import signal
import subprocess
import time
from pathlib import Path

import requests

from tests import templates


class TestFlask(templates.TestCase):
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class."""
        p = None
        folder = str(Path(__file__).parent.parent / "backend/Flask")

        try:
            p = subprocess.Popen(
                args=[f"cd {folder}; python3 app.py"],
                stdout=subprocess.PIPE,
                shell=True,
                preexec_fn=os.setsid,
            )

        except Exception as E:
            os.killpg(os.getpgid(cls.p.pid), signal.SIGTERM)
            raise E

        time.sleep(10)
        cls.p = p

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a setup_class
        method.
        """
        try:
            res = requests.delete(templates.DELETETODOS)
            assert res.status_code in templates.status_codes

        finally:
            print()
            os.killpg(os.getpgid(cls.p.pid), signal.SIGTERM)
            time.sleep(3)
