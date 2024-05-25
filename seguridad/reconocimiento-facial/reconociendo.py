import cv2
import os
import numpy as np
from zipfile import ZipFile
from seguridad import models

dataPath = "C:/Users/57301/Documents/proyecto/facecheck/gimnasio/reconocimiento/data"
peoplelist = os.listdir(dataPath)

labels = []
facesdata = []
label = 0

for nameDir in peoplelist:
    personPath = dataPath + '/' + nameDir
    
    pathScript = os.path.dirname(os.path.dirname(__file__))
    pathArchivo = personPath
    pathCompleto = os.path.join(pathScript, pathArchivo)

    print('Leyendo las imagenes')
    
    for fileName in os.listdir(personPath):
        labels.append(label)
        facesdata.append(cv2.imread(personPath+'/'+fileName,0))
        image = cv2.imread(personPath+'/'+fileName,0)
        # cv2.imshow('image',image)
        # cv2.waitKey(10)
    label += 1
    

# face_recognizer = cv2.face.EigenFaceRecognizer_create()
# face_recognizer = cv2.face.FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# reconociendo
face_recognizer.train(facesdata, np.array(labels))

# almacenando reconocedor
# face_recognizer.write('modeloEigenFace.xml')
# face_recognizer.write('modeloFisherFace.xml')
face_recognizer.write('modeloLBPHFace.xml')
