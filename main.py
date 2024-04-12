from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time
import random
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
hra = 0

oled.fill(0)  
oled.text("PicoBox v1.0", 5, 6)
oled.text("By Kuba", 30, 23)
oled.text("&", 55, 35)
oled.text("Stepan", 35, 47)
oled.rect(0, 0, 128, 20 , 1)
oled.show()
time.sleep(2)


# Game:  space ---------------------------------------------------------------------------------------

def game_space():
    

    tlacitko = Pin(7, Pin.IN, Pin.PULL_UP)
    tlacitko2 = Pin(15, Pin.IN, Pin.PULL_UP)
    tlacitko3 = Pin(3, Pin.IN, Pin.PULL_UP)
    tlacitko4 = Pin(4, Pin.IN, Pin.PULL_UP)
    buzzer = PWM(Pin(16))
    reset = 1

    while True:
        if reset == 1:
            x_star2 = 0
            x = 1
            x_star=1
            ran = 2
            ran2 = 0
            x_pos = 0
            tilt = 0
            score = 1
            shield = 100
            shot = 0
            ran3 = 0
            ran4 = 0
            ran5 = 0
            s = 1
            block = 1
            block2 = 0
            oprava = 1
            r = 0
            dest = 0
            boom = 0
            hit = 0
            flash_shield = 0
            flash_count = 0
            flash_spaceship = 1
            reset = 0
            sound=0
            
        
        
        if flash_count >= 1:
            flash_count = flash_count+1
            flash_spaceship = flash_spaceship+1 

        if flash_spaceship == 2:
            flash_spaceship = 0

        if flash_count >= 5:
            flash_count = 0
    
        oled.fill(0) 
        tilt = 0
        
        if not tlacitko4.value():  
           return
        
        # move spaceship

        if not tlacitko.value():  
            x_pos = x_pos + 4
            tilt = 4 
  
        if not tlacitko2.value():  
            x_pos = x_pos - 4
            tilt = -4
        
        # shot from your spaceship
            
        if not tlacitko3.value():  
            shot = 1
            block = block + 1
               
            
        if shot == 1 and block == 0:
            shot = 0
            oled.line(60 + x_pos, 45 , 60 + x_pos + tilt, 15, 1)
            sound=1
             
        if block >= 1:
            block=0   
            
       
        
        # flash shield
        
        flash_shield = flash_shield + 1 

        if flash_shield == 2:
            flash_shield = 0   
        
        # star cluster
        
        oled.rect(62 - x_star , 25 - x_star , 1, 1, 1)
        oled.rect(68 + x_star, 30+x_star, 1, 1, 1)
        oled.rect(70 + x_star2, 28 - x_star2, 1, 1, 1)
        oled.rect(60 - x_star2 , 32 + x_star2 , 1, 1, 1)
        oled.rect(85 + x_star2 + ran, 13 - x_star2 , ran, ran, 1)
        oled.rect(45 - x_star2 , 47 + x_star2 , 1, 1, 1)
        oled.rect(62 - x_star , 25 ,1, 1, 1)
        oled.rect(68 + x_star, 22, 1, 1, 1)
        oled.rect(32 - x_star, 25 , 1, 1, 1)
        oled.rect(98 + x_star, 22, ran, ran, 1)
        
        x_star=x_star+r
        x_star2=x_star2+r
        
        if x_star2 >= 15:
            x_star2=0
        if x_star >= 30:
            x_star=0
            ran = random.randint(1, 2)
        
        # alien
            
        if x >= 15 and oprava < 5:
            
            oled.rect( 58 + ran2, 3 + x + dest, 4, 4, 1)
            oled.rect( 55 + ran2 - dest, 2 + x + dest, 1, 7, 1)
            oled.rect( 64 + ran2 + dest, 2 + x + dest, 1, 7, 1)
            oled.rect( 56 + ran2 , 5 + x + dest * 2, 9, 1, 1)
        else:
            oled.rect( 58 + ran2 , 3 + x, 4, 2, 1)
           
        if x >= 15 and oprava == 5:
            oled.rect( 58 + ran2 , 3 + x, 6, 6, flash_shield)
            oled.rect( 60 + ran2, 5 + x, 2, 2, flash_shield)
    
        # informations
         
        oled.text("score:" + str(score), 65 , 57)
        oled.rect( 0, 58, 6, 6, 1)
        oled.rect( 2, 60, 2, 2, 1)
        oled.text(str(shield) + "%", 10, 57)
        
        # alien move
        
        x = x + r
        r = round(s)
            
        # alien random shot
         
        if x == 16 and ran4 == 1 and oprava < 5 and boom==0:
            
            
            oled.line(58 + ran3, 55 , 62 + ran2, 5 + x , 1)

            sound = 1
            
        # alien hit your spaceship
        
        if x_pos < ran3 + 8 and x_pos > ran3-8 and  x == 16 and ran4 == 1 and boom==0:
         
            flash_count = 1
            shield = shield - 10
        
        # game over
        
        if  shield < 1:
            oled.text("GAME OVER", 25, 26)
            reset = 1        
            oled.show()
            time.sleep(2)
        
        # shield catch
    
        if x_pos < ran2 + 8 and x_pos > ran2-8 and x >= 36 and oprava == 5:
            
            shield = shield + 10
            sound = 1
            boom = 0
        
        # your bad hit to alien
        
        if x >= 36:
            if hit == 0 and oprava < 5:
                oled.line(60 + x_pos, 55 , 65 + ran2, 5 + x , 1)
                # oled.rect( 33 + x_pos , 50, 55, 5, 1)
                flash_count = 1
                shield = shield - 10
                sound = 1
            dest = 0
            x = 0
            
            ran2 = random.randint(-10, 10)
            ran3 = random.randint(-10, 10)
            ran4 = random.randint(1, 2)
            oprava = random.randint(1, 5)
            ran2 = ran2 * 4
            ran3 = ran3 * 4
            s=s+0.05
            boom = 0
            hit = 0
            block2 = 0
        
        # successful hit to alien 
        
        if x_pos < ran2 + 8 and x_pos > ran2-8 and x >= 14 and shot == 1 and oprava < 5 and block2 == 0:
           
            boom = 1
            block2=1
            hit = 1
            score = score + 1
            sound=1
            
        if boom == 1:
            dest = dest - 4
        
        # beep
        
        if sound==1:
            sound=0
            buzzer.freq(50)
            buzzer.duty_u16(32768)
            time.sleep(0.05)
            buzzer.duty_u16(0)
            buzzer.deinit()
    

        # your spaceship

        oled.line(60 + x_pos, 47 , 70 + x_pos, 55 + tilt, flash_spaceship)
        oled.line(60 + x_pos, 47, 50 + x_pos, 55 - tilt , flash_spaceship)
        oled.line(60 + x_pos, 52 , 70 + x_pos, 55 + tilt, flash_spaceship)
        oled.line(60 + x_pos, 52, 50 + x_pos, 55 - tilt , flash_spaceship)

        
        
        time.sleep(0.1)
        
        oled.show()
        
