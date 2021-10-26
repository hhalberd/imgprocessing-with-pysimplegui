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
        sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Choose an image from list :"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(18, 10), key="ImgList"
            )
        ],
    ]
# Kolom Area No 2: Area viewer image input
image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

# Kolom Area No 3: Area Image info dan Tombol list of processing
list_processing = [
    [
        sg.Text("Image Information:"),
    ],
    [
        sg.Text(size=(20, 1), key="ImgSize"),
    ],
    [
        sg.Text(size=(20, 1), key="ImgColorDepth"),
    ],
    [
        sg.Text("List of Processing:"),
    ],
    [
        sg.Button("Image Negative", size=(25, 1), key="ImgNegative"),
    ],
    [
        sg.Button("Image Brightness (+80)", size=(25, 1), key="ImgBright"),
    ],
    [
        sg.Button("Image Threshold (+128)", size=(25, 1), key="ImgThresh"),
    ],
    [
        sg.Button("Image Rotate 45° C", size=(25, 1), key="ImgRotate45"),
    ],
    [
        sg.Button("Image Rotate 90° C", size=(25, 1), key="ImgRotate90"),
    ],
    [
        sg.Button("Image Rotate 90° CC", size=(25, 1), key="ImgRotate90CC"),
    ],
    [
        sg.Button("Image Rotate 180°", size=(25, 1), key="ImgRotate180"),
    ],
    [
        sg.Button("Image Flip Horizontal", size=(25, 1), key="ImgFlipH"),
    ],
    [
        sg.Button("Image Flip Vertical", size=(25, 1), key="ImgFlipV"),
    ],
    [
        sg.Button("Image Zooming (+50%)", size=(25, 1), key="ImgZoom"),
    ],
    [
        sg.Button("Image Shrinking (-50%)", size=(25, 1), key="ImgShrink"),
    ],
    [
        sg.Button("Image Translation (100,100)", size=(25, 1), key="ImgTrans"),
    ],
    [
        sg.Button("Image Translation (-100,-100)", size=(25, 1), key="ImgTrans2"),
    ],
]
# Kolom Area No 4: Area viewer image output
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
    [sg.Slider(range=(0, 200), default_value=default_nilai, orientation='h', size=(30, 10), change_submits=True, visible=False, key="nilai")] 
]

# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(list_processing),
        sg.VSeperator(),
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
    #nilai slider update
    sz = int(values['nilai'])
    if sz != default_nilai:
        default_nilai = sz
        window['nilai'].update(sz)
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
            window.Element('nilai').Update(visible=False)
            img_output=ImgNegative(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgBright":
        try:
            window["ImgProcessingType"].update("Image Brightness")
            window.Element('nilai').Update(visible=True,range=(-200,200))
            img_output=ImgBrightness(img_input,coldepth,80)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgThresh":
        try:
            window["ImgProcessingType"].update("Image Thresholding")
            window.Element('nilai').Update(visible=True,range=(0,256))
            img_output=ImgThreshold(img_input,coldepth,128)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgRotate45":
        try:
            window["ImgProcessingType"].update("Image Rotate 45° C")
            window.Element('nilai').Update(visible=False)
            img_output=ImgRotate(img_input,-45)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgRotate90":
        try:
            window["ImgProcessingType"].update("Image Rotate 90° C")
            window.Element('nilai').Update(visible=False)
            img_output=ImgRotate(img_input,-90)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgRotate90CC":
        try:
            window["ImgProcessingType"].update("Image Rotate 90° CC")
            window.Element('nilai').Update(visible=False)
            img_output=ImgRotate(img_input,90)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgRotate180":
        try:
            window["ImgProcessingType"].update("Image Rotate 180°")
            window.Element('nilai').Update(visible=False)
            img_output=ImgRotate(img_input,180)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgFlipH":
        try:
            window["ImgProcessingType"].update("Image Flip Horizontal")
            window.Element('nilai').Update(visible=False)
            img_output=ImgFlipHorizontal(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgFlipV":
        try:
            window["ImgProcessingType"].update("Image Flip Vertical")
            window.Element('nilai').Update(visible=False)
            img_output=ImgFlipVertical(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgTrans":
        try:
            window["ImgProcessingType"].update("Image Translation (100,100)")
            window.Element('nilai').Update(visible=False)
            img_output=ImgTranslation(img_input,coldepth,100,100)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgTrans2":
        try:
            window["ImgProcessingType"].update("Image Translation (-100,-100)")
            window.Element('nilai').Update(visible=False)
            img_output=ImgTranslation(img_input,coldepth,-100,-100)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgScale":
        try:
            window["ImgProcessingType"].update("Image Scale")
            window.Element('nilai').Update(visible=True,range=(0,180))
            img_output=ImgScale(img_input,coldepth,default_nilai)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgZoom":
        try:
            window["ImgProcessingType"].update("Image Zooming (+50%)")
            window.Element('nilai').Update(visible=False)
            img_output=ImgScale(img_input,coldepth,150)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgShrink":
        try:
            window["ImgProcessingType"].update("Image Shrinking (-50%)")
            window.Element('nilai').Update(visible=False)
            img_output=ImgScale(img_input,coldepth,50)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

window.close()
