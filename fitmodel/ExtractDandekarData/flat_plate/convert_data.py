# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 22:49:17 2013

@author: Yuxiang Wang
"""


import numpy as np
import matplotlib.pyplot as plt


def main():
    dandekar_data = []
    for i in range(4):
        rawdata = np.genfromtxt('subject'+str(i+1)+'.csv', delimiter=',')
        frame_pixels = rawdata[:4]
        frame_coords = rawdata[4:8]
        pts_pixels = rawdata[8:]
        # Calibrate the pixel to scale to value
        origin_pixel, param = calibrate(frame_pixels, frame_coords)
        # Calculate the actual data points
        pts_coords = convert(pts_pixels, origin_pixel, param)
        # Plot to check result
        plt.plot(pts_coords[:, 0], pts_coords[:, 1], '.--k')
        dandekar_data.extend(pts_coords)
    np.savetxt('dandekar_data.csv', np.array(dandekar_data), delimiter=',')


def calibrate(frame_pixels, frame_coords):
    origin_pixel = frame_pixels[0]
    oa = frame_coords[3] - frame_coords[0]
    oc = frame_coords[1] - frame_coords[0]
    OA = frame_pixels[3] - frame_pixels[0]
    OC = frame_pixels[1] - frame_pixels[0]
    xscale = np.linalg.norm(oc) / np.linalg.norm(OC)
    yscale = np.linalg.norm(oa) / np.linalg.norm(OA)
    return (origin_pixel, np.array((xscale, yscale)))


def convert(pts_pixels, origin_pixel, param):
    pts_coords = np.empty_like(pts_pixels)
    for (i, pts_pixel) in enumerate(pts_pixels):
        pts_coords[i] = np.abs(pts_pixel - origin_pixel) * param
    return pts_coords


if __name__ == '__main__':
    main()