# Game:  Pong ---------------------------------------------------------------------------------------


def game_pong():

    x_pos = 2
    direction = 0
    ran = 1
    direction2 = 1
    direction3 = 1
    x_pos2 = 2
    y_pos2 = 2
    score = 0
    tlacitko = Pin(7, Pin.IN, Pin.PULL_UP)
    tlacitko2 = Pin(15, Pin.IN, Pin.PULL_UP)
    tlacitko3 = Pin(4, Pin.IN, Pin.PULL_UP)
    buzzer = PWM(Pin(16))
    shift = 0
    sound = 0

    while True:


        if not tlacitko3.value():  
            return

        if not tlacitko.value():  
            x_pos = x_pos + 2  
  
        if not tlacitko2.value():  
            x_pos = x_pos - 2 

        
        oled.fill(0)  
        oled.text("Score " + str(score), 0, 0)
   

        # bat
        oled.rect(x_pos, 58, 10, 2, 1)

        # ball
        oled.rect(x_pos2 + 5 , 56 - y_pos2, 2, 2, 1)
   

        if shift == 0:
            x_pos2 = x_pos2 + ran 
            y_pos2 = y_pos2 + direction3

    
        if x_pos2 <= 0 or x_pos2 >= 116:  
            direction2 = -direction2
            ran = -ran
            sound = 1
       
        if x_pos <= x_pos2 + 8 and x_pos >= x_pos2 - 8 and y_pos2 == 0:   
            shift = 0
            ran = random.randint(1, 3)
            score = score + 1
            sound = 1

        elif y_pos2 == 0 :       
            oled.text("GAME OVER", 25, 26)
            oled.show()
            time.sleep(2) 
            x_pos = 2
            direction = 0
            ran = 1
            direction2 = 1
            direction3 = 1
            x_pos2 = 2
            y_pos2 = 2
            score = 0
   
    
        if y_pos2 <= 0 or y_pos2 >= 54:  
            direction3 = -direction3
            sound = 1
        

        oled.show()


        if sound == 1:
            buzzer.freq(200)
            buzzer.duty_u16(32768)
            time.sleep(0.02)
            buzzer.duty_u16(0)
            sound = 0
            buzzer.deinit()
        else:
            time.sleep(0.02)



