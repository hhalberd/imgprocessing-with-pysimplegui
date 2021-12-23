import PySimpleGUI as sg
import os.path

from PIL import Image, ImageOps
from processing_list import *

sg.theme('Default1')

default_nilai = 100

# Kolom Area No 1: Area open folder and select image
file_list_column = [
    [
        sg.Text("Open Image Folder :"),
    ],
    [
        sg.In(size=(15, 1), enable_events=True, key="ImgFolder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Choose an image from list :"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(23, 4), key="ImgList"
            )
    ],
    [sg.Frame('Image Information:',[
    [
        sg.Text(size=(20, 1), key="ImgSize"),
    ],
    [
        sg.Text(size=(20, 1), key="ImgColorDepth"),
    ],
    ],)],
    [sg.Frame('Image Enhancements:',[
    [
        sg.Button("Image Thresholding", size=(20, 1), key="ImgThresh"),
    ],
    [
        sg.Button("Image Negative", size=(20, 1), key="ImgNegative"),
    ],
    [
        sg.Button("Image Brightness", size=(20, 1), key="ImgBright"),
    ],
    [
        sg.Button("Image Logarithmic", size=(20, 1), key="ImgLog"),
    ],
    [
        sg.Button("Image Dilasi", size=(20, 1), key="ImgDilation"),
    ],
    [
        sg.Button("Image Erosi", size=(20, 1), key="ImgErosion"),
    ],
    ],)],
    [sg.Frame('Image Conversions:',[
    [
        sg.Button("RGB to Grayscale", size=(20, 1), key="ImgGray"),
    ],
    [
        sg.Button("RGB to HSV", size=(20, 1), key="ImgHSV"),
    ],
    ],)],
    ]
# Kolom Area No 2: Area viewer image input
image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(20, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

# Kolom Area No 3: Area Image info dan Tombol list of processing
list_processing = [
    [sg.Frame('Image Transformations:',[
    [
        sg.Button("Rotate 45° Ke-kanan", size=(9, 2), key="ImgRotate45C"),
        sg.Button("Rotate 45° Ke-kiri", size=(9, 2), key="ImgRotate45CC"),
    ],
    [
        sg.Button("Rotate 90° Ke-kanan", size=(9, 2), key="ImgRotate90C"),
        sg.Button("Rotate 90° Ke-kiri", size=(9, 2), key="ImgRotate90CC"),
    ],
    [
        sg.Button("Flip    Horizontal", size=(9, 2), key="ImgFlipH"),        
        sg.Button("Flip       Vertical", size=(9, 2), key="ImgFlipV"),
    ],
    [
        sg.Button("Zooming (+50%)", size=(9, 2), key="ImgZoom"),
        sg.Button("Shrinking (-50%)", size=(9, 2), key="ImgShrink"),
    ],
    [
        sg.Button("Translation (100,100)", size=(9, 2), key="ImgTrans"),
        sg.Button("Translation (-100,-100)", size=(9, 2), key="ImgTrans2"),
    ], 
    ],)],
    [sg.Frame('Image Filterings:',[
    [
        sg.Button("Mean Filter", size=(20, 1), key="ImgMean"),
    ],
    [
        sg.Button("Median Filter", size=(20, 1), key="ImgMedian"),
    ],
    [
        sg.Button("Gaussian Filter", size=(20, 1), key="ImgGaussian"),
    ],
    ],)],
    [sg.Frame('Edge Detections:',[
    [
        sg.Button("Sobel", size=(20, 1), key="ImgSobel"),
    ],
    [
        sg.Button("Laplacian", size=(20, 1), key="ImgLaplace"),
    ],
    ],)],
]

# Kolom Area No 4: Area viewer image output
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(20, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(list_processing),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.Column(image_viewer_column2),
    ]
]
window = sg.Window("Mini Image Editor", layout)

