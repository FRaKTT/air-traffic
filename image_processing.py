from PIL import Image
import os

def png2jpg(src, dst=None):
    """Convert png to jpg"""
    if not dst:
        wo_ext, ext = os.path.splitext(src)
        dst = f'{wo_ext}.jpg'
    im = Image.open(src)
    rgb_im = im.convert('RGB')
    rgb_im.save(dst)
    return dst
