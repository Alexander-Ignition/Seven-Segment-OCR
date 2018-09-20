import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt


class cutDigits:
    def __init__(self, image=None, src_file_name=None, dst_folder_name=None, return_image=False, last_digit=3, labels=None):
        """
        The aim of this class is to extract digits from the frame-only preprocessed image.
        We to delimit digits by bounding boxes.
        We tried several approaches, but we present here the most successful one, a "dummy" yet efficient approach.
        :param image: RGB image (numpy array NxMx3) of a SLICED SCREEN. If image is None, the image will be extracted from src_filename
        :param src_file_name: filename of a SLICED SCREEN to load the source image (e.g. HQ_digital_preprocessing/0a07d2cff5beb0580bca191427e8cd6e1a0eb678.jpg)
        :param image:

        """
        if image is None :
            self.image = cv2.imread(src_file_name)
        else:
            self.image = image
        self.src_file_name = src_file_name
        self.dst_folder_name = dst_folder_name
        self.return_image = return_image
        self.last_digit=last_digit
        self.labels = labels

        self.box_size = None
        self.boxes = []



    #TODO : modifier le commentaire
    def get_bounding_box_dummy(self):
        """
        1st approach : dummy approach
        Get the bounding box considering that the comma is at 8/13 of the image
        and dividing the area by 4 before the detected comma

        :param ppc_img : the preprocessed image (output of a preprocess fct) ie the exctracted screen + constrats
        :return dist : the distance between each cut (used after in the cut_and_affect_to_folder ) ie the size of the bounding boxes
        plots the image with the computed cuts

        Creates bounding boxes and put each box in the folder corresponding to its label
    preprocessed_img : preprocessed image is after exctarcted dark screen + contrasts

        :param dist: the dist between each cuts, ie the width of each bounding boxes (same widths), output of the 'get_bd_dummy' function
        :param labels: list of int of size 4, 10 labels : from '0' to '9' and 'X' if nothing of the digits BEFORE the COMMA
        :param digits_path: string, the output path to save the bounding boxes in.
                Of the form "Datasets_digits/" and contains the '0', '1', ... 'X' folders
                The image reduced to its bounding box is saved into the folder corresdponding to its label

        :param ind: the ID of the image 'o8sdf7ksqjdh.jpg'
        :param last_digit: int, optional.
                  If 2, we only save the 3 last digits before the comma (without the unity digit)
                  If 3, we save all digits before the comma
        :return:
        """

        self.boxes = []
        self.box_size = self.image.shape[1]/4

        for i in range(self.last_digit):
            inf = i * self.box_size
            sup = (i+1) * self.box_size
            self.boxes += [self.image[:, int(inf):int(sup)]]


    # TODO : modifier le commentaire
    def save_to_folder(self) :
        """
        :return:
        """
        if self.dst_folder_name is None :
            return

        for i in range(len(self.boxes)):
            if self.labels :
                box = self.boxes[i]
                label = self.labels[i]

                file_name = self.src_file_name.split('/')[-1].split('.')[0]
                dst_file_name = self.dst_folder_name + "/" \
                                + file_name \
                                + "_label_" + str(label) \
                                + "_position_" + str(i) \
                                + '.jpg'

                cv2.imwrite(dst_file_name, box)

            else :
                box = self.boxes[i]

                file_name = self.src_file_name.split('/')[-1].split('.')[0]
                dst_file_name = self.dst_folder_name + "/" \
                                + file_name \
                                + "_label_no_" + \
                                + "_position_" + str(i) \
                                + '.jpg'

                cv2.imwrite(dst_file_name, box)







"""
A main function to cut the digits on all images.
"""

if __name__ == "main":


    # ---- INITIALISATION ----

    # eleven folder 'Datasets'
    raw_dir = "Datasets_raw/"

    # may be HQ_digital, MQ_digital or LQ_digital
    cat_dir =  "LQ_digital"

    # path to Sacha's output, with the extracted screen
    preprocessed_dir = "Datasets_preprocessed/"+ cat_dir +"_preprocessing/"

    all_images = os.listdir(raw_dir + cat_dir)
    all_images_preprocessed = os.listdir(preprocessed_dir)

    # output path to save individual digits in
    # of the form "Datasets_digits/" and contains the '0', '1', ... 'X' folders
    digits_path = "Datasets_digits/"

    # Csv file with the image name, 'cadran_1', 'cadran_2', 'cadran_3', 'cadran_4' columns containing the digits' labels before the comma
    labels_path = "Datasets_labels/"+cat_dir+".csv"

    # convert file into dataframe
    labels_df   = csv_labels_to_df(labels_path)

    # ---- LOOP ----

    for ind in all_images_preprocessed:
        if ind != ".DS_Store":
            print(ind)
            image = cv2.imread(preprocessed_dir + ind)                  # get the extracted screen from img
            #warped = extract_screen(image)
            preprocessed_img = preprocess2(image)                       # preprocess the img
            dist = get_bd_dummy(preprocessed)                           # get bounding boxes' size

            # get the labels of the digits before the comma
            labels = labels_df[labels_df['image'] == ind][['cadran_1', 'cadran_2', 'cadran_3', 'cadran_4']].values

            # get bounding boxes and save truncated images in the folder corresponding to its label
            cut_and_affect_to_folder(preprocessed_img, dist, labels[0], \
                                     digits_path, ind, last_digit= 2)
            plt.close()



# DECOMMENT IF IMAGES NOT PREPROCESSED ALREADY
'''for ind in all_images:
    print(ind)
    image = cv2.imread(input_dir + ind)
    warped = extract_screen(image)
    preprocessed = preprocess_short(warped)
    dist = get_bd_short_wo_comma(preprocessed)
    preprocessed_img = warped
    labels = labels_df[labels_df['image'] == ind][['cadran_1', 'cadran_2', 'cadran_3', 'cadran_4']].values
    affect_to_folder(preprocessed_img, dist, labels[0], digits_path, ind)

    #plt.savefig(output_dir + "bd_plot_" + ind)
    plt.close()'''