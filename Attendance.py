import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime




def markscan (path):

	images = cv2.imread(path)

	def encodings(img):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encode = face_recognition.face_encodings(img)[0]
		print('encoding completed!!')
		return encode

	encodelistknown = []
	encodelistknown.append(encodings(images))

	cap = cv2.VideoCapture(0)

	i=0

	while i<20:
		success, img = cap.read()
		imgs = cv2.resize(img,(0,0),None,0.25,0.25)
		imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		faces =  face_recognition.face_locations(imgs)
		encodescurr = face_recognition.face_encodings(imgs,faces)

		flag = 0;


		for encodeface,faceloc in zip(encodescurr,faces):

			y1,x2,y2,x1 = faceloc
			cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)

			matches = face_recognition.compare_faces(encodelistknown,encodeface)
			faceDis = face_recognition.face_distance(encodelistknown,encodeface)
			matchperson = np.argmin(faceDis)

			if matches[matchperson]:
				flag = 1
				break;

		cv2.imshow('webcam',img)
		cv2.waitKey(1)

		if flag:
			print('SUCCESS')
			return True
		else:
			print('Scanning...')
			i+=1
	return False