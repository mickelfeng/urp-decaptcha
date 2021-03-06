# -*- coding: utf-8 -*-

import numpy
import cv2
from segmentation import region_from_segment

FEATURE_DATATYPE = numpy.float32


class FeatureExtractor(object):
    '''
    given a list of segments, returns a list of feature vectors
    '''
    def extract(self, image, segments):
        raise NotImplementedError()


class SimpleFeatureExtractor(FeatureExtractor):
    def __init__(self, feature_size=10, stretch=False):
        self.feature_size = feature_size
        self.stretch = stretch

    def extract(self, image, segments):
        fs = self.feature_size
        bg = 255
        regions = numpy.ndarray(shape=(0, fs), dtype=FEATURE_DATATYPE)

        for segment in segments:
            region = region_from_segment(image, segment)

            if self.stretch:
                region = cv2.resize(region, (fs, fs))
            else:
                x, y, w, h = segment
                proportion = float(min(h, w)) / max(w, h)
                new_size = (fs, int(fs * proportion)) if min(w, h) == h else (int(fs * proportion), fs)

                region = cv2.resize(region, new_size)
                s = region.shape
                new_region = numpy.ndarray((fs, fs), dtype=region.dtype)
                new_region[:, :] = bg
                new_region[:s[0], :s[1]] = region
                region = new_region

            regions = numpy.append(regions, region, axis=0)
        regions.shape = (len(segments), fs**2)

        return regions
