from PIL import Image
from math import ceil, floor
from matplotlib import pyplot as plt


class histogram:

    def __init__(self, ImagePlane, ImageQuery):
        numBins = 32
        Bsize = ceil(255.0 / numBins)  # considering grayscale
        im1 = Image.open(ImagePlane)
        im2 = Image.open(ImageQuery)
        im1 = im1.resize(im2.size, Image.BILINEAR)
        im1 = im1.convert('LA')
        im2 = im2.convert('LA')

        # reading into lists
        data_im1 = [i[0] for i in im1.getdata()]
        data_im2 = [i[0] for i in im2.getdata()]

        # calculate histograms
        im1_bins = self.calcHistogram(data_im1, numBins, Bsize)
        im2_bins = self.calcHistogram(data_im2, numBins, Bsize)
        combined_val = self.calcHistogram(data_im1 + data_im2, numBins, Bsize)

        # plot histograms
        plt.figure(1)
        plt.bar(range(32), im1_bins)
        plt.show()
        # plt.savefig('./data/histogram_image1.png')

        plt.figure(2)
        plt.bar(range(32), im2_bins)
        plt.show()
        # plt.savefig('./data/histogram_image2.png')

        plt.figure(3)
        plt.bar(range(32), combined_val)
        plt.show()
    # plt.savefig('./data/histogram_imageCombined.png')
    # print(im1_bins, im2_bins)

    def calcHistogram(self, seq, numBuckets, Bsize):
        hist_list = [0] * numBuckets
        for pnt in seq:
            hist_list[int(floor(pnt / Bsize))] += 1
        return hist_list


obj = histogram('./data/planerized.png', './data/westcott/westcott2.png')