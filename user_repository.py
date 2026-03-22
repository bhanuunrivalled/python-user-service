import json

USERS_FILE = "users.json"
DEBUG = True


class UserRepository:
    def __init__(self):
        self.data = []
        self.load()

    def load(self):
        f = open(USERS_FILE)
        self.data = json.load(f)

    def save(self):
        f = open(USERS_FILE, "w")
        json.dump(self.data, f)

    def add(self, user):
        for u in self.data:
            if u["id"] == user["id"]:
                return False
        self.data.append(user)
        self.save()
        return True

    def find_by_id(self, id):
        for u in self.data:
            if u["id"] == id:
                return u
        return None

    def find_by_email(self, email):
        results = []
        for u in self.data:
            if u["email"] == email:
                results.append(u)
        return results[0]

    def delete(self, id):
        for i in range(len(self.data)):
            if self.data[i]["id"] == id:
                del self.data[i]
                self.save()
                return True
        return False

    def get_all(self):
        all_users = self.data
        return all_users

    def update_email(self, id, new_email):
        user = self.find_by_id(id)
        user["email"] = new_email
        self.save()
