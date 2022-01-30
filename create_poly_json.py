import numpy as np
import json
import os
import argparse
from PIL import Image
from time import *
from collections import defaultdict, OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument('--input_semantic', type=str, default="./annotation/label_semantic/", help='the path of <Sol_num>_semanticId.png')
parser.add_argument('--input_instance', type=str, default="./annotation/label_instance/", help='the path of <Sol_num>_instanceId.png')
parser.add_argument('--output', type=str, default="./polygon/", help='config file content labels informations')
opt = parser.parse_args()
ids_name = ['soil','bedrock','gravel','sand','big rock','steep slope','sky','unknown']

def findContours(img, objects):
    for i,ins in enumerate(objects):
        margin = []
        x_min = 10e12
        x_max = 0
        y_min = 10e12
        y_max = 0
        coors = ins['coors']
        for coor in coors:
            if coor['x'] < x_min:
                x_min = coor['x']
            if coor['x'] > x_max:
                x_max = coor['x']
            if coor['y'] < y_min:
                y_min = coor['y']
            if coor['y'] > y_max:
                y_max = coor['y']

            # print('margin judgement for point ({0},{1}) in instance {2}'.format(coor[0],coor[1],i))
            x = coor['x']
            y = coor['y']
            while x >= 0:
                if (img[y,x] == img[coor['y'],coor['x']]):
                    x -= 1
                else:
                    break

            if ({'x':x+1,'y':y} not in margin):
                margin.append({'x':x+1,'y':y})

            x = coor['x']
            y = coor['y']
            while x < img.shape[1]:
                if (img[y,x] == img[coor['y'],coor['x']]):
                    x += 1
                else:
                    break

            if ({'x':x-1,'y':y} not in margin):
                margin.append({'x':x-1,'y':y})

            x = coor['x']
            y = coor['y']
            while y >= 0:
                if (img[y,x] == img[coor['y'],coor['x']]):
                    y -= 1
                else:
                    break

            if ({'x':x,'y':y+1} not in margin):
                margin.append({'x':x,'y':y+1})

            x = coor['x']
            y = coor['y']
            while y < img.shape[0]:
                if (img[y,x] == img[coor['y'],coor['x']]):
                    y += 1
                else:
                    break
                
            if ({'x':x,'y':y-1} not in margin):
                margin.append({'x':x,'y':y-1})

        objects[i]['location'] = {
            'x_min':x_min,
            'y_min':y_min,
            'x_max':x_max,
            'y_max':y_max}
        objects[i]['polygon'] = margin
    return objects


for name in os.listdir(opt.input_instance):
    begin_time = time()
    img_instance = Image.open(opt.input_instance + name)    
    img_instance = np.asarray(img_instance)

    img_semantic = Image.open(opt.input_semantic + name.replace('instance','semantic'))   
    img_semantic = np.asarray(img_semantic)

    dict_mars = OrderedDict()
    dict_mars['height'] = img_instance.shape[0]
    dict_mars['width'] = img_instance.shape[1]
    
    objects = []
    ids = []
    objects = []
    instances = []
    for i in range(img_instance.shape[0]):
        for j in range(img_instance.shape[1]):
            if (img_instance[i,j] != 255) & (img_instance[i,j] not in ids):
                ids.append(img_instance[i,j])
                objects.append({
                    'ins_id': img_instance[i,j],
                    'label': ids_name[img_semantic[i,j]],
                    'coors': [{'x':j,'y':i}]
                })
            elif (img_instance[i,j] != 255) & (img_instance[i,j] in ids):
                for id_o,obj in enumerate(objects):
                    if obj['ins_id'] == img_instance[i,j]:
                        objects[id_o]['coors'].append({'x':j,'y':i})
    
    objects = findContours(img_instance, objects)
    for obj in objects:
        obj.pop('ins_id')
        obj.pop('coors')
    dict_mars['objects'] = objects
    

    json_str = json.dumps(dict_mars, indent=4)
    name_polygon = '{0}_{1}_polygon.json'.format(name.split('_')[0], name.split('_')[1])
    with open(opt.output + name_polygon, 'w') as json_file:
        json_file.write(json_str)

    end_time = time()
    run_time = int((end_time-begin_time)/60)
    print('{0}m for sample {1}_{2}'.format(run_time, name.split('_')[0], name.split('_')[1]))






