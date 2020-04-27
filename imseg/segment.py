import os
def segmentation_module(path):
    dirpath = os.getcwd()
#    dirpath = dirpath[:-6]
    dirpath = os.path.join('tmp')
    f1 = os.path.join(dirpath, '1.png')
    f2 = os.path.join(dirpath, '2.png')
    f3 = os.path.join(dirpath, '3.png')
    return [f1, f2, f3]
