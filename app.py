import json
import os
import time
import requests
import base64
from random import randrange
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')


class Text2ImageAPI:

    def __init__(self, url: str, api_key: str, secret_key: str):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "style": "UHD",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        # pprint(data)
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def save_base64_image(base64_string, filename):
    with open(filename, "wb") as f:
        f.write(base64.b64decode(base64_string))


def random_filename(prefix: str = 'generated_image') -> str:
    """
        Make random name for image.

    """

    random_num = lambda: randrange(1, 200) * 112
    image_name = f'{prefix}{random_num()}{random_num()}{random_num()}.jpg'

    return image_name


def create_filename(folder: str, filename: str) -> str:
    """
        Build a full path to generated image. Create a new directory if it doesn't exist and generate random
        prefix-based filename for an image.

    """

    image_name = random_filename(prefix=filename)

    if folder:
        if not os.path.exists(folder):
            os.mkdir(folder)

        image_name = os.path.join(folder, image_name)

    return image_name


def generate_image(prompt: str, filename: str = 'filename', image_num: int = 1, folder: str = None) -> None:
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', api_key=API_KEY, secret_key=SECRET_KEY)

    for i in range(image_num):
        filename_handled = create_filename(folder, filename)
        print(f"{i + 1}: {filename_handled}")

        model_id = api.get_model()
        uuid = api.generate(prompt=prompt, model=model_id)
        images = api.check_generation(uuid)

        save_base64_image(base64_string=images[0], filename=filename_handled)


if __name__ == '__main__':
    prompt_1 = (
        "Городской пейзаж с небоскребами и девушкой в зеленом платье и зеленой губной помадой на губах,"
        "которая стоит близко в пол оборота к камере. Девушка смеется и держит в руках букет из ярко желтых цветов."
        "Очень реалистичное лицо."
    )

    prompt_2 = (
        "Корова в стиле цветочного сюрреализма на лугу,  вдохновленный природой камуфляж, "
        "цветочный панк, нежные материалы, яркая, студийная фотография. Стиль: Детальное фото."
    )

    prompt_3 = (
        "Цитадель с облачным небом, причудливые цветочные сцены, светло-серебристый и светло-красный,"
        "минималистский иллюстратор, линейная элегантность."
    )

    prompt_4 = (
        "Кот в кожанной куртке и темных очках играет на электрогитаре на сцене. Вокруг видны молнии и черепа в огне."
    )

    # Just run it
    FILENAME = 'heavy_metal_cat_2'
    generate_image(prompt=prompt_4, filename=FILENAME, image_num=20, folder=FILENAME)

