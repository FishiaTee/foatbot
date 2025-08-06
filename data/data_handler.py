import os

class DataHandler:
    working_directory = ""
    data = {
        "users": {},
        "server": {
            "goon_exp_gain": 3,
            "goon_exp_next_multiplier": 1.5
        }
    }
    def __init__(self, dir):
        self.working_directory = os.path.normpath(dir)
        if not os.path.isdir(self.working_directory):
            os.mkdir(self.working_directory)
            self.write_to_disk()
        else:
            self.read_from_disk()
        pass
    def init_user(self, id):
        self.data['users'][id] = {
            "goon": {
                "exp": 0,
                "exp_next": 20,
                "exp_gain_multiplier": 1.5,
                "level": 1,
                "total_count": 0,
                "goon_history": [],
                "competitive": {
                    "rank": 1,
                    "match_history": [],
                   "records": {}
                }
            }
        }
    def read_from_disk(self):
        pass
    def write_to_disk(self):
        pass