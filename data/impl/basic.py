import os
import json
import pathlib
import sys
from .. import data_handler
sys.path.append("../..")
from logger import logger

class BasicDataHandler(data_handler.DataHandler):
    def write_to_disk(self):
        logger.info("writing all data to disk...")
        if not os.path.isdir(os.path.join(self.working_directory, "users")):
            os.mkdir(os.path.join(self.working_directory, "users"))
        for user in self.data['users'].keys():
            logger.verbose(f"writing data for user {user}...")
            json.dump(self.data['users'][user], open(os.path.join(self.working_directory, "users", f"{str(user)}.json"), 'w'), indent=2)
        logger.verbose("writing server data...")
        json.dump(self.data['server'], open(os.path.join(self.working_directory, "general.json"), 'w'), indent=2)
        logger.success("data write done.")
        return super().write_to_disk()
    def read_from_disk(self):
        logger.info("reading data from disk...")
        for file in os.listdir(os.path.join(self.working_directory, "users")):
            logger.verbose(f"reading data for user {pathlib.Path(os.path.join(self.working_directory, "users", file)).stem}...")
            user_data = json.load(open(os.path.join(self.working_directory, "users", file)))
            self.data['users'][pathlib.Path(os.path.join(self.working_directory, "users", file)).stem] = user_data
        logger.verbose("reading server data...")
        server_data = json.load(open(os.path.join(self.working_directory, "general.json")))
        self.data['server'] = server_data
        logger.success("data read done.")
        return super().read_from_disk()