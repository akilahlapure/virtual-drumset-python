# Virtual Drums
# Author: Navendu Pottekkat https://bit.ly/navendupottekkat
# MIT License

# Source code: https://www.github.com/navendu-pottekkat/virtual-drums

# Importing the necessary libraries
import numpy as np
import time
import cv2
from pygame import mixer
import imutils

# This function plays the corresponding drum beat if a red color object is detected in the region
def play_beat(detected,sound):
	# Importing drum beats
	mixer.init()

	drum_kick = mixer.Sound('./sounds/1_kick.wav')
	drum_snare = mixer.Sound('./sounds/2_snare.wav')
	drum_hat = mixer.Sound('./sounds/3_hihat-close.wav')
	drum_hato = mixer.Sound('./sounds/4_hihat-open.wav')
	drum_tom = mixer.Sound('./sounds/5_tom-sm.wav')
	drum_ride = mixer.Sound('./sounds/6_ride.wav')
	drum_crash = mixer.Sound('./sounds/7_crash-bla.wav')

	# Checks if the detected red color is greater that a preset value 	
	play = (detected) > kick_thickness[0]*kick_thickness[1]*0.8

	# If it is detected play the corresponding drum beat
	if play and sound==1:
		drum_kick.play()
		time.sleep(0.01) # add delay of 0.01 sec
		
	elif play and sound==2:
		drum_snare.play()
		time.sleep(0.01)
	
	elif play and sound==3:
		drum_hat.play()
		time.sleep(0.01)

	elif play and sound==4:
		drum_hato.play()
		time.sleep(0.01)

	elif play and sound==5:
		drum_tom.play()
		time.sleep(0.01)

	elif play and sound==6:
		drum_ride.play()
		time.sleep(0.01)

	elif play and sound==7:
		drum_crash.play()
		time.sleep(0.01)


# This function is used to check if red color is present in the small region
def detect_in_region(frame,sound):
	
	# Converting to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Creating mask
	mask = cv2.inRange(hsv, redLower, redUpper)
	
	# Calculating the number of red pixels
	detected = np.sum(mask)
	
	# Call the function to play the drum beat
	play_beat(detected,sound)

	return mask

# A flag variable to choose whether to show the region that is being detected
verbose = False

# Set HSV range for detecting red color 
redLower = (131, 90, 106)
redUpper = (255,255,255)

# Obtain input from the webcam 
camera = cv2.VideoCapture(0)
ret,frame = camera.read()

kernel = np.ones((7,7),np.uint8)

# Read the images
# cv2.resize(src, desired size, interpolation)
kick = cv2.resize(cv2.imread('images/kick-cropped.png'),(420,280),interpolation=cv2.INTER_CUBIC)
snare = cv2.resize(cv2.imread('images/snare.png'),(210,130),interpolation=cv2.INTER_CUBIC)
hihat = cv2.resize(cv2.imread('images/ride-btm-cropped.png'),(210,440),interpolation=cv2.INTER_CUBIC)
hihat_open = cv2.resize(cv2.imread('images/ride-side-cropped.png'),(200,570),interpolation=cv2.INTER_CUBIC) 
tom = cv2.resize(cv2.imread('images/tom.png'),(220,170),interpolation=cv2.INTER_CUBIC)
ride = cv2.flip(cv2.resize(cv2.imread('images/ride-btm-cropped.png'),(210,440),interpolation=cv2.INTER_CUBIC), 1) #flip image horizontally
crash = cv2.flip(cv2.resize(cv2.imread('images/ride-side-cropped.png'),(200,570),interpolation=cv2.INTER_CUBIC), 1) #flip image horizontally

