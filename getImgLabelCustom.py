import subprocess
import os

dataDir = '/content'
image_dir = '/content/Output/IMG'
label_dir = '/content/Output/LABEL'
path, dirs, files = next(os.walk(image_dir))
numberImg = len(files)

print('Number img custom image: %d'%(numberImg))

f_train = open("imgTrain.txt", 'a')

for f in os.listdir(image_dir):
   # How to use find() 
   if (f.find('jpg') != -1): 
      subprocess.run(['cp', image_dir + '/' + f, '/content/images/train2017/'])
      f_train.write(dataDir+'/images/train2017/'+ f + '\n')
      strFileLabel = f.replace('.jpg', '.txt')
      subprocess.run(['cp', label_dir + '/' + strFileLabel, '/content/labels/train2017'])

f_train.close()


