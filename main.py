from json.decoder import JSONDecodeError
from kivy.app import App
import json
from datetime import datetime

# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def reset_pwd(self):
        pass


def write(data):
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("users.json", "r+") as f:
        content = {}
        try:
            content = json.load(f)
        except JSONDecodeError as e:
            print(e)
            pass

        content[data["username"]] = data
        f.seek(0)
        json.dump(content, f)
        f.close()


class SignUpScreen(Screen):
    def add_user(self, **kwargs):
        write(kwargs)
        self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def redirect_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
