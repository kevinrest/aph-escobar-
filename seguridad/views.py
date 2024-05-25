from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import cv2
import os
import imutils
import numpy as np
from django.contrib import messages
from seguridad import models
from seguridad.forms import Residents
from shutil import rmtree

def Reconociendo(request):
    dataPath = ''"C:/Users/kevin/OneDrive/Documentos/cara/seguridad/reconocimiento/data"
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
            print(f'Rostros: {nameDir + '/' + fileName}')
            labels.append(label)
            facesdata.append(cv2.imread(personPath+'/'+fileName,0))
            image = cv2.imread(personPath+'/'+fileName,0)
            # print(image)
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
    return redirect('login')
    

def Registrar(request):
    if request.method == 'POST':
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            id = request.POST['id']
            edificio = request.POST['edificio']
            aparta = request.POST['aparta'] 


    personName = f'{nombre}_{apellido}'
    dataPath = ''"C:/Users/kevin/OneDrive/Documentos/cara/seguridad/reconocimiento/data"
    personPath = dataPath + '/' + personName
    # print(personPath)

    if not os.path.exists(personPath):
        os.makedirs(personPath)

    url = "https://192.168.0.25:8080/video"
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    while True:
        ret, frame = cap.read()
        if ret == False: break
        frame + imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
            filename = f'/{personName}_{count}.jpg'
            cv2.imwrite(personPath + filename, rostro)
            count += 1
            
            # return rostro
        cv2.imshow('frame',cv2.resize(frame,(800,600)))

        k = cv2.waitKey(1)
        if k == 27 or count == 250: 
            break
   
    fileName = f'/{personName}_{count}.jpg'  
        
    registro = models.residents(identificacion = id, nombre = nombre, edificio = edificio, 
                                apartamento = aparta, cara = fileName, apellido = apellido)
    registro.save()
        
    cap.release()
    cv2.destroyAllWindows()
    Reconociendo(request)
    messages.info(request, 'Registro exitoso')
    return render(request, 'registrar-rostro.html')

def Select(request, filename):
    insert = models.residents.objects.all()

    return render(request,'registration/login.html', {'file': filename, 'insert': insert})


def Reconocimiento(request):
    dataPath = ''"C:/Users/kevin/OneDrive/Documentos/cara/seguridad/reconocimiento/data"
    imagePaths = os.listdir(dataPath)
    

    # face_recognizer = cv2.face.EigenFaceRecognizer_create()
    # face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # leyendo el modelo
    # face_recognizer.read('modeloEigenFace.xml')
    # face_recognizer.read('modeloFisherFace.xml')
    face_recognizer.read('modeloLBPHFace.xml')
    
    url = "https://192.168.1.14:8080/video"
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    file = [] 

    while True:        
        ret, frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxframe = gray.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            rostro = auxframe[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)
            # print(rostro)

            cv2.putText(frame, '{}'.format(result), (x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
            filename = f'/{imagePaths[result[0]]}_250.jpg'
            a = 0
            while len(file) < len(imagePaths):
                file.append(' ')

                file[a] = filename

                a += 1
            print(file)
        
            a = 0
            for i in file:
                a += 1
                if a == len(file):
                    break
                elif file[a-1] == file[a]:
                    file.remove(file[a])
                    file.append(' ')
                    print('borrado')
                
                if len(file[a]) == 1 and file[0] != filename:
                    file[a] = filename
                    print('aqui entro')
                    break
                else:
                    pass

            conjunto = set(file)

            # file = list(conjunto)
                # if file.count(i) > 1:
                #     file.remove(i)
                #     break

            if result[1] < 80:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2) 
            else:
                cv2.putText(frame, 'Desconocido', (x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)
            
            # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)

        cv2.imshow('frame',cv2.resize(frame,(800,600)))

        if cv2.waitKey(1) == ord('Z'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(file)
    return Select(request, conjunto)


def Registrar2(request):
    return render(request, 'registrar-rostro.html')

def Users(request):
    insert = models.residents.objects.all()
    return render(request, 'users.html', {'insert': insert})

def Editar(request, id):
    insert = models.residents.objects.get(identificacion = id)

    if request.method == 'POST':
        form = Residents(request.POST, instance=insert)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = Residents(instance=insert)

    return render(request, 'editar.html', {'form': form})

def Eliminar(request, id):
    dataPath = ''"C:/Users/kevin/OneDrive/Documentos/cara/seguridad/reconocimiento/data"
    imagePaths = os.listdir(dataPath)

    insert = models.residents.objects.get(identificacion = id)

    insert.delete()

    borrar = f'{insert.nombre}_{insert.apellido}'
    a = 0
    for i in imagePaths:
        if i == borrar:
            print('nada')
            borro = imagePaths[a]
            path = dataPath + '/' + borro
            rmtree(path)
        a += 1
        
    # try:
    Reconociendo(request)
    # except:
    #     pass

    return redirect('users')