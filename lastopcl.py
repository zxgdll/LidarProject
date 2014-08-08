import pcl
from liblas import file


'''
Needs Input a LasFile and Output a PcdFile
'''


class lastopcl:

    def __init__(self, LasFile, PcdFile):
        newcloud = pcl.PointCloud()
        _file = file.File(LasFile, mode='r')
        h = _file.header
        _val = []
        for pnt, i in zip(_file, range(30000)):
            c = pnt.color
            _val.append([pnt.x, pnt.y, pnt.z])

        print "Importing into pcl----------------------------"
        newcloud.from_list(_val)
        '''
        fil = newcloud.make_statistical_outlier_filter()
        fil.set_mean_k (50)
        fil.set_std_dev_mul_thresh (1.0)

        fil.filter().to_file("test.pcd")
        '''
        newcloud.to_file(PcdFile)

        print "Done importing into pcl-----------------------"
