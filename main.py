from kivy.app import App
from Views.views_manager import get_main_window


class MainApp(App):
    def build(self):
        return get_main_window()


def output_in_txt(arg_path, arg_str):
    file = open(arg_path, "w", encoding="utf-8")
    file.write(arg_str)
    file.close()


def main():
    MainApp().run()


if __name__ == '__main__':
    main()

