# USAGE
# python detect_mask_img.py --img imgs/pic1.jpeg

# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.img import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import cv2
import os

 def _open_modal(self):
        log.info("\tOpening GreenButton modal")
        GREEN_BUTTON_XPATH = "//span[contains(text(), 'Green Button')]"
        self._driver.wait().until(
            EC.element_to_be_clickable((By.XPATH, GREEN_BUTTON_XPATH))
        )
        self._driver.find(GREEN_BUTTON_XPATH, xpath=True).click()

        self.screenshot("after opening modal")

def _unzip_archive(self, filename):
        log.info("\tGetting readings from {}".format(filename))
        path = self._zip_path(filename)

        with ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self._driver.download_dir)

        os.remove(path)

    def _zip_path(self, filename):
        return "{}/{}.zip".format(self._driver.download_dir, filename)

def mask_img():
	
	print("[INFO] loading face detector model...")
	prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
	weightsPath = os.path.sep.join([args["face"],
		"res10_300x300_ssd_iter_140000.caffemodel"])
	net = cv2.dnn.readNet(prototxtPath, weightsPath)

	# load the face mask detector model from disk
	print("[INFO] loading face mask detector model...")
	model = load_model(args["model"])

	# load the input img from disk, clone it, and grab the img spatial
	img = cv2.imread(args["img"])
	orig = img.copy()
	(h, w) = img.shape[:2]

	# construct a block from the img
	block = cv2.dnn.blockFromimg(img, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	print("[INFO] computing face detections...")
	net.setInput(block)
	detections = net.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associate
		confidence = detections[0, 0, i, 2]
 
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = img[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)
			face = np.expand_dims(face, axis=0)

			# pass the face through the model to determine if the face
			# has a mask or not
			(mask, withoutMask) = model.predict(face)[0]

			# determine the class label and color we'll use to draw
			# the bounding box and text
			label = "Mask" if mask > withoutMask else "No Mask"
			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

			# include the probability in the label
			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

			# display the label and bounding box rectangle on the output
			# frame
			cv2.putText(img, label, (startX, startY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(img, (startX, startY), (endX, endY), color, 2)

	# show the output img
	cv2.imshow("Output", img)
	cv2.waitKey(0)
	
if __name__ == "__main__":
	mask_img()
