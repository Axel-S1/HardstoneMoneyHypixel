import numpy as np
import cv2
import pyautogui
import time

class Simulation:
    def __init__(self):
        self.nb_iteration = 0
        self.nb_reset = 0
        self.buy_break = False
        self.sell_break = False
        self.not_find_until_break = 10
        
        self.region1 = (600, 200, 700, 500)
        self.region2 = (00, 500, 1000, 500)
        
        self.order_to_buy =     ['Hardstone1.png', 'Hardstone2.png', 'Create_buy_order.png', 'Custom_amount.png', 'Done.png', 'Top_order.png', 'Hardstone4.png']
        self.order_to_claim =   ['Manage_Order.png', 'Hardstone3.png', 'Go_back.png']
        self.order_to_sell =    ['Hardstone1.png', 'Sell_sacks.png', 'Validation.png', 'Go_back.png']
        self.order_to_cancel =  ['Manage_Order.png', 'Hardstone3.png', 'Cancel_validation.png', 'Go_back.png']
        
        self.debug = False
    
    def clickTo(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
    
    def reset_iteration(self):
        while True:
            find, loc = self.find_template(cv2.imread("Back_to_game.png",0), 0.90, self.region1, self.debug)
            if find:
                pyautogui.press('esc')
                self.send_command("pickupstash")
                self.send_command("bz")
                break
            else:
                pyautogui.press('esc')
                time.sleep(0.05)
    
    def send_command(self, cmd):
        pyautogui.typewrite('/')
        time.sleep(0.2)
        pyautogui.typewrite(cmd)
        pyautogui.press('enter')
    
    def find_template(self, template, threshold, region, debug):
        find = False
        w, h = template.shape[::-1]
        
        pyautogui.moveTo(960, 200)
        img = pyautogui.screenshot(region=region)
        img_rgb = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        if loc[0].size > 0:
            find = True
            loc = [loc[1][0] + w//2 , loc[0][0] + h//2]
            if debug:
                cv2.circle(img_rgb, loc, 5, (255,0,0), 2)
                cv2.imshow('Screenshot Finding', img_rgb)
                cv2.waitKey(0) 
                cv2.destroyAllWindows()
            loc = [loc[0] + region[0] , loc[1] + region[1]]   
        return find, loc
    
    def buy_order(self):
        for template in self.order_to_buy:
            cpt_not_find = 0   
            if self.buy_break == False:
                while True:
                    find, loc = self.find_template(cv2.imread(template,0), 0.99, self.region1, self.debug)
                    if find:
                        cpt_not_find = 0
                        if template == "Done.png":
                            pyautogui.typewrite("71680")
                        self.clickTo(loc[0], loc[1])
                        break
                    else:
                        cpt_not_find += 1
                        if cpt_not_find >= self.not_find_until_break:
                            self.buy_break = True
                            break
            else:
                break
            
        if self.buy_break == True:
            self.reset_iteration()
                    
    def wait_order(self):
        start_time = time.time()
        while True:
            find, _ = self.find_template(cv2.imread("Fill.png",0), 0.7, self.region2, self.debug)
            if find:
                self.send_command("pickupstash")
                self.send_command("bz")
                self.claim_order()
                break
                
            elif time.time() - start_time >= 40:
                self.send_command("pickupstash")
                self.send_command("bz")
                self.cancel_order()
                break
                
    def cancel_order(self):
        for template in self.order_to_cancel:
            cpt_not_find = 0   
            while True:
                find, loc = self.find_template(cv2.imread(template,0), 0.99, self.region1, self.debug)
                if find:
                    cpt_not_find = 0
                    self.clickTo(loc[0], loc[1])
                    if template != 'Hardstone3.png':
                        break
                else:
                    cpt_not_find += 1
                    if cpt_not_find >= self.not_find_until_break:
                        break
    
    def claim_order(self):
        for template in self.order_to_claim:
            cpt_not_find = 0   
            while True:
                find, loc = self.find_template(cv2.imread(template,0), 0.99, self.region1, self.debug)
                if find:
                    cpt_not_find = 0
                    self.clickTo(loc[0], loc[1])
                    if template != 'Hardstone3.png':
                        break
                else:
                    cpt_not_find += 1
                    if cpt_not_find >= self.not_find_until_break:
                        break
    
    def sell_order(self):
        for template in self.order_to_sell:
            cpt_not_find = 0   
            if self.buy_break == False:
                while True:
                    find, loc = self.find_template(cv2.imread(template,0), 0.99, self.region1, self.debug)
                    if find:
                        cpt_not_find = 0
                        self.clickTo(loc[0], loc[1])
                        break
                    else:
                        cpt_not_find += 1
                        if cpt_not_find >= self.not_find_until_break:
                            self.sell_break = True
                            break
            else:
                break
            
        if self.sell_break == True:
            self.reset_iteration()
    
    
    
simulation = Simulation()

time.sleep(10)
simulation.send_command('bz')


first_start_time = time.time()
for i in range(9999999):
    print(f"Itération n°{i} : elapsed time : {np.round(time.time()-first_start_time, 1)}s")
    
    if i%50 == 49:
        pyautogui.press('esc')
        time.sleep(0.5)
        simulation.send_command("is")
        time.sleep(7)
        
    simulation.buy_order()
    if simulation.buy_break == False:
        simulation.wait_order()
        simulation.sell_order()
    
    simulation.buy_break = False
    simulation.sell_break = False
print("END")