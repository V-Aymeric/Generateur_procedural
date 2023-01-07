from kivy.app import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from Views.bitmap_generator import generate_image
from Views.bitmap_generator import basic_image
from Statistics.input_data import InputData
from Statistics.input_data import PercentageKeys
from generators import perlin_generator
from generators import grammary_generator
from generators import poisson_points_generator
from generators import str_to_tab

from threading import Thread
import pathlib
import queue


class MainWindow(Screen):
    print(str(pathlib.Path().absolute()))
    Builder.load_file("./Views/kv/main_window.kv")
    Builder.load_file("./Views/kv/IntInputBox.kv")
    Builder.load_file("./Views/kv/CheckBoxWithLabel.kv")
    #window_width = NumericProperty(Window.size[0])
    #window_height = NumericProperty(Window.size[1])

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.perlin_toggle = self.ids.perlin_method.ids.toggle
        self.grammary_toggle = self.ids.grammary_method.ids.toggle
        self.poisson_points_toggle = self.ids.poisson_method.ids.toggle

        self.seed_input_text = self.ids.seed.ids.value
        self.path_input_text = self.ids.path

        self.seed_input_text.bind(text=self.check_seed)
        self.path_input_text.bind(text=self.check_seed)

        self.water_slider = self.ids.ocean.ids.value #self.ids.water_slider
        self.beach_slider = self.ids.beach.ids.value #self.ids.beach_slider
        self.plain_slider = self.ids.plains.ids.value #self.ids.plain_slider
        self.mountain_slider = self.ids.mountain.ids.value #self.ids.mountain_slider

        self.water_slider.bind(text=self.set_data_water)
        self.beach_slider.bind(text=self.set_data_beach)
        self.plain_slider.bind(text=self.set_data_plain)
        self.mountain_slider.bind(text=self.set_data_mountain)

        self.generate_button = self.ids.generate_button

        self.mythread = None
        self.input_data = InputData()
        self.input_data.add_percentage(PercentageKeys.WATER, 40)
        self.input_data.add_percentage(PercentageKeys.BEACH, 5)
        self.input_data.add_percentage(PercentageKeys.PLAINS, 45)
        self.input_data.add_percentage(PercentageKeys.MOUNTAIN, 10)
        self.input_data.set_age(1)

        self.img_world_map = self.ids.world_map
        #self.test_label = self.ids.tester
        self.value_image = [None, None]

        self.img_world_map.texture = basic_image().texture

    def generate_file(self):

        if self.perlin_toggle.active:
            self.__generate_perlin()
            popup = Popup(
                title='Generation Progress',
                content=Label(text="Progression en cours"),
                size=(400, 400)
            )
            self.generate_world_map()
        elif self.poisson_points_toggle.active:
            self.__generate_poisson_points()
            self.generate_world_map()
        else:
            self.__generate_grammary()
            self.generate_world_map()

    def __generate_perlin(self):
        queue_thread = queue.Queue()
        #self.mythread = Thread(
        #    target=perlin_generator,
        #    args=(
        #        self.seed_input_text.text,
        #        self.path_input_text.text,
        #        self.input_data
        #    )
        #)
        self.mythread = Thread(
            target=lambda q, arg1, arg2, arg3: q.put(perlin_generator(arg1, arg2, arg3)),
            args=(
                queue_thread,
                self.seed_input_text.text,
                self.path_input_text.text,
                self.input_data
            )
        )
        self.mythread.start()
        self.mythread.join()
        self.value_image = str_to_tab(queue_thread.get())

    def __generate_grammary(self):
        queue_thread = queue.Queue()
        #self.mythread = Thread(
        #    target=grammary_generator,
        #    args=(
        #        self.seed_input_text.text,
        #        self.path_input_text.text,
        #        self.input_data
        #    )
        #)
        self.mythread = Thread(
            target=lambda q, arg1, arg2, arg3: q.put(
                grammary_generator(arg1, arg2, arg3)),
            args=(
                queue_thread,
                self.seed_input_text.text,
                self.path_input_text.text,
                self.input_data
            )
        )
        self.mythread.start()
        self.mythread.join()
        self.value_image = str_to_tab(queue_thread.get())

    def __generate_poisson_points(self):
        queue_thread = queue.Queue()
        self.mythread = Thread(
            target=lambda q, arg1, arg2, arg3: q.put(poisson_points_generator(arg1, arg2, arg3)),
            args=(
                queue_thread,
                self.seed_input_text.text,
                self.path_input_text.text,
                self.input_data
            )
        )
        self.mythread.start()
        self.mythread.join()
        self.value_image = str_to_tab(queue_thread.get())

    def generate_world_map(self):
        print("value_image 0 0 = " + str(self.value_image[0][0]))
        if None not in self.value_image:
            data_img = generate_image(self.value_image)
            self.img_world_map.texture = data_img.texture

    def __verify_percentages(self):
        if "" in [self.water_slider.text,
                  self.beach_slider.text,
                  self.plain_slider.text,
                  self.mountain_slider.text]:
            return False
        if int(self.water_slider.text) + \
            int(self.beach_slider.text) + \
            int(self.plain_slider.text) + \
            int(self.mountain_slider.text) != 100:
            return False
        return True

    def __verify_seed(self):
        seed = self.seed_input_text.text
        if len(seed) != 6:
            return False
        if int(seed) > 999999 or int(seed) < 99999:
            return False
        return True

    def __check_info(self):
        if self.__verify_percentages() and self.__verify_seed() and self.path_input_text.text != "":
            self.generate_button.disabled = False
            return
        self.generate_button.disabled = True

    def check_seed(self, instance, value):
        self.__check_info()

    def set_data_water(self, instance, value):
        if value != "":
            self.input_data.add_percentage(
                PercentageKeys.WATER,
                int(value))
        self.__check_info()

    def set_data_beach(self, instance, value):
        if value != "":
            self.input_data.add_percentage(
                PercentageKeys.BEACH,
                int(value))
        self.__check_info()

    def set_data_plain(self, instance, value):
        if value != "":
            self.input_data.add_percentage(
                PercentageKeys.PLAINS,
                int(value))
        self.__check_info()

    def set_data_mountain(self, instance, value):
        if value != "":
            self.input_data.add_percentage(
                PercentageKeys.MOUNTAIN,
                int(value))
        self.__check_info()

    def set_data_age(self, instance, value):
        if value != "":
            self.input_data.set_age(int(value))
        self.__check_info()

    #def test_on_down_touch(self):
    #    self.test_label.text = "AAAAAAA"
