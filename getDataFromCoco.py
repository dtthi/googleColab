from pycocotools.coco import COCO
import numpy as np
import argparse
import subprocess
import time

start = time.time()

parser = argparse.ArgumentParser(description='Get images and label from COCO Person dataset')
parser.add_argument('--dir', help='Path to image file.')
args = parser.parse_args()

dataDir= args.dir
dataVal='val2017'
dataTrain= 'train2017'
print('Entering directory : ' + dataDir )

#Create images, annotations, label folder
subprocess.run(['rm', '-rf', dataDir + '/images'])
subprocess.run(['mkdir', dataDir + '/images'])
print('Create folder: ' + dataDir + '/images')

subprocess.run(['rm', '-rf', dataDir + '/annotations'])
subprocess.run(['mkdir', dataDir + '/annotations'])
print('Create folder: ' + dataDir + '/annotations')

subprocess.run(['rm', '-rf', dataDir + '/labels'])
subprocess.run(['mkdir', dataDir + '/labels'])
subprocess.run(['mkdir', dataDir + '/labels/val2017'])
subprocess.run(['mkdir', dataDir + '/labels/train2017'])
print('Create folder: ' + dataDir + '/labels')
print('Create folder: ' + dataDir + '/labels/val2017')
print('Create folder: ' + dataDir + '/labels/train2017' + '\n')

#Download Coco api
subprocess.run(['git', 'clone', 'https://github.com/pdollar/coco'])

#Get train, validation image, annotations form COCO dataset 2017
print("Download data file")
subprocess.run(['wget', '-c', 'http://images.cocodataset.org/zips/train2017.zip'])
subprocess.run(['wget', '-c', 'http://images.cocodataset.org/zips/val2017.zip'])
subprocess.run(['wget', '-c', 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'])

#unzip data file
print("unzip data file")
subprocess.run(['unzip', '-q', '/content/train2017.zip', '-d', '/content/images'])
subprocess.run(['unzip', '-q', '/content/val2017.zip', '-d', '/content/images'])
subprocess.run(['unzip', '-q', '/content/annotations_trainval2017.zip'])

# Get val images
annFileVal='{}/annotations/instances_{}.json'.format(dataDir,dataVal)
# initialize COCO api for instance annotations
cocoVal=COCO(annFileVal)
# get all images containing given categories: person
catIdsVal = cocoVal.getCatIds(catNms=['person'])
imgIdsVal = cocoVal.getImgIds(catIds=catIdsVal )
imagesVal = cocoVal.loadImgs(imgIdsVal)
print('Number inamges val: %d'%( len(imagesVal) ))
f_val = open("imgVal.txt", 'w')
count = 0
for im in imagesVal:
   f_val.write(dataDir+'/images/val2017/'+ im['file_name']+ '\n')
   heightIMG = im['height']
   widthIMG = im['width']
   annIds = cocoVal.getAnnIds(imgIds=im['id'], catIds=catIdsVal, iscrowd=None)
   anns = cocoVal.loadAnns(annIds)
   strFileLabel = im['file_name'].replace('.jpg', '')
   f_label = open('labels/val2017/%s.txt'%(strFileLabel),'a')
   for i in range(len(anns)):
      if(anns[i]['category_id'] in catIdsVal):
         widthBox = anns[i]['bbox'][2] / widthIMG
         heightBox = anns[i]['bbox'][3] / heightIMG
         center_x = anns[i]['bbox'][0] + (anns[i]['bbox'][2] / 2)
         center_y = anns[i]['bbox'][1] + (anns[i]['bbox'][3] / 2)
         center_x = center_x / widthIMG
         center_y = center_y / heightIMG

         f_label.write(' '.join([str(0),
                                str(center_x),
                                str(center_y),
                                str(widthBox),
                                str(heightBox)])
                      +'\n')
   f_label.close()

f_val.close()


# Get train images
annTrainFile='{}/annotations/instances_{}.json'.format(dataDir,dataTrain)
# initialize COCO api for instance annotations
cocoTrain=COCO(annTrainFile)
# get all images containing given categories: person
catIdsTrain = cocoTrain.getCatIds(catNms=['person'])
imgIdsTrain = cocoTrain.getImgIds(catIds=catIdsTrain )
imagesTrain = cocoTrain.loadImgs(imgIdsTrain)
print('Number inamges val: %d'%( len(imagesTrain) ))
f_train = open("imgTrain.txt", 'w')
count = 0
for im in imagesTrain:  
   f_train.write(dataDir+'/images/train2017/'+ im['file_name']+ '\n')
   heightIMG = im['height']
   widthIMG = im['width']
   annIds = cocoTrain.getAnnIds(imgIds=im['id'], catIds=catIdsTrain, iscrowd=None)
   anns = cocoTrain.loadAnns(annIds)
   strFileLabel = im['file_name'].replace('.jpg', '')
   f_label = open('labels/train2017/%s.txt'%(strFileLabel),'a')
   for i in range(len(anns)):
      if(anns[i]['category_id'] in catIdsTrain):
         widthBox = anns[i]['bbox'][2] / widthIMG
         heightBox = anns[i]['bbox'][3] / heightIMG
         center_x = anns[i]['bbox'][0] + (anns[i]['bbox'][2] / 2)
         center_y = anns[i]['bbox'][1] + (anns[i]['bbox'][3] / 2)
         center_x = center_x / widthIMG
         center_y = center_y / heightIMG

         f_label.write(' '.join([str(0),
                                str(center_x),
                                str(center_y),
                                str(widthBox),
                                str(heightBox)])
                      +'\n')
   f_label.close()

f_train.close()

subprocess.run(['rm', '-rf', '/content/train2017.zip'])
subprocess.run(['rm', '-rf', '/content/val2017.zip'])
subprocess.run(['rm', '-rf', '/content/annotations_trainval2017.zip'])

end = time.time()
runTime = end - start 
print('Get data from Coco dataset completed: (runTime: %.2f)'%(runTime))