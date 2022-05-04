
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)

# plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

IMGNAME = file_path

img = cv.imread(file_path,0)

print(img.shape)
f = np.fft.fft2(img) # Fourier Transform of Image 
fshift = np.fft.fftshift(f) # we shift the low frequencies to the middle
org_fshift = np.copy(fshift) # a copy to replot the image (we made pixeles in fshift =0) when we move the moving box
reset_fshift = np.copy(fshift) # a final copy for the reset button
magnitude_spectrum = 20*np.log(np.abs(fshift)) 


rows, cols = img.shape
print((rows, cols))
#middle of the image
crow = int(rows//2)  
ccol = int(cols//2)



# we show the ft in ax and inverse ft in ax2
fig, (ax,ax2) = plt.subplots(1, 2, sharey=True)

plt.subplots_adjust(left=0, bottom=0.5)
plt.subplot(121)
freq_img = ax.imshow(magnitude_spectrum, cmap = 'gray')
axcolor = 'yellow'
ax_slider1 = plt.axes([0.01, 0.05, 0.0225, 0.9], facecolor=axcolor)
slider1 = Slider(ax_slider1, 'Height->', 1, crow, valinit=50 ,orientation="vertical")

ax_slider2 = plt.axes([0.05, 0.01, 0.4, 0.03], facecolor=axcolor)
slider2 = Slider(ax_slider2, 'Width->', 1, ccol, valinit=50)


f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.real(img_back)



plt.subplot(122)
real_image =ax2.imshow(img_back, cmap = 'gray')

ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax2.axes.xaxis.set_visible(False)
ax2.axes.yaxis.set_visible(False)


def update(buttclick = "NOTHING"): #nothing is just a filler we need buttclick arguman for save and reset buttons
    
    slid1 = int(slider1.val) #getting the value form sliders
    slid2 = int(slider2.val)
    
    global org_fshift # making fshift global so we can change it from update()
    
    #bounderies of the white 0 box
    butt = crow-slid1 
    top  = crow+slid1
    left = ccol-slid2
    right = ccol+slid2
    
    print("original:  butt = {} , top = {} , left = {} , right = {}".format(butt, top , left , right))
    #making sure that the box doesnt go out of the image bouderies
    if butt < 0: butt = 0
    if top > rows: top = rows
    if left< 0: left = 0
    if right > cols: right = cols
    print("rectified:  butt = {} , top = {} , left = {} , right = {}".format(butt, top , left , right))
    
    
    
    # if we click reset button the value "RESET" will get return
    
    # rest should be before decrealing fshift and save should be after in order to upadte function work realtime
    if  buttclick == "RESET!":
        org_fshift = np.copy(reset_fshift)
        print("butt click value is {}".format(type(buttclick)))
    
    fshift = np.copy(org_fshift)
    fshift[butt:top,left:right] = 0
    print(fshift.shape)
    
    if  buttclick == "SAVE!": #SETs the image removal
        org_fshift = np.copy(fshift)
        print("butt click value is {}".format(type(buttclick)))
        
    
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    
    # clear is really nessary for updating without it it wont work
    ax.clear()
    ax.imshow(magnitude_spectrum, cmap = 'gray')
    
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)
    ax2.clear()
    ax2.imshow(img_back, cmap = 'gray')
    
    if  buttclick == "SAVEIMG!": #saves image as a file
        
        IMGBACKNAME = IMGNAME[:IMGNAME.index(".")]
        IMGFORMAT =IMGNAME[IMGNAME.index("."):]
        cv.imwrite(IMGBACKNAME +"_Edited" +'.jpg' , img_back)
    
    
    fig.canvas.draw_idle()
    
    
slider1.on_changed(update)
slider2.on_changed(update)



def onclick(event):
    global ccol 
    global crow
    
    #  ax == event.inaxes checks if subplot 1 is clicked becuase if we click on figure or right subplot we still get 
    #    correct format x and y
    if(ax == event.inaxes):
        if(type(event.xdata) != type(None) and type(event.ydata) != type(None) ):
            if (event.xdata > 0 and event.xdata < cols) and (event.ydata > 0 and event.ydata < rows):
                print("on click happend")
                ccol =int(event.xdata)
                crow = int(event.ydata)
                print(event.xdata, event.ydata)
    update()
    
fig.canvas.mpl_connect('button_press_event', onclick)

def button_save(val):
    update("SAVE!")
axsave = plt.axes([0.5, 0.01, 0.1, 0.075])
bsave = Button(axsave, 'Set Removal')
bsave.on_clicked(button_save)


def button_reset(val):
    update("RESET!")
axreset = plt.axes([0.6, 0.01, 0.1, 0.075])
breset = Button(axreset, 'Reset')
breset.on_clicked(button_reset)


def button_save_img(val):
    update("SAVEIMG!")
axsaveimg = plt.axes([0.7, 0.01, 0.1, 0.075])
bsaveimg = Button(axsaveimg, 'Save Image')
bsaveimg.on_clicked(button_save_img)



plt.show()

