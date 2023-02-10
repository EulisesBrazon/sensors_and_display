from ST7735 import TFT
from machine import SPI,Pin,ADC
#from sysfont import sysfont
import utime
import math

#difien values for displey use
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
tft=TFT(spi,0,7,1)
tft.initr()
tft.rgb(True)

#define value for use LM35
analog_value = ADC(26)
conversion_factor = 3.3/ 65535

#define pin for photoresist
photoResist = ADC(27)

#define pin for potenciometro
potenciometer_analog_value = ADC(28)

#define pin distance
trigger = Pin(15,Pin.OUT)
echo = Pin(14, Pin.IN)

def readTemperature():
    temp_voltage_raw = analog_value.read_u16()
    convert_voltage = temp_voltage_raw*conversion_factor
    tempC = convert_voltage/(10.0 / 1000)
    return tempC

def readLight():
    return photoResist.read_u16()

def readPotenciometer():
    return potenciometer_analog_value.read_u16()

def readDistance():
    trigger.high()
    utime.sleep_ms(10)
    trigger.low()
    
    while echo.value() == 0:
        star = utime.ticks_us()
    while echo.value() ==1:
        end = utime.ticks_us()
        
    duration = end - star
    distance = (duration * 0.0343) / 2
    return distance

def seeDate():
    
    size=2 #font size
    separation = 4 #separation between each line
    h=0 #height
    
    #data reading
    temperature = str(round(readTemperature(), 2))
    light = str(readLight())
    potentiometer = str(readPotenciometer())
    distance = str(readDistance())
    
    tft.fill(TFT.BLACK)#clean screen
    
    tft.text((0, h), "Temperatura:", TFT.RED, sysfont, size, nowrap=True)#printing on screen
    
    h += sysfont["Height"]*size+separation #recalculated height
    tft.text((0, h), temperature+"C", TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Nivel Luz:", TFT.RED, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), light, TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Potenciometo:", TFT.RED, sysfont, size-1, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), potentiometer, TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Distancia:", TFT.RED, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), distance, TFT.BLUE, sysfont, size, nowrap=True)

def main():
    while True :
        try:
            seeDate()
        except Exception as e:
            print("Error:", e)
        utime.sleep(1)
        
        
if __name__ == '__main__':
    #main()
    while True:
        print(readDistance())
        utime.sleep_ms(300)