# Game: Lunar module ---------------------------------------------------------------------------------------

def game_modul():

    
    level = 1
    x_pos = 2
    direction = 0
    ran = 1
    direction2 = 1
    direction3 = 1
    x_pos2 = 2
    y_pos2 = 2
    gravity= 1
    fuel = 25
    fire = 0
    
    tlacitko2 = Pin(20, Pin.IN, Pin.PULL_UP)
    tlacitko3 = Pin(4, Pin.IN, Pin.PULL_UP)
    shift = 0

    while True:


        if not tlacitko3.value():  
           return
    
        if not tlacitko2.value():
            fire = 1
            gravity = gravity - 5
            fuel = fuel - 1 

  
        oled.fill(0)  
        oled.text("Fuel " + str(fuel), 0, 55)
        oled.text("m/s " + str(gravity), 80, 1)
    
   
        # Lunar modul
        
        oled.rect(6 + x_pos2, 3 + y_pos2, 5, 5, 1)
        oled.vline(5 + x_pos2, 5 + y_pos2, 5, 1)
        oled.vline(11 + x_pos2, 5 + y_pos2, 5, 1)
        oled.rect(7 + x_pos2, 1 + y_pos2, 3, 4 , 1)

        # landing area
        oled.rect(100, 62, 14, 2, 1)
        
        if fire == 1:
            oled.vline(8 + x_pos2, 11 + y_pos2, 8, 1)
            fire = 0

        x_pos2 = x_pos2 + ran 
        y_pos2 = y_pos2 + direction3
        y_pos2 = y_pos2 +  1 + gravity // 10
        gravity = gravity + 1
       
        if x_pos2 > 90 and x_pos2 < 110 and y_pos2 >=  56 and gravity < 4:
            oled.text("Landing OK!", 25, 20)
            level = level + 1
            oled.text("Level " + str(level), 25, 30)
            oled.show()
            time.sleep(2) 
            x_pos = 2
            direction = 0
            gravity = 1
            ran = ran + 1
            direction2 = 1
            direction3 = 1
            x_pos2 = 2
            y_pos2 = 2
            fuel = 25

        elif y_pos2 >=  56 or fuel < 1:       
            oled.text("GAME OVER", 25, 26)
            oled.show()
            time.sleep(2) 
            x_pos = 2
            direction = 0
            gravity = 1
            ran = 1
            direction2 = 1
            direction3 = 1
            x_pos2 = 2
            y_pos2 = 2
            fuel = 25
            level = 1
   

        oled.show()

        time.sleep(0.1)


# Game: Full speed ---------------------------------------------------------------------------------------

