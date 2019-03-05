# -*- coding: utf-8 -*-
import uuid

from PIL import Image
import zipfile
import os


class ImageConverter:
    @staticmethod
    def convert_image_to_twitch_format(img_path):
        try:
            img = Image.open(img_path)
            if img.width != img.height:
                return False
            img_28x28 = img.resize(size=[28, 28]).save('28x28_{}'.format(img_path), 'png')
            img_56x56 = img.resize(size=[56, 56]).save('56x56_{}'.format(img_path), 'png')
            img_112x112 = img.resize(size=[112, 112]).save('112x112_{}'.format(img_path), 'png')

            archv_name = uuid.uuid1().hex
            img_archv = zipfile.ZipFile('{}.zip'.format(archv_name), 'w')
            img_archv.write('28x28_{}'.format(img_path))
            img_archv.write('56x56_{}'.format(img_path))
            img_archv.write('112x112_{}'.format(img_path))

            os.remove('28x28_{}'.format(img_path))
            os.remove('56x56_{}'.format(img_path))
            os.remove('112x112_{}'.format(img_path))
            os.rename('/home/tsr/{}.zip'.format(archv_name), '/home/tsr/zip_files/{}.zip'.format(archv_name))
            return '{}.zip'.format(archv_name)
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    ImageConverter().convert_image_to_twitch_format(img_path='')