#nama image file temporary setiap kali processing output
filename_out = "out.png"
# Run the Event Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]

        window["ImgList"].update(fnames)
    elif event == "ImgList": # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["ImgFolder"], values["ImgList"][0]
            )
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
            window["ImgProcessingType"].update(filename)
            window["ImgOutputViewer"].update(filename=filename)
            img_input = Image.open(filename)
            #img_input.show()

            #Size

            img_width, img_height = img_input.size
            window["ImgSize"].update("Image Size : "+str(img_width)+" x "+str(img_height))

            #Color depth
            mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB":24, "HSV": 24, "I": 32, "F": 32}
            coldepth = mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update("Color Depth : "+str(coldepth))
        except:
            pass
    
    elif event == "ImgNegative":

        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output=ImgNegative(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgBright":
        try:
            window["ImgProcessingType"].update("Image Brightness")
            img_output=ImgBrightness(img_input,coldepth,80)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgThresh":
        try:
            window["ImgProcessingType"].update("Image Thresholding")
            img_output=ImgThreshold(img_input,coldepth,128)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgRotate45C":
        try:
            window["ImgProcessingType"].update("Image Rotate 45° Kekanan")
            img_output=ImgRotate(img_input,45)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgRotate45CC":
        try:
            window["ImgProcessingType"].update("Image Rotate 45° Kekiri")
            img_output=ImgRotate(img_input,-45)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgRotate90CC":
        try:
            window["ImgProcessingType"].update("Image Rotate 90° Kekiri")
            img_output=ImgRotate(img_input,-90)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgRotate90C":
        try:
            window["ImgProcessingType"].update("Image Rotate 90° Kekanan")
            img_output=ImgRotate(img_input,90)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgRotate180":
        try:
            window["ImgProcessingType"].update("Image Rotate 180°")
            img_output=ImgRotate(img_input,180)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgFlipH":
        try:
            window["ImgProcessingType"].update("Image Flip Horizontal")
            img_output=ImgFlipHorizontal(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgFlipV":
        try:
            window["ImgProcessingType"].update("Image Flip Vertical")
            img_output=ImgFlipVertical(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgTrans":
        try:
            window["ImgProcessingType"].update("Image Translation (100,100)")
            img_output=ImgTranslation(img_input,coldepth,100,100)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgTrans2":
        try:
            window["ImgProcessingType"].update("Image Translation (-100,-100)")
            img_output=ImgTranslation(img_input,coldepth,-100,-100)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
        
    elif event == "ImgZoom":
        try:
            window["ImgProcessingType"].update("Image Zooming (+50%)")
            img_output=ImgScale(img_input,coldepth,150)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgShrink":
        try:
            window["ImgProcessingType"].update("Image Shrinking (-50%)")
            img_output=ImgScale(img_input,coldepth,50)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgLog":
        try:
            window["ImgProcessingType"].update("Image Logarithmic")
            img_output=ImgLogarithmic(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgMean":
        try:
            window["ImgProcessingType"].update("Image Mean Filtering")
            img_output=ImgMeanFilter(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgMedian":
        try:
            window["ImgProcessingType"].update("Image Median Filtering")
            img_output=ImgMedianFilter(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgGaussian":
        try:
            window["ImgProcessingType"].update("Image Gaussian Filtering")
            img_output=ImgGaussFilter(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgDilation":
        try:
            window["ImgProcessingType"].update("Image Dilasi")
            img_output=ImgDilation(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgErosion":
        try:
            window["ImgProcessingType"].update("Image Erosi")
            img_output=ImgErosion(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgEdge":
        try:
            window["ImgProcessingType"].update("Image Edge Detection")
            img_output=ImgEdge(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgGray":
        try:
            window["ImgProcessingType"].update("Image RGB to Grayscale")
            img_output=ImgGrayscale(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgHSV":
        try:
            window["ImgProcessingType"].update("Image RGB to HSV")
            img_output=ImgRGB_HSV(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgSobel":
        try:
            window["ImgProcessingType"].update("Sobel Edge Detection")
            img_output=ImgSobel(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgLaplace":
        try:
            window["ImgProcessingType"].update("Laplacian Edge Detection")
            img_output=ImgLaplacian(img_input)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
window.close()