# Set the region area for detecting red color 
kick_center = [446,534] #[x, y]
kick_thickness = [420,280]
kick_top = [kick_center[0]-kick_thickness[0]//2,kick_center[1]-kick_thickness[1]//2]
kick_btm = [kick_center[0]+kick_thickness[0]//2,kick_center[1]+kick_thickness[1]//2]

snare_center = [708,500]
snare_thickness = [210,130]
snare_top = [snare_center[0]-snare_thickness[0]//2,snare_center[1]-snare_thickness[1]//2]
snare_btm = [snare_center[0]+snare_thickness[0]//2,snare_center[1]+snare_thickness[1]//2]

hihat_center = [740,454]
hihat_thickness = [210,440]
hihat_top = [hihat_center[0]-hihat_thickness[0]//2,hihat_center[1]-hihat_thickness[1]//2]
hihat_btm = [hihat_center[0]+hihat_thickness[0]//2,hihat_center[1]+hihat_thickness[1]//2]

hihat_open_center = [800,350]
hihat_open_thickness = [200,570]
hihat_open_top = [hihat_open_center[0]-hihat_open_thickness[0]//2,hihat_open_center[1]-hihat_open_thickness[1]//2]
hihat_open_btm = [hihat_open_center[0]+hihat_open_thickness[0]//2,hihat_open_center[1]+hihat_open_thickness[1]//2]

tom_center = [160,528]
tom_thickness = [220,170]
tom_top = [tom_center[0]-tom_thickness[0]//2,tom_center[1]-tom_thickness[1]//2]
tom_btm = [tom_center[0]+tom_thickness[0]//2,tom_center[1]+tom_thickness[1]//2]

ride_center = [140,454]
ride_thickness = [210,440]
ride_top = [ride_center[0]-ride_thickness[0]//2,ride_center[1]-ride_thickness[1]//2]
ride_btm = [ride_center[0]+ride_thickness[0]//2,ride_center[1]+ride_thickness[1]//2]

crash_center = [100,350]
crash_thickness = [200,570]
crash_top = [crash_center[0]-crash_thickness[0]//2,crash_center[1]-crash_thickness[1]//2]
crash_btm = [crash_center[0]+crash_thickness[0]//2,crash_center[1]+crash_thickness[1]//2]

time.sleep(1)

while True:
	
	# Select the current frame
	ret, frame = camera.read()
	frame = cv2.flip(frame,1)
	frame = imutils.resize(frame, height=700, width=900)

	if not(ret): break

	# Select region corresponding to the kick drum
	kick_region = np.copy(frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]])
	mask = detect_in_region(kick_region, 1)

	# snare
	snare_region = np.copy(frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]])
	mask = detect_in_region(snare_region, 2)

	# hihat 
	hihat_region = np.copy(frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]])
	mask = detect_in_region(hihat_region, 3)

	# hihat_open
	hihat_open_region = np.copy(frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]])
	mask = detect_in_region(hihat_open_region, 4)

	# tom
	tom_region = np.copy(frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]])
	mask = detect_in_region(tom_region, 5)

	# ride
	ride_region = np.copy(frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]])
	mask = detect_in_region(ride_region, 6)

	# crash
	crash_region = np.copy(frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]])
	mask = detect_in_region(crash_region, 7)

	# Output project title
	cv2.putText(frame,'Virtual Drums',(10,30),2,1,(20,20,20),2)
    
	# If flag is selected, display the region under detection
	if verbose:
		frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]] = cv2.bitwise_and(frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]],frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]], mask=mask[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]])
		frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]] = cv2.bitwise_and(frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]],frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]], mask=mask[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]])
		frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]] = cv2.bitwise_and(frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]],frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]], mask=mask[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]])
		frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]] = cv2.bitwise_and(frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]],frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]], mask=mask[hihat_open_top[1]:hihat_open_btm[1],tom_top[0]:hihat_open_btm[0]])
		frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]] = cv2.bitwise_and(frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]],frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]], mask=mask[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]])
		frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]] = cv2.bitwise_and(frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]],frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]], mask=mask[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]])
		frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]] = cv2.bitwise_and(frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]],frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]], mask=mask[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]])
    
	# If flag is not selected, display the drums
	else:
		frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]] = cv2.addWeighted(kick, 1, frame[kick_top[1]:kick_btm[1],kick_top[0]:kick_btm[0]], 1, 0)
		frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]] = cv2.addWeighted(snare, 1, frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]], 1, 0)
		frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]] = cv2.addWeighted(hihat, 1, frame[hihat_top[1]:hihat_btm[1],hihat_top[0]:hihat_btm[0]], 1, 0)
		frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]] = cv2.addWeighted(hihat_open, 1, frame[hihat_open_top[1]:hihat_open_btm[1],hihat_open_top[0]:hihat_open_btm[0]], 1, 0)
		frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]] = cv2.addWeighted(tom, 1, frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]], 1, 0)
		frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]] = cv2.addWeighted(ride, 1, frame[ride_top[1]:ride_btm[1],ride_top[0]:ride_btm[0]], 1, 0)
		frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]] = cv2.addWeighted(crash, 1, frame[crash_top[1]:crash_btm[1],crash_top[0]:crash_btm[0]], 1, 0)

    
    
	cv2.imshow('Output',frame)
	key = cv2.waitKey(1) & 0xFF
	# 'Q' to exit (quit application)
	if key == ord("q"):
		break
 
# Clean up the open windows
camera.release()
cv2.destroyAllWindows()