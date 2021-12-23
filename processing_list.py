from math import sin, cos, floor
from PIL import Image, ImageFilter
import colorsys
import cv2
import numpy as np
from scipy import ndimage

def ImgNegative(img_input,coldepth):
    #solusi 1
    #img_output=ImageOps.invert(img_input)

    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (255-r, 255-g, 255-b)
        
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgBrightness(img_input,coldepth,nilai_pencerahan):
    
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (nilai_pencerahan+r, nilai_pencerahan+g, nilai_pencerahan+b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgThreshold(img_input,coldepth,n):
    
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    img_output = img_input.convert('L')
    pixels = img_output.load()
    ukuran_horizontal = img_output.size[0]
    ukuran_vertikal = img_output.size[1]

    for x in range(ukuran_horizontal):
        for y in range(ukuran_vertikal):
            if pixels[x, y] < n:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def ImgRotate(img_input,derajat):

    CITRA = img_input
    PIXEL = CITRA.load()

    ukuran_horizontal = CITRA.size[0]
    ukuran_vertikal = CITRA.size[1]

    img_output = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    PIXEL_BARU = img_output.load()

    x_tengah = ukuran_horizontal // 2
    y_tengah = ukuran_vertikal // 2

    for x in range(ukuran_horizontal):
        for y in range(ukuran_vertikal):

            theta = derajat * 22/7 / 180

            x_baru = (cos(theta) * (x - x_tengah) - sin(theta)
                      * (y - y_tengah) + x_tengah)
            y_baru = (sin(theta) * (x - x_tengah) + cos(theta)
                      * (y - y_tengah) + y_tengah)

            if (x_baru >= ukuran_horizontal or y_baru >= ukuran_vertikal
                    or x_baru < 0 or y_baru < 0):
                PIXEL_BARU[x, y] = (0, 0, 0)
            else:
                PIXEL_BARU[x, y] = PIXEL[x_baru, y_baru]
    
    return img_output
    
def ImgFlipHorizontal(img_input,coldepth):

    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((img_input.size[1]-1-i,j))
            pixels[i,j] = (r, g, b)
    
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def ImgFlipVertical(img_input,coldepth):

    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i,img_input.size[0]-1-j))
            pixels[i,j] = (r, g, b)
    
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def ImgTranslation(img_input,coldepth,m,n):

    citra = img_input
    pixel = citra.load()

    ukuran_horizontal = citra.size[0]
    ukuran_vertikal = citra.size[1]

    img_output = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    new_pixel = img_output.load()

    start_m = m
    start_n = n

    if m < 0:
        start_m = 0
    if n < 0:
        start_n = 0

    for x in range(start_m, ukuran_horizontal):
        for y in range(start_n, ukuran_vertikal):
            x_baru = x - m
            y_baru = y - n
       
            if (x_baru >= ukuran_horizontal or y_baru >= ukuran_vertikal or x_baru < 0 or y_baru < 0):
                new_pixel[x, y] = (0, 0, 0)
            else:
                new_pixel[x, y]=pixel[x_baru, y_baru]

    return img_output

def ImgScale(img_input,coldepth,s):
    
    s2 = s / 100  
    
    citra = img_input
    pixel = citra.load()

    ukuran_horizontal = citra.size[0]
    ukuran_vertikal = citra.size[1]

    ukuran_horizontal_baru = floor(ukuran_horizontal * s2)
    ukuran_vertikal_baru = floor(ukuran_vertikal * s2)
    
    img_output = Image.new("RGB", (ukuran_horizontal_baru, ukuran_vertikal_baru))
    new_pixel = img_output.load()

    for x in range(ukuran_horizontal_baru):
        for y in range(ukuran_vertikal_baru):
            x_lama = ukuran_horizontal * x / ukuran_horizontal_baru
            y_lama = ukuran_vertikal * y / ukuran_vertikal_baru
            new_pixel[x, y] = pixel[x_lama, y_lama]
            
    return img_output

def ImgMeanFilter(img_input):
    pil_image = img_input.convert('RGB')
    img_output = np.array(pil_image) 
    img_output = cv2.cvtColor(img_output, cv2.COLOR_RGB2BGR)
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img_output,-1,kernel)
    color_coverted = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    img_output=Image.fromarray(color_coverted)
    return img_output

def ImgMedianFilter(img_input):
    
    im=img_input
    img_output=im.filter(ImageFilter.MedianFilter(size = 5)) 
    return img_output

def ImgGaussFilter(img_input):
    
    im=img_input
    img_output=im.filter(ImageFilter.GaussianBlur(radius = 3)) 
    return img_output

def ImgEdge(img_input):
    
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    Ix = ndimage.filters.convolve(img_input, Kx)
    Iy = ndimage.filters.convolve(img_input, Ky)
    
    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    img_output = (G, theta)
    
    return img_output

def ImgDilation(img_input):
    
    im=img_input
    img_output=im.filter(ImageFilter.MaxFilter(3))
    return img_output

def ImgErosion(img_input):
    
    im=img_input
    img_output=im.filter(ImageFilter.MinFilter(3))
    return img_output

def ImgGrayscale(img_input,coldepth):
    
    #solusi 1
    #img_output = img_input.convert('L')
    
    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            gray = int(round(0.299 * r + 0.587 * g + 0.114 * b))
            pixels[i,j] = (gray, gray, gray)
            
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def ImgRGB_HSV(img_input):
    
    if isinstance(img_input,Image.Image):
        r,g,b = img_input.split()
        Hdat = []
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None
    
def ImgLogarithmic(img_input):
    pil_image = img_input.convert('RGB')
    open_image = np.array(pil_image)
    open_image = open_image[:, :, ::-1].copy()
    img_log = (np.log(open_image+1)/(np.log(1+np.max(open_image))))*255
    img_log = np.array(img_log,dtype=np.uint8)
    img_log = cv2.cvtColor(img_log, cv2.COLOR_BGR2RGB)
    img_output = Image.fromarray(img_log)
    return img_output

def ImgSobel(img_input):
    pil_image = img_input.convert('RGB') 
    img_output = np.array(pil_image) 
    img = cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY)
    rows, cols = img.shape
    img_output = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    arr = np.uint8(img_output)
    h, w = arr.shape
    img_output=Image.fromarray(arr)
    return img_output

def ImgLaplacian(img_input):
    pil_image = img_input.convert('RGB') 
    img_output = np.array(pil_image) 
    img_output = cv2.cvtColor(img_output, cv2.COLOR_RGB2BGR)
    img_output = cv2.cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY)

    img_output = cv2.GaussianBlur(img_output,(3,3),0)
    laplacian = cv2.Laplacian(img_output,cv2.CV_64F)
    arr = np.uint8(laplacian)
    h, w = arr.shape
    img_output=Image.fromarray(arr)
    return img_output
