import random
import requests
from PyQt5.QtGui import QPixmap


def img_save(sub_category):
    result = sub_category.iloc[random.sample(range(len(sub_category)), 2)]
    image1 = result.iloc[0].image_path
    image2 = result.iloc[1].image_path
    result1 = requests.get(image1)
    result2 = requests.get(image2)
    with open('./img/result1.jpg', 'wb') as f:
        f.write(result1.content)
    with open('./img/result2.jpg', 'wb') as f:
        f.write(result2.content)

