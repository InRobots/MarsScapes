import numpy as np
from PIL import Image
import os

path_input = ['./image', './annotation/label_semantic']
path_processed = './processed'

if not os.path.exists(os.path.join(path_processed, 'train')):
    os.mkdir(os.path.join(path_processed, 'train'))
if not os.path.exists(os.path.join(path_processed, 'val')):
    os.mkdir(os.path.join(path_processed, 'val'))
if not os.path.exists(os.path.join(path_processed, 'test')):
    os.mkdir(os.path.join(path_processed, 'test'))
if not os.path.exists(os.path.join(path_processed, 'list')):
    os.mkdir(os.path.join(path_processed, 'list'))

list_train = open(os.path.join(path_processed, 'list', 'train.txt'), 'a')
list_val = open(os.path.join(path_processed, 'list', 'val.txt'), 'a')
list_test = open(os.path.join(path_processed, 'list', 'test.txt'), 'a')

h0 = 512
w0 = 512
overlap_ratio = 0.5
overlook_ratio = 0.75
id = 0
for p in path_input:
    for name in os.listdir(p):
        image = np.asarray(Image.open(os.path.join(p, name)))
        h = image.shape[0]
        w = image.shape[1]
        deta_h = int(h / (h0*(1-overlap_ratio))) + 1
        deta_w = int(w / (w0*(1-overlap_ratio))) + 1
        
        for i in range(deta_h):
            for j in range(deta_w):
                for flip in [1,-1]:
                    flip_id = 1 if flip==-1 else 0
                    if 'color' in name:
                        name_save = name.replace('color', '{0}_{1}_{2}_color'.format(i, j, flip_id))
                    elif 'semanticId' in name:
                        name_save = name.replace('semanticId', '{0}_{1}_{2}_semanticId'.format(i, j, flip_id))
                    else:
                        name_save = '{0}_{1}_{2}_{3}.png'.format(name.split('.')[0], i, j, flip_id)

                    if (os.path.exists(os.path.join(path_processed, 'train', name_save)) |
                        os.path.exists(os.path.join(path_processed, 'test', name_save)) |
                        os.path.exists(os.path.join(path_processed, 'val', name_save))):
                        print('skip ' + name_save)
                        continue
                    
                    # crop horizontally and vertically
                    if (h0+i*int(h0*(1-overlap_ratio)) > h) & (w0+j*int(w0*(1-overlap_ratio)) <= w):
                        if name.split('_')[-1] == 'semanticId.png':
                            cropped = np.zeros((h0, w0)).astype(int) + 255
                        else:
                            cropped = np.zeros((h0, w0, 3))
                        cropped[0:h-i*int(h0*(1-overlap_ratio)), 0:w0] = image[i*int(h0*(1-overlap_ratio)):h, j*int(w0*(1-overlap_ratio)):w0+j*int(w0*(1-overlap_ratio))]
            
                    elif (h0+i*int(h0*(1-overlap_ratio)) <= h) & (w0+j*int(w0*(1-overlap_ratio)) > w):
                        if name.split('_')[-1] == 'semanticId.png':
                            cropped = np.zeros((h0, w0)).astype(int) + 255
                        else:
                            cropped = np.zeros((h0, w0, 3))                   
                        cropped[0:h0, 0:w-j*int(w0*(1-overlap_ratio))] = image[i*int(h0*(1-overlap_ratio)):h0+i*int(h0*(1-overlap_ratio)), j*int(w0*(1-overlap_ratio)):w]
                    
                    elif (h0+i*int(h0*(1-overlap_ratio)) > h) & (w0+j*int(w0*(1-overlap_ratio)) > w):
                        if name.split('_')[-1] == 'semanticId.png':
                            cropped = np.zeros((h0, w0)).astype(int) + 255
                        else:
                            cropped = np.zeros((h0, w0, 3))
                        cropped[0:h-i*int(h0*(1-overlap_ratio)), 0:w-j*int(w0*(1-overlap_ratio))] = image[i*int(h0*(1-overlap_ratio)):h, j*int(w0*(1-overlap_ratio)):w]

                    else:
                        cropped = image[0+i*int(h0*(1-overlap_ratio)):h0+i*int(h0*(1-overlap_ratio)), 0+j*int(w0*(1-overlap_ratio)):w0+j*int(w0*(1-overlap_ratio))]
                    
                    count = 0
                    for a in range(h0):
                        for b in range(w0):
                            if name.split('_')[-1] == 'semanticId.png':
                                if cropped[a,b] == 255:
                                    count += 1
                            else:
                                if all(cropped[a,b] == [0,0,0]):
                                    count += 1
                                    
                    # discard sub-images with fewer pixels
                    if count > w0 * h0 * overlook_ratio:
                        continue
                    
                    # flip horizontally
                    if name.split('_')[-1] == 'semanticId.png':
                        cropped = cropped[:, ::flip]
                        cropped = Image.fromarray(np.uint8(cropped))
                    else:
                        cropped = cropped.transpose((2,0,1))
                        cropped = cropped[:, :, ::flip]
                        cropped = Image.fromarray(np.uint8(cropped.transpose((1,2,0))), mode='RGB')

                    # 3:1:1
                    id = id + 1
                    if (id > 3) & ((id + 1) % 5 == 0):
                        cropped.save(os.path.join(path_processed, 'val', name_save))
                        list_val.write('val/' + name_save + '\n')
                    elif (id > 3) & (id % 5 == 0):
                        cropped.save(os.path.join(path_processed, 'test', name_save))
                        list_test.write('test/' + name_save + '\n')
                    else:
                        cropped.save(os.path.join(path_processed, 'train', name_save))
                        list_train.write('train/' + name_save + '\n')

list_train.close()
list_val.close()
list_test.close()