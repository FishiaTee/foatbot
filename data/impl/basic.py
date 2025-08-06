import os
import json
from .. import data_handler

class BasicDataHandler(data_handler.DataHandler):
    def write_to_disk(self):
        if not os.path.isdir(os.path.join(self.working_directory, "users")):
            os.mkdir(os.path.join(self.working_directory, "users"))
        for user in self.data['users'].keys():
            json.dump(self.data['users'][user], open(os.path.join(self.working_directory, "users", f"{str(user)}.json"), 'w'), indent=2)
        json.dump(self.data['server'], open(os.path.join(self.working_directory, "general.json"), 'w'), indent=2)
        return super().write_to_disk()