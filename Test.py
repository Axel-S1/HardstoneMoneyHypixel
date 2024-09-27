import numpy as np
import cv2
import pyautogui
import time

region1 = (600, 200, 700, 500)
def find_template(template, threshold, debug):
        find = False
        w, h = template.shape[::-1]
        
        pyautogui.moveTo(960, 200)
        img = pyautogui.screenshot(region=region1)
        img_rgb = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        if loc[0].size > 0:
            find = True
            loc = [loc[1][0] + 0 + w//2 , loc[0][0] + 0 + h//2]
            if debug:
                cv2.circle(img_rgb, loc, 5, (255,0,0), 2)
                cv2.imshow('Screenshot Finding', img_rgb)
                cv2.waitKey(0) 
                cv2.destroyAllWindows()
        loc = [loc[0] + region1[0] , loc[1] + region1[1]]
        return find, loc
    

find, loc = find_template(cv2.imread("Back_to_game.png",0), 0.90, True)
pyautogui.click(loc[0], loc[1])