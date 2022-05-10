import serial

from matplotlib import pyplot as plt
import numpy as np
import struct


#ValueError: invalid literal for int() with base 16: "'0F394'"


output_str = ""
counter = 0

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM8'
ser.timeout = 9.0
if(ser.is_open):
    ser.close()
    print("close Port")
else:
    ser.open()
    output = ser.readline(250000)
    #output_str = output.decode("utf-8")
    output_str = output_str.split(',')
    
    print(output_str[0])
    print(output_str[1])
    print(output_str[2])
with open('ByteStream.txt', 'wt') as f:
        for number in output_str:
            counter = counter +1
            f.write("'" + number +"'")
            f.write("aa")


print(f'Pixelarray contains {counter} Pixels') # 25344


    
# 25344 Pixel muessen uebertragen werden, wenn alles korrekt uebertragen wird , kann man zu Konstanten machen

if (counter < 25444): # 25344
    
    decArray = []
    rawText = ""            
    with open ("ByteStream.txt", 'r') as file:
        rawText = file.read()
    rawText = rawText.replace("'", "")
    rawText = rawText.replace("aa", ",")
    rawText = rawText.replace("0x", '')
    rawTextArray = rawText.split(',')
    for hexNumber in rawTextArray:
        #hexNumber = "'0"+ hexNumber +"'"
        if hexNumber=='':
            print("Pixel fehlerhaft")
            hexNumber = '0F394'
        decNumber = int(hexNumber, 16)
        decArray.append(decNumber)
    
    decArray = decArray[:-1]

    # Annahme: bei der Uebertragung kann es sein, dass einige Pixel nicht uebertragen werden -> diese werden am Ende mit dem Wert 0 aufgefuellt
    missingPixel = 25344 - len(decArray) 
    for i in range(missingPixel):
        decArray.append(0);
        
    print(f'Array successfully transformed and has size of = {(len(decArray))}')
    with open("Image.txt", "w") as file:
        file.write(rawText)
    
    HEXADECIMAL_BYTES = decArray
# Reformat the bytes into an image
    raw_bytes = np.array(HEXADECIMAL_BYTES, dtype="i2")
    image = np.zeros((len(raw_bytes),3), dtype=int)
    
    print(len(image))
    print(len(raw_bytes))
# Loop through all of the pixels and form the image
    for i in range(len(raw_bytes)):
        #Read 16-bit pixel
        pixel = struct.unpack('>h', raw_bytes[i])[0]

        #Convert RGB565 to RGB 24-bit
        r = ((pixel >> 11) & 0x1f) << 3;
        g = ((pixel >> 5) & 0x3f) << 2;
        b = ((pixel >> 0) & 0x1f) << 3;
        image[i] = [r,g,b]

    image = np.reshape(image,(144, 176,3)) #QCIF resolution

# Show the image
    plt.imshow(image)
    plt.show()
    
