#import System.Drawing
from PIL import Image
from generators import caracters
from Statistics.input_data import PercentageKeys as enumKeys
from Statistics.input_data import keys_percentages as caracters
from io import BytesIO
from kivy.core.image import Image as CoreImage

def generate_image(file_content):
    img = Image.new('RGB', (500, 500), 'black')
    pixels_list = img.load()

    for j in range(img.size[1]):
        for i in range(img.size[0]):
            #print(i, j)
            pixels_list[i, j] =table_caracters[file_content[j][i]] #(255,255,255)#table_tuple[table_caracters[file_content[j][i]]]  # (0,0,0) # RGB

    data = BytesIO()

    img.save(data, format='png')
    data.seek(0)
    core_img = CoreImage(BytesIO(data.read()), ext='png')
    return core_img

def basic_image():
    img = Image.new('RGB', (500, 500), 'white')
    pixels_list = img.load()

    for j in range(img.size[1]):
        for i in range(img.size[0]):
            # print(i, j)
            pixels_list[i, j] = (0, 0, 0)

    data = BytesIO()

    img.save(data, format='png')
    data.seek(0)
    core_img = CoreImage(BytesIO(data.read()), ext='png')
    return core_img

def get_tuple_water():
    return (121, 197, 255)


def get_tuple_beach():
    return (245, 221, 156)


def get_tuple_plain():
    return (62, 185, 25)


def get_tuple_mountain():
    return (150, 150, 150)


table_caracters = {
    "˵": (121, 197, 255),
    "ᴖ": (245, 221, 156),
    "∩": (62, 185, 25),
    "▲": (150, 150, 150)
}


table_tuple = {
    enumKeys.WATER: get_tuple_water(),
    enumKeys.BEACH: get_tuple_beach(),
    enumKeys.PLAINS: get_tuple_plain(),
    enumKeys.MOUNTAIN: get_tuple_mountain()
}