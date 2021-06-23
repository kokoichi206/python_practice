import glob
from PIL import Image

files = glob.glob("/home/TT/master/diary/scraping/minami_hoshino/*.jpeg")
files = files[0:40]
images = list(map(lambda file : Image.open(file) , files))
images[0].save('image.gif' , save_all = True , append_images = images[1:] , duration = 150 , loop = 0)
# Image.save('out.gif', save_all=True, append_images=images)
