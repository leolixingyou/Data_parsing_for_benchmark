import os
import glob

def write_txt(output,fname):
    with open(fname,'a') as f:
        f.write(output + '\n')

def read_txt(path):
    with open(path,'r') as f:
        data = f.readlines()
        return data

if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(),'data')
    txt_path = os.path.join(os.getcwd(),'ts_list.txt')
    fname = os.path.join(os.getcwd(),'Benchmark_data.txt')
    data=read_txt(txt_path)
    for i in data: 
        name = i.split('/')[-1]
        output = output_path + '/' + name
        write_txt(output,fname)