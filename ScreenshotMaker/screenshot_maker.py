#!usr/bin/env python
# -*- coding: utf-8 -*-
from SimpleITK.SimpleITK import GetArrayFromImage
from .utils import (
    sanity_checker_base,
    resample_image,
    rescale_intensity,
    get_bounding_box,
)
import SimpleITK as sitk


class ScreenShotMaker:
    def __init__(self, args):
        # change comma-separated string to list for images and masks
        self.images = args.images.split(",")
        assert len(args.images) > 0, "Please provide at least one image."
        self.mask_present = False
        if args.masks is not None:
            self.masks = args.masks.split(",")
            self.mask_present = True
        else:
            self.masks = None
        
        # initialize members
        self.slice_numbers = args.slice
        self.mask_opacity = args.mask_opacity
        self.border_pc = args.borderpc
        self.colormap = args.colormap
        self.axis_row = args.axis_row

        ## sanity checker
        # read the first image and save that for comparison
        file_reader_base = sitk.ImageFileReader()
        file_reader_base.SetFileName(self.images[0])
        file_reader_base.ReadImageInformation()

        if sanity_checker_base(file_reader_base, self.images[1:]):
            # only check masks if sanity check for images passes
            sanity_checker_base(file_reader_base, self.masks)

    def make_screenshot(self):
        # make the screenshot
        # try one of the following:
        # - https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1LabelMapOverlayImageFilter.html
        # - https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1LabelOverlayImageFilter.html -- seems to be more appropriate
        # - https://github.com/SimpleITK/NIH2019_COURSE/blob/master/09_results_visualization.ipynb

        input_images = [
            rescale_intensity(resample_image(sitk.ReadImage(image)))
            for image in self.images
        ]

        if self.mask_present:
            input_masks = [
                resample_image(
                    sitk.ReadImage(mask), interpolator=sitk.sitkNearestNeighbor
                )
                for mask in self.masks
            ]
        else:
            input_masks = None

        bounding_box = get_bounding_box(input_images[0], input_masks, self.border_pc)
        print(bounding_box)

        # get the bounded image and masks in the form of arrays
        input_images_array = [
            sitk.GetArrayFromImage(image)[
                bounding_box[0] : bounding_box[1],
                bounding_box[2] : bounding_box[3],
                bounding_box[4] : bounding_box[5],
            ]
            for image in input_images
        ]

        if self.mask_present:
            input_mask_array = [
                sitk.GetArrayFromImage(image)[
                    bounding_box[0] : bounding_box[1],
                    bounding_box[2] : bounding_box[3],
                    bounding_box[4] : bounding_box[5],
                ]
                for image in input_masks
            ]
        else:
            input_mask_array = None

        test = 1

    def save_screenshot(self, filename):
        # save the screenshot to a file
        test = 1
