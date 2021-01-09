from kivy.app import App

# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def reset_pwd(self):
        pass


class SignUpScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
