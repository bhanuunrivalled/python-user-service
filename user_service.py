class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, user_id, name, email):
        if user_id in self.users:
            raise ValueError(f"User {user_id} already exists")
        self.users[user_id] = {"name": name, "email": email}
        return self.users[user_id]

    def get_user(self, user_id):
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found")
        return self.users[user_id]

    def list_users(self):
        return list(self.users.values())

    def delete_user(self, user_id):
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found")
        del self.users[user_id]
