import os
import json
import glob

class json_txt():
    def __init__(self,path):
        self.path = path
        self.folder_name = os.listdir(path)
        
        ### hyper param
        self.output = './output/'
        self.need_num = 20001
        # self.need_num = 10000
        self.selec_name_list = ['SS','DA']
        self.label_n = [
                        'traffic sign',
                        'car',
                        'truck',
                        'special vehicle',
                        'bus',
                        'pedestrian',
                        'motorcycle'
                        ]

        ### initilize
        self.num_pic = 0
        self.readable_path = []
        self.label_list = []
        self.bbox_list =[]
        self.obj_info_list =[]
        self.flag = True
        
        ###The param for checking bug(ignore)
        self.temp0 = 0
        self.temp1 = 0
        self.temp2 = 0
        self.temp3 = []

    ### Counting number of pictures 
    def count_file(self,file_path):
        with open(file_path + os.sep + 'file_count.' + "txt", 'r') as f:
            self.num_pic += int(f.readlines()[0].split(':')[1])
            self.readable_path.append(file_path)
        # print(file_path)
        # print(self.num_pic)

    ### Select folder name
    def select_folder(self):
        for i in self.folder_name:
            ### jurdge the folder or not and wanted folder name
            ### also can use "os.path.isdir()"
            tyep_n = i.split('.')
            if len(tyep_n) == 1:
                sele_name = tyep_n[0][:2]
                if sele_name in self.selec_name_list:
                    # if self.num_pic >= self.need_num:
                    self.count_file(self.path + os.sep + i)
                    
    ### Main for read json file
    def read_json(self,file_path):
        ### File name list ==> fname_l
        j_fname_l = glob.glob(file_path + os.sep + 'labels' + os.sep + "**.json" )
        i_fname_l = glob.glob(file_path + os.sep + 'JPEGImages' + os.sep + "**.jpg" )
        i_fname = file_path + os.sep + 'JPEGImages' + os.sep

        for j_count in range(len(j_fname_l)):
            img_path = i_fname + j_fname_l[j_count].split('.json')[0].split('/')[-1] + '.jpg'
            if len(self.obj_info_list) >= self.need_num:
                self.flag = False
                break
            
            ###test
            ## For checking img
            # if img_path in i_fname_l:
                # print(img_path)
            ## For checking img
            
            obj_info = []
            with open(j_fname_l[j_count],'r') as f :
                data = json.load(f)
                obj_list = data.get('Annotation')
                size = data.get('Source_Image_Info').get('Resolution')

                for ii in range(len(obj_list)):
                    label = obj_list[ii].get('Label')
                    # ### For checking all label name
                    # if not label in self.label_list : 
                    #     self.label_list.append(label)
                    # ###For checking all label name
                    
                    ### Main process continue
                    if  label in self.label_n :
                        bbox = obj_list[ii].get('Coordinate')
                        bbox_info = self.yolo_transform(bbox,label,size)
                        obj_info.append(bbox_info)
            if obj_info != []:    
                obj_info.insert(0,img_path)
                self.obj_info_list.append(obj_info)

    ###Convert YOLO Format
    def yolo_transform(self,bbox_info,label_info,size_info):
        # print('yolo')
        # print(bbox_info,label_info)
        dw = 1./size_info[0]
        dh = 1./size_info[1]
        x = (bbox_info[0] + bbox_info[2])/2.0
        y = (bbox_info[1] + bbox_info[3])/2.0
        w = bbox_info[2] - bbox_info[0]
        h = bbox_info[3] - bbox_info[1]
        x = round(x*dw,6)
        w = round(w*dw,6)
        y = round(y*dh,6)
        h = round(h*dh,6)
        label_ind = self.label_n.index(label_info)
        return [x,y,w,h,label_ind]
    
    def mkdir(self,dir):
        if(not os.path.exists(dir)):
            os.makedirs(dir)
    
    ###Write txt file
    def write_txt(self,obj_info):
        self.mkdir(self.output)
        for i in range(len(obj_info)):
            flag = True
            for o in range(len(obj_info[i])):
                contents = str(obj_info[i][o])
                ###Delete []
                if contents[0] == '[':
                    contents = contents.split('[')[1].split(']')[0]
                if o <len(obj_info[i])-1:
                    with open(self.output + 'ts_list.txt','a') as f :
                        f.write(contents + " ")
                else:
                    with open(self.output + 'ts_list.txt','a') as f :
                        f.write(contents + "\n")

    def main(self):
        self.select_folder()
        for i in self.readable_path:
            if self.flag:
                self.read_json(i)
        print(len(self.obj_info_list))
        self.write_txt(self.obj_info_list)
        
        # ### For checking all label name
        # print(self.label_list)
        # ### For checking all label name

if __name__ == "__main__":
    path = os.path.join(os.getcwd(),'full_set')
    js = json_txt(path)
    js.main()

    