import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

theta = np.linspace(0, 2*np.pi, 201)
delta_theta = np.linspace(0, 2*np.pi, 201)
b = 1.0
muki = True

ims=[]
for i in delta_theta:
    x = np.cos(theta)
    y1 = np.sin(theta + i)
    y2 = np.sin(b*theta)
    y3 = np.sin(2*theta + i)

    # 描画
    fig = plt.figure(figsize=(3,3))
    plt.plot(x, y1, 'b', x, y2, 'g', x, y3, 'r')
    fig.canvas.draw()

    # Imageオブジェクトへ変換
    image_array = np.array(fig.canvas.renderer.buffer_rgba())
    # image_array = np.array(fig.canvas.renderer._renderer) # matplotlibが3.1より前の場合
    im = Image.fromarray(image_array)
    ims.append(im)
    plt.close()

    if muki is True:
        b = b + 0.05
        if b > 6:
            muki = False
    else:
        b = b - 0.05

# 出力
ims[0].save('out.gif', save_all=True, append_images=ims[1:], loop=0, duration=30)
