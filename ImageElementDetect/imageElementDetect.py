import numpy as np
import cv2

class ImageElementDetect:
	def __init__(self, filePath, verbose=False):
		"""
		Face utility
		:param filePath: image path
		:param verbose: True, False. Display result if true
		:return:
		"""
		self._filePath = filePath
		self._verbose = verbose

	def hasFaces(self):
		return self.countFaces() > 0

	def countFaces(self):
		"""
		Count faces in the image with CascadeClassifier
		:return: int, nb faces
		"""

		#http://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html#gsc.tab=0
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		img = cv2.imread(self._filePath)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)


		if self._verbose:
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

			cv2.imshow('faces',img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return len(faces)





