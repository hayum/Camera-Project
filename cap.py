import subprocess
import RPi.GPIO as GPIO
import time
from PIL import Image 
import numpy 
from blend_modes import blend_modes

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

size=640,320
i=0

try:
    while True:
        input_state=GPIO.input(23)
        print(input_state)
        if input_state==0:
            GPIO.output(24,GPIO.HIGH)
            subprocess.call("fswebcam -d/dev/video0 -r 1024*768 -S0 /home/pi/img/" + str(i) +"pic.jpg", shell = True)
            print('PIC CAPTURED')
            GPIO.output(24,GPIO.LOW)
            GPIO.output(25,GPIO.HIGH)
            background_img_raw = Image.open("/home/pi/img/" + str(i) +"pic.jpg").convert('LA')  # RGBA image
            rgbimg = Image.new("RGBA", background_img_raw.size) 
            rgbimg.paste(background_img_raw) 
            background_img = numpy.array(rgbimg)  # Inputs to blend_modes need to be numpy arrays. 
            background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats. 

            foreground_img_raw = Image.open('/home/pi/img/1.png')  # RGBA image
            foreground_img = numpy.array(foreground_img_raw)  # Inputs to blend_modes need to be numpy arrays.
            foreground_img_float = foreground_img.astype(float)  # Inputs to blend_modes need to be floats.

            # Blend images
            opacity = 0.7  # The opacity of the foreground that is blended onto the background is 70 %.
            blended_img_float = blend_modes.multiply(background_img_float, foreground_img_float, opacity)

            # Convert blended image back into PIL image
            blended_img = numpy.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
            blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
            
            # Display blended image
            # blended_img_raw.show()
            blended_img_raw.thumbnail(size,Image.ANTIALIAS)
            blended_img_raw.save("/home/pi/img/" + str(i) +"newpic.jpg")
            i=i+1;
            GPIO.output(25,GPIO.LOW)
            time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()

