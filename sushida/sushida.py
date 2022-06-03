from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageOps
import pyocr
import pyocr.builders

# Chrome Driverのパス
driver_path = './chromedriver'
# ドライバーを開く
driver = webdriver.Chrome(driver_path)


# ウィンドウサイズを固定
# +123としているのは
# 「Chromeは自動テストソフトウェアによって制御されています。」
# という部分を考慮している
window = (750, 620+123)
driver.set_window_size(*window)

# OpenGL版の寿司打を開く
target_url = 'http://typingx0.net/sushida/play.html?soundless'
driver.get(target_url)

# クリックする前にロード時間待機
sleep(10)

print("______開始します_____")

# <body>に向かってキーを入力させる
target_xpath = '/html/body'
element = driver.find_element_by_xpath(target_xpath)
element.send_keys(" ")

# 画像の範囲を指定するためのリスト
im_ranges = [149, 298, 647, 717]

# PyOCRのツール
tool = pyocr.get_available_tools()[0]

from time import time
start = time()
while time() - start < 500.0:

    # 移動した
    # ファイル名
    fname = "sample_image.png"
    # スクショをする
    driver.save_screenshot(fname)

    # 画像をPILのImageを使って読み込む
    # ローマ字の部分を取り出す

    #"3000"円用
    im = Image.open(fname).crop((600,700,900,775))

    #"5000"円用
    #im = Image.open(fname).crop((570,700,960,775))

    #"10000"円用
    #im = Image.open(fname).crop((480,700,1080,775))

    for im_range in im_ranges:
        
         # 画像を二値化する
            im = im.convert("L")
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    if im.getpixel((i, j)) >= 128:
                        im.putpixel((i, j), 0)
                    else:
                        im.putpixel((i, j), 255)
            break

    im.save("sample.png")

    # tool で文字を認識させる
    text = tool.image_to_string(im, lang='eng', builder=pyocr.builders.TextBuilder())

    # text を確認
    print(text)

    # 文字を入力させる
    element.send_keys(text)


input("何か入力してください")

# ドライバーを閉じる
driver.close()
driver.quit()