import os.path
import os

class Config(object):
    """Configuration object"""
    def __init__(self):
        super(Config, self).__init__()
        self.conf_dir = os.path.expanduser('~/.pytomato/')
        self.db_file = 'data.db'
        self._create_conf_dir()

    def _create_conf_dir(self):
        if os.path.isdir(self.conf_dir):
            return
        if os.path.exists(self.conf_dir):
            os.unlink(self.conf_dir)
        os.mkdir(self.conf_dir)

    def get_db_filename(self):
        return os.path.join(self.conf_dir, self.db_file)

conf = Config()

