import pickle
import os
import datetime
import time
import hashlib  # this should be done in client

PASSWORD = 0
STORAGE = 2
IS_LOGGED = 1
USER_ALREADY_EXISTS = 11
USER_ADDED = 10
LOGIN_SUCCESS = 12
INCORRECT_PASSWORD = 13
USER_NOT_EXIST = 14
LOGOUT_SUCCESS = 15
USER_ALREADY_LOGGED_OUT = 16
MAX_LOGIN_COUNT = 5
FILE_STORAGE = 'file_storage\\'


def calcMd5(psf):
    res = hashlib.md5(psf.encode())
    # printing the equivalent hexadecimal value.
    # this should be in client
    print("The hexadecimal equivalent of hash is : ", end="")
    hexPass = res.hexdigest()
    return hexPass


class RegisterLogin:
    def __init__(self):
        self.userFile = "usersDB.pkl"
        self.users = {}

        if os.path.exists(self.userFile):
            with open(self.userFile, 'rb') as handle:
                self.users = pickle.load(handle)

    def __delitem__(self, key):
        if key in self.users.keys():
            del self.users[key]
            with open(self.userFile, 'wb') as handle:
                pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        return False

    def register(self, username, psf):
        if username in self.users.keys():
            return USER_ALREADY_EXISTS, None
        else:
            storage = ''
            i = 1
            while True:  # Creates a directory for user
                try:
                    storage = FILE_STORAGE + username + str(i)
                    os.mkdir(storage)
                    break
                except FileExistsError:
                    i += 1
            self.users[username] = [psf, True,
                                    storage]  # gives users values of password, is he logged in, storage space
            with open(self.userFile, 'wb') as handle:
                pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return USER_ADDED, self.users[username]

    def login(self, username, psf):
        if username in self.users.keys():
            password = self.users[username][PASSWORD]
            if password == psf:
                self.users[username][IS_LOGGED] = True
                with open(self.userFile, 'wb') as handle:
                    pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return LOGIN_SUCCESS, self.users[username]
            else:
                return INCORRECT_PASSWORD, ''
        else:
            return USER_NOT_EXIST, ''

    def logout(self, username):
        if username in self.users.keys():
            data = self.users[username]
            if data[IS_LOGGED]:
                self.users[username][IS_LOGGED] = False
                with open(self.userFile, 'wb') as handle:
                    pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return LOGOUT_SUCCESS
            else:
                return USER_ALREADY_LOGGED_OUT
        else:
            return USER_NOT_EXIST

    def printUsers(self):
        for key in self.users.keys():
            print(key, self.users[key])


if __name__ == "__main__":
    u = RegisterLogin()
    # Tests.
    u.printUsers()
