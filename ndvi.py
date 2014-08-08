# script to merge several individual Tiffs (bands) into one multiband GeoTiff
# and potentially do calculations like NDVI, albedo, etc...

# import the GDAL and numpy libraries
from osgeo import gdal
import numpy as np
from PIL import Image
from liblas import file
from liblas import header
import subprocess


class ndvi:

    def __init__(self):
        pass
    
    def lastotif(self, x, y, minx, miny, maxx, maxy, m, n):
            xlen = maxx - minx
            ylen = maxy - miny
            resx = int((x - minx) * n / xlen)
            resy = int((maxy - y) * m / ylen)
            return (resx, resy)

    def vegetation(self, SatImage, OutImage):        
        # ok lets load in the first 4 bands of Landsat
        # imagery into their own numpy arrays
        # the numpy arrays are named band1, band2, etc.
        print "Initializing Ndvi......"
        im = Image.open(SatImage)
        im.load()
        source = im.split()
        source[0].save("2009_47758red.tif")
        source[1].save("2009_47758nir.tif")
        # g = gdal.Open("./data/2009_47758red.tif")
        band3 = source[0]
        print "Starting........."
        g = gdal.Open("2009_47758nir.tif")  # near infrared bandd
        band4 = source[1]
        band4 = np.array(band4, dtype=float)
        band3 = np.array(band3, dtype=float)
        del source
        print("Red and NIR Bands created !!!")

        # these variables will get information about the input Tiff so we can
        # write out our new Tiff into the correct geographic space and with
        # correct row/column dimensions

        geo = g.GetGeoTransform()  # get the datum
        proj = g.GetProjection()  # get the projection
        # get the image dimensions - format (row, col)
        shape = band3.shape
        print("Image dimensions taken!!!")
        # freeing memory
        del g
        # Lets do an NDVI calc
        var1 = np.subtract(band4, band3)
        var2 = np.add(band4, band3)
        # freeing memory
        del band4
        del band3

        ndvi = np.divide(var1, var2)
        # freeing memory
        del var1
        del var2
        print("NDVI calculations done!!!")

        # here we write out the new image, only one band to write out in this
        # case

        driver = gdal.GetDriverByName('GTiff')
        dst_ds = driver.Create(
            OutImage, shape[1], shape[0], 1, gdal.GDT_Float32)
        # here we set the variable dst_ds with
        # destination filename, number of columns and rows
        # 1 is the number of bands we will write out
        # gdal.GDT_Float32 is the data type - decimals
        dst_ds.SetGeoTransform(geo)  # set the datum
        dst_ds.SetProjection(proj)  # set the projection

        # write numpy array band1 as the first band of the multiTiff - this is
        # the blue band
        dst_ds.GetRasterBand(1).WriteArray(ndvi)
        # get the band statistics (min, max, mean, standard deviation)
        stat = dst_ds.GetRasterBand(1).GetStatistics(1, 1)
        # set the stats we just got to the band
        dst_ds.GetRasterBand(1).SetStatistics(
            stat[0], stat[1], stat[2], stat[3])

        # that's it, close Python and load your NDVI image into QGIS !!
        print("Done!!!")

    def removevegetation(self, newlasfile, oldlasfile, NdviImage):
        h = header.Header()
        h.dataformat_id = 3
        h.minor_version = 1
        ###############################################
        '''get bounding box'''
        ##################################################
        outputtxt = './data/output.txt'
        
        fout = open(outputtxt, 'a')
        cmd = 'lasinfo ' + oldlasfile + '>' + outputtxt
        subprocess.check_output(cmd, shell=True)
        fout.close()
        
        rows = [i.split()[2:] for i in open(outputtxt, 'r') if "Bounding" in i]
        box = [i.strip(',') for i in rows[0]]
        minx = float(box[0])
        miny = float(box[1])
        maxx = float(box[2])
        maxy = float(box[3])

        ######################################################

        g = gdal.Open(NdviImage)
        lasfile = file.File(oldlasfile, mode='r')
        newlas = file.File(newlasfile, mode='w', header=h)
        #######################################################
        ndviband = g.ReadAsArray()
        ndviband = np.array(ndviband, dtype=float)
        m = len(ndviband)  # y axe len
        n = len(ndviband[0])  # x axe len

        #######################################################
        # print lastotif(2035311.686,525276.565,minx,miny,maxx,maxy,m,n)
        count = 0
        for p in lasfile:
            xy = self.lastotif(p.x, p.y, minx, miny, maxx, maxy, m, n)
            yval = xy[1]
            xval = xy[0]

            if yval <= m and xval <= n and ndviband[yval - 1][xval - 1] < 0.25:
                newlas.write(p)
                count += 1
        print count
        newlas.close()
        
if __name__ == '__main__':
    obj = ndvi()
    obj.vegetation('./data/47758.tif', './data/ndvioutput.tif')
    obj.removevegetation('./data/Only_buildings.las',
                         './data/outputMeanFilterSize_10.las',
                         './data/ndvioutput.tif')