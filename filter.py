from liblas import file, color


class FilterLas:

    def __init__(self, LasFile):
        print "Initalizing Filter ......."
        self.f = file.File(LasFile, mode='r')
        self.h = self.f.header
        self.lidar_list = [pnt for pnt in self.f]
        self.window_size = 10
        self.window_step = self.window_size  # no-overlapping

    def MeanFilter(self, MeanOut):
        print "Starting Mean Filter..."
        fw = file.File(MeanOut, mode="w", header=self.h)
        for i in range(0, len(self.lidar_list) -
                       self.window_size + 1, self.window_step):
            moving_window = [self.lidar_list[i + j].z
                             for j in range(self.window_size)]
            critical_val = sum(moving_window) / self.window_size
            for j in range(self.window_size):
                if moving_window[j] >= critical_val:
                    fw.write(self.lidar_list[i + j])
                    break
        fw.close()

    def MinFilter(self, MinOut):
        print "Starting Min Filter..."
        fw = file.File(MinOut, mode="w", header=self.h)
        for i in range(0, len(self.lidar_list) - self.window_size + 1,
                       self.window_step):
            moving_window = [self.lidar_list[i + j].z
                             for j in range(self.window_size)]
            critical_val = min(moving_window)
            critical_index = moving_window.index(critical_val)
            fw.write(self.lidar_list[i + critical_index])
        fw.close()

    '''
    def NumReturnsFilter(self,OutName):
        fw = file.File(OutName,mode='w')
        for p in self.lidar_list:
            if(p.number_of_returns > 1):
               fw.write(p)
            else:
                #process lidar data
                p_temp = p
                p.color = color.Color(255,0,0)
                fw.write(OutName)

        fw.close()
     '''


obj = FilterLas("./data/47758.las")
# obj.MinFilter('./data/outputMinFilterSize_10.las')
obj.MeanFilter('./data/outputMeanFilterSize_10.las')
# obj.NumReturnsFilter('./data/number_of_returns.las')