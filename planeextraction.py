from liblas import file, header
from PIL import Image
import subprocess
from math import ceil


class planeextraction:

    def __init__(self, onlybuildings, PlaneImage):
        only_building = file.File(onlybuildings, mode='r')

        # Get the value of bounding box
        height = width = 0
        oldlasnm = onlybuildings
        outputtxt = 'output.txt'

        fout = open(outputtxt, 'w')
        cmd = 'lasinfo ' + oldlasnm + '>' + outputtxt
        subprocess.check_output(cmd, shell=True)
        fout.close()

        rows = [i.split()[2:] for i in open(outputtxt, 'r') if "Bounding" in i]
        box = [i.strip(',') for i in rows[0]]
        minx = float(box[0])
        miny = float(box[1])
        maxx = float(box[2])
        maxy = float(box[3])
        height = int(ceil(maxy - miny))
        width = int(ceil(maxx - minx))
        print(height, width)

        h = header.Header()
        h.dataformat_id = 3
        # h = only_building.header
        print(h.min, h.max)

        lidar_list = [pnt for pnt in only_building]
        im = Image.new('RGB', (height, width))

        for i in range(0, len(lidar_list)):
            temp = lidar_list[i]
            temp.z = 0
            im.putpixel([int(temp.x - minx), int(temp.y - miny)],
                        (temp.color.red, temp.color.green, temp.color.blue))
            # im.append((temp.color.red, temp.color.green, temp.color.blue))
            # print(temp.color.red, temp.color.green, temp.color.blue)
            # fw.write(temp)

        # im.putdata([(i.color.red,i.color.green, i.color.blue)
        # for i in lidar_list])
        im.save(PlaneImage)

        print(len(lidar_list))
        # fw.close()
        only_building.close()


obj = planeextraction("./data/Only_Buildings.las", './data/planerized.png')