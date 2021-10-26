from PIL import Image
from math import sin, cos, floor

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

    CITRA = img_input
    PIXEL = CITRA.load()

    ukuran_horizontal = CITRA.size[0]
    ukuran_vertikal = CITRA.size[1]

    img_output = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    PIXEL_BARU = img_output.load()

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
                PIXEL_BARU[x, y] = (0, 0, 0)
            else:
                PIXEL_BARU[x, y]= PIXEL[x_baru, y_baru]

    return img_output

def ImgScale(img_input,coldepth,s):
    
    s2 = s / 100  
    
    CITRA = img_input
    PIXEL = CITRA.load()

    ukuran_horizontal = CITRA.size[0]
    ukuran_vertikal = CITRA.size[1]

    ukuran_horizontal_baru = floor(ukuran_horizontal * s2)
    ukuran_vertikal_baru = floor(ukuran_vertikal * s2)
    
    img_output = Image.new("RGB", (ukuran_horizontal_baru, ukuran_vertikal_baru))
    PIXEL_BARU = img_output.load()

    for x in range(ukuran_horizontal_baru):
        for y in range(ukuran_vertikal_baru):
            x_lama = ukuran_horizontal * x / ukuran_horizontal_baru
            y_lama = ukuran_vertikal * y / ukuran_vertikal_baru
            PIXEL_BARU[x, y] = PIXEL[x_lama, y_lama]

    return img_output