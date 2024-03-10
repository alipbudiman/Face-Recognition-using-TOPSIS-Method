import firebase_admin, time, os
from livejson import File
from firebase_admin import credentials
from firebase_admin import db as firebasedb

class Database:
    def __init__(self):
        self.get_data = File("config/system_config.json")
        if self.__check_valid():
            self.use_firebase = self.get_data["use_firebase_database"]
        else:
            self.use_firebase = False
    
    def __check_valid(self):
        if not os.path.exists(self.get_data["firebase_database_path"]):
            return False
        return True


class DatabaseManager(Database):
    def __init__(self) -> None:
        super().__init__()
        if not self.use_firebase:
            raise Exception("Firebase Certificate is not found")
        self.config = self.get_data
        self.cred = credentials.Certificate(self.config["firebase_database_path"])
        firebase_admin.initialize_app(self.cred)
        self.ref = firebasedb.reference(url=self.config["firebase_db_uri"])
    
    def save_session(self, session_id, files):
        user_ref = self.ref.child("users").child(session_id)
        user_ref.update({
            "files": files,
            "lifetime":time.time() + self.config["firebase_delete_image_time"],
            "process":False,
        })
        return user_ref

    def session_update_proc_status(self, session_id, data=True):
        user_ref = self.ref.child("users").child(session_id)
        user_ref.update({"process":data})
    
    def remove_session(self, session_id):
        user_ref = self.ref.child("users").child(session_id).delete()
        return user_ref

    def get_session_detail(self, session_id):
        user_ref = self.ref.child("users").child(session_id).get()
        return user_ref
    
    def get_session_list(self):
        user_ref = self.ref.child("users").get()
        return user_ref

class LocalDatabaseManager(Database):
    def __init__(self) -> None:
        super().__init__()
        self.local_storage = {
            "user":{}
        }

    def save_session(self, session_id, files):
        user_ref = self.local_storage["user"]
        user_ref.update({
            session_id: {
                "files": files,
                "lifetime":time.time() + self.get_data["firebase_delete_image_time"],
                "process":False,
            }
        })
        return user_ref

    def session_update_proc_status(self, session_id, data=True):
        user_ref = self.local_storage["user"][session_id]
        user_ref["process"] = data
    
    def remove_session(self, session_id):
        del self.local_storage["user"][session_id]
        return self.local_storage["user"]

    def get_session_detail(self, session_id):
        user_ref = self.local_storage["user"][session_id]
        return user_ref
    
    def get_session_list(self):
        user_ref = self.local_storage["user"]
        return user_ref

