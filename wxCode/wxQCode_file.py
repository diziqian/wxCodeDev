# coding:utf-8

import os
import qrcode
from wxQCode_const import URL_DES, TMP_PATH


def get_qcode(open_id):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )

    url = '{0}?openid={1}'.format(URL_DES, open_id)
    qr.add_data(url)
    path = '{0}_{1}.png'.format(TMP_PATH, open_id)
    os.remove(path)

    img = qr.make_image()
    img.save(path)

    # 一直等到文件存在
    while not os.path.exists(path):
        continue

    return path


def get_media_id(client, path):
    with open(path, "rb") as file:
        msg = client.material.add(media_type="image", media_file=file)
        media_id = msg["media_id"]
        return media_id
