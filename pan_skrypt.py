# -*- coding: utf-8 -*-
import time
import webbrowser
import sys
import os
from datetime import date

import pyautogui
import pywinauto

# from pywinauto.application import Application: timings

# img = lokalizacja screena: np. screens/1_ramka_calogin_login.png'
def find_img(img, confidence=0.70, timeout=50, raise_not_found=True):
	print('--- wejscie do find_ramka_img: szukany:', img)
	i = 0
	print('Looking for image ' + img)
	while i < timeout:
		print('--- petla:', i)
		# tmp_screen = self.common['tmp_dir'] + 'ramka.png'
		location = pyautogui.locateOnScreen(img, grayscale=True)
		if location:
			print('--- znaleziono lokalizacje')
			return location
		time.sleep(.5)
		# logger.debug('Looking for image ' + img)
		i += 1
	if raise_not_found:
		raise RuntimeError("Image not found!")
	return None
 
def click_mouse(leftoffset, topoffset, location):
	print('Click: X: {} Y: {}'.format(location[0] + leftoffset, location[1] + topoffset))
	pywinauto.mouse.click(coords=(location[0] + leftoffset, location[1] + topoffset))
 
def typing_on_keyboard(keys):
	print('Typing: {}'.format(keys))
	pywinauto.keyboard.SendKeys(keys)
 
# odpalenie strony settlers i wejście do gry


images_play_list = [
	# 'Screeny/1_scr_log.png', 
	'Screeny/2_scr_play.png', 
	'Screeny/3_scr_fsh_agg.png', 
	'Screeny/4_scr_flash_agree.png', 
	'Screeny/2_scr_play.png'
]

offsets_dict = {
	# 'Screeny/1_scr_log.png' : (0,0),
	'Screeny/2_scr_play.png' : (0,0),
	'Screeny/3_scr_fsh_agg.png' : (.5,.5), #poprzerabiać na %
	'Screeny/4_scr_flash_agree.png' : (0,0),
	'Screeny/5_scr_tick.png' : (.5,.5),
	'Screeny/6_scr_guild.png' : (.5,.5),
	'Screeny/7_scr_main.png' : (.5,.5),
	'Screeny/8_scr_members.png' : (.1,.5),
	'Screeny/9_scr_name.png' : (0,0),
	'Screeny/10_scr_arrow.png' : (0,0)
}

# TODO: jason -> konfiguracja przeglądarki
webbrowser.open('https://www.thesettlersonline.pl/pl/strona-g%C5%82%C3%B3wna', new=1)

#Włączanie gry dla zalogowanego gracza
for image in images_play_list:
	loc = find_img(image)
	topoffset = int(offsets_dict[image][0] * loc[2])
	leftoffset = int(offsets_dict[image][1] * loc[3])
	click_mouse(topoffset, leftoffset, loc)
# TODO: obsługa niezalogowanego gracza
# TODO: obsługa nowej karty
# TODO: Jason -> Left ofset: topofset

#czekanie na ekran logowania
time.sleep(10)

#dotarcie do zakładki kto odklikał zg
imgage_screen_list = [
	'Screeny/5_scr_tick.png',
	'Screeny/6_scr_guild.png',
	'Screeny/7_scr_main.png',
	# 'Screeny/8_scr_members.png',
	'Screeny/9_scr_name.png'
]

for image in imgage_screen_list:
	loc = find_img(image)
	topoffset = int(offsets_dict[image][0] * loc[2])
	leftoffset = int(offsets_dict[image][1] * loc[3])
	click_mouse(topoffset, leftoffset, loc)
#TODO: obsługa mrożenia ekranu przy logowaniu

# robienie screenshotów

loc_1 = find_img('Screeny/9_scr_name.png')
loc_2 = find_img('Screeny/10_scr_arrow.png')

def screen_shot(loc_1,loc_2):
	x_screen = loc_1[0]
	y_screen = loc_1[1]+loc[3]
	w_screen = loc_2[0]-x_screen
	h_screen = loc_2[1]-y_screen
	return pyautogui.screenshot(region=(x_screen,y_screen, w_screen, h_screen))

dir_name = 'Screenshots/'+ str(date.today())
try:
	os.mkdir(dir_name)
except FileExistsError:
	pass
# screen_shot(loc_1, loc_2)
myScreenshot = screen_shot(loc_1, loc_2)
myScreenshot.save(dir_name+'/1.png')
screen_arrow = 'Screeny/10_scr_arrow.png'
loc_arr = find_img(screen_arrow)
leftoffset = int(offsets_dict[screen_arrow][1] * loc_arr[3])
topoffset = int(offsets_dict[screen_arrow][0] * loc_arr[2])
j=2
while j<11:
	i=0
	while i <10:
		click_mouse(topoffset, leftoffset, loc_arr)
		i=i+1
	myScreenshot = screen_shot(loc_1, loc_2)
	myScreenshot.save(dir_name+'/'+str(j)+'.png')
	j=j+1

# zamknięcie przeglądarki
webbrowser. close()
sys.exit(0)