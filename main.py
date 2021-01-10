from json.decoder import JSONDecodeError
from kivy.app import App
import json
from datetime import datetime
import random

# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown

USERS_DB_PATH = "data/users.json"


def check_credentials(username, password):
    with open(USERS_DB_PATH) as f:
        users = json.load(f)
        if username in users and users[username]["password"] == password:
            return True

        f.close()


def get_random_line(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()
        return random.choice(lines)


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def reset_pwd(self):
        pass

    def login(self):
        username, password = [
            self.ids[field].text for field in ["username", "password"]
        ]
        if check_credentials(username, password):
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_error_message.text = "Wrong credentials"


def _write(data):
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(USERS_DB_PATH, "r+") as f:
        content = {}
        try:
            content = json.load(f)
        except JSONDecodeError as e:
            pass

        content[data["username"]] = data
        f.seek(0)
        json.dump(content, f)
        f.close()


def write(data):
    try:
        _write(data)
    except FileNotFoundError:
        with open(USERS_DB_PATH, "w") as f:
            f.close()

        _write(data)


class SignUpScreen(Screen):
    def add_user(self):
        data = {k: v.text for k, v in self.ids.items()}
        write(data)
        self.manager.current = "sign_up_screen_success"

    def redirect_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class SignUpScreenSuccess(Screen):
    def redirect_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self):
        try:
            quote = get_random_line(f"data/{feeling}.txt")
            self.ids.quote.text = quote
        except NameError:
            self.ids.quote.text = (
                "You haven't selected a feeling. Select one and try again."
            )


class CustomDropDown(DropDown):
    def select(self, _feeling):
        global feeling
        feeling = _feeling


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
