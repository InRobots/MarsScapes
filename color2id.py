import numpy as np
from PIL import Image
import os

path_semantic = './annotation/label_semantic'
name_label = os.listdir(path_semantic)
for name in name_label:
    if name.split('_')[-1] == 'color.png':
        name_Id = name.replace('color.png', 'semanticId.png')
        if os.path.exists(os.path.join(path_semantic, name_Id)):
            print('{0} skipped'.format(name))
            continue

        label = np.asarray(Image.open(os.path.join(path_semantic, name)))
        label_Id = np.zeros((label.shape[0], label.shape[1]))
        for i in range(label.shape[0]):
            for j in range(label.shape[1]):
                if all(label[i,j]==[0,0,0]):
                    label_Id[i,j] = 255

                elif all(label[i,j]==[0,0,255]):
                    label_Id[i,j] = 0
                    
                elif all(label[i,j]==[0,255,0]):
                    label_Id[i,j] = 1
                    
                elif all(label[i,j]==[255,0,0]):
                    label_Id[i,j] = 2
                    
                elif all(label[i,j]==[255,0,255]):
                    label_Id[i,j] = 3
                    
                elif all(label[i,j]==[255,255,0]):
                    label_Id[i,j] = 4
                    
                elif all(label[i,j]==[0,255,255]):
                    label_Id[i,j] = 5
                    
                elif all(label[i,j]==[34,56,19]):
                    label_Id[i,j] = 6
                    
                elif all(label[i,j]==[170,85,0]):
                    label_Id[i,j] = 7

                else:
                    print('Error point ({0},{1}) in {2}'.format(i,j,name))
                    
        label_Id = Image.fromarray(label_Id).convert('L')
        label_Id.save(os.path.join(path_semantic, name_Id))
        print('{0} finished'.format(name))