import shutil
import os


def mkdir(dir):
    if(not os.path.exists(dir)):
        os.makedirs(dir)

def mk_dataset(src,name):
    tar_file = os.path.join(os.getcwd(),'2022_KIPIA_Bench','data')
    mkdir(tar_file)
    shutil.copyfile(src, tar_file+'/'+name)

def read_txt(path):
    with open(path,'r') as f:
        data = f.readlines()
        return data

if __name__ == "__main__":
    path = os.path.join(os.getcwd(),'output','ts_list.txt')
    data = read_txt(path)
    for i in data:
        src = i.split(' ')[0]
        name = src.split('/')[-1]
        mk_dataset(src,name)