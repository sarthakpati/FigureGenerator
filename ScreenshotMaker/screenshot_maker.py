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
    def __init__(self, images, masks=None, slice_numbers=None, mask_opacity=100, border_pc=0.05):

        # change comma-separated string to list for images and masks
        self.images = images.split(",")
        assert len(images) > 0, "Please provide at least one image."
        if masks is not None:
            self.masks = masks.split(",")
        else:
            self.masks = None
        self.slice_numbers = slice_numbers
        self.mask_opacity = mask_opacity
        self.border_pc = border_pc

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

        if self.masks is not None:
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
            sitk.GetArrayFromImage(image)[bounding_box[0] : bounding_box[1], bounding_box[2] : bounding_box[3], bounding_box[4] : bounding_box[5]]
            for image in input_images
        ]

        if self.masks is not None:
            input_mask_array = [
                sitk.GetArrayFromImage(image)[bounding_box[0] : bounding_box[1], bounding_box[2] : bounding_box[3], bounding_box[4] : bounding_box[5]]
                for image in input_masks
            ]
        else:
            input_mask_array = None

        test = 1

    def save_screenshot(self, filename):
        # save the screenshot to a file
        test = 1
