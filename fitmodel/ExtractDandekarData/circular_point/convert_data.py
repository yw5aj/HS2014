# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 22:49:17 2013

@author: Yuxiang Wang
"""


import numpy as np
import matplotlib.pyplot as plt


def main():
    dandekar_data_circular = []
    dandekar_data_point = []
    for i in range(4):
        rawdata = np.genfromtxt('subject'+str(i+1)+'.csv', delimiter=',')
        frame_pixels = rawdata[:4]
        frame_coords = rawdata[4:8]
        circular_pts_pixels = rawdata[8:15]
        point_pts_pixels = rawdata[15:]
        # Calibrate the pixel to scale to value
        origin_pixel, param = calibrate(frame_pixels, frame_coords)
        # Calculate the actual data points
        circular_pts_coords = convert(circular_pts_pixels, origin_pixel, param)
        point_pts_coords = convert(point_pts_pixels, origin_pixel, param)
        # Plot to check result
        fig, axs = plt.subplots(1, 1)
        axs.plot(circular_pts_coords[:, 0], circular_pts_coords[:, 1], '.--b')
        axs.plot(point_pts_coords[:, 0], point_pts_coords[:, 1], '.--r')
        dandekar_data_circular.extend(circular_pts_coords)
        dandekar_data_point.extend(point_pts_coords)
    np.savetxt('dandekar_data_circular.csv', np.array(dandekar_data_circular), delimiter=',')
    np.savetxt('dandekar_data_point.csv', np.array(dandekar_data_point), delimiter=',')


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