def game_moto():
    x = 1
    y = 1
    prekazka = 1
    ran = 0
    direction3 = 1
    x_pos = 2
    tilt = 0
    score = 1
    speed= 1
    acceleration = 1
    level = 1
    y_rival = 0
    crasch = 0

    tlacitko = Pin(7, Pin.IN, Pin.PULL_UP)
    tlacitko2 = Pin(15, Pin.IN, Pin.PULL_UP)
    tlacitko3 = Pin(4, Pin.IN, Pin.PULL_UP)



    while True:
    
        oled.fill(0) 
        tilt = 0
        if not tlacitko3.value():  
           return

        if not tlacitko.value():  
            x_pos = x_pos + 2
            tilt = 4 
  
        if not tlacitko2.value():  
            x_pos = x_pos - 2
            tilt = -4
    
        y_rival = ran + y
        oled.text("Score:" + str(score), 0, 0)
        oled.text(str(score * 5) + " km/h", 70, 0)
    
        x = x + 1
        y = y + direction3
        prekazka = prekazka + speed

    
        # horizont
        oled.line(20 + y // 5, 35 + y // 10 , 9 + y // 4 , 39 + y // 10, 1)
        oled.line(20 + y // 5, 35 + y // 10, 29 + y // 4, 39 + y // 10, 1)
        
        # road
    
    
        oled.rect(0, 40 + y //10, 128, 2, 1)

        oled.line(50 + y, 40 + y // 10, 30 , 50, 1)
        oled.line(70 + y , 40 + y // 10, 90, 50, 1)
    
        oled.line(30, 50, 10, 63, 1)
        oled.line(90, 50, 118, 63, 1)
    
        oled.rect(0, 42 + x//2, 128, 4, 0)
    
        oled.rect(0, 52 + x, 128, 8, 0)
    
        # your moto
        oled.rect(60 + x_pos, 58, 2, 4, 1)
        oled.rect(59  + x_pos + tilt // 2, 55, 5, 4, 1)

        oled.rect(60 + x_pos + tilt, 52, 2, 2, 1)

        # rival
        if prekazka > 10: 
            oled.rect(60 + ran + y, 38 + prekazka , 2, 4, 1)
            oled.rect(59 + y // 20  + ran + y, 35 + prekazka, 5, 4, 1)

            oled.rect(60 + y // 10  + ran + y, 32 + prekazka, 2, 2, 1)
        
        if prekazka <= 10: 
            oled.rect(60 + ran + y, 38 + prekazka , 2, 4, 1)
    
        oled.show()
    
        if x== 4:  
            x = 0

        if prekazka >= 30:  
            ran = random.randint(-5, 5)
            ran = ran * 2
            prekazka = 0
            score = score + 1
            acceleration = acceleration + 0.05
            speed = round(acceleration)
    

        if y <= -35  or y >= 25:  
            direction3 = -direction3

        if y <= -15:  
            x_pos = x_pos + 2
        
        if y > 15 :  
            x_pos = x_pos - 2
            
        if x_pos >=  46 or x_pos < -46:       
            crasch = 1

        if x_pos <= y_rival + 4  and x_pos >= y_rival - 4 and prekazka >= 15:       
            crasch = 1


        if  crasch ==  1:  
            oled.text("GAME OVER", 25, 26)
            oled.show()
            time.sleep(2)
            x = 1
            y = 1
            prekazka = 1
            ran = 0
            direction3 = 1
            x_pos = 2
            tilt = 0
            score = 1
            speed= 1
            acceleration = 1
            level = 1
            y_rival = 0
            crasch = 0

        time.sleep(0.1)  


def main_menu():
    
    while True:
        
        oled.fill(0)  
        oled.text("King of Space", 18, 25)
        oled.show()
        time.sleep(2)
        game_space() 
       
        oled.fill(0)  
        oled.text("   Pong  ", 18, 25)
        oled.show()
        time.sleep(2)
        game_pong() 

        oled.fill(0)  
        oled.text("Lunar Module", 18, 25)
        oled.show()
        time.sleep(2)
        game_modul()         

        oled.fill(0)  
        oled.text(" Full Speed", 18, 25)
        oled.show()
        time.sleep(2)
        game_moto()
     
        

main_menu()


