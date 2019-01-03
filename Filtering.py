import numpy as np
import cv2
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

class Filtering:
    image = None
    filter = None
    cutoff = None
    order = None

    def __init__(self, image):
        self.image = image
        #self.filter_name = filter_name

    ############################# Mean filters ##############################################

    def arithmatic_mean_filter(self, image, window_size, order):
        """The idea of mean filtering is simply to replace each pixel value in an image with the mean (`average')
        value of its neighbors, including itself.
        This has the effect of eliminating pixel values which are unrepresentative of their surroundings.
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        f(x,y) = (1/(m*n)) * sum(g(s,t))
        """

        # window_size = [3, 3]  ##by default
        print("Arithmatic mean filter called")

        m = window_size[0]
        n = window_size[1]
        # print(m, n)
        new_image = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        # print(image)
        # print("--------------------------------------")

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                # print("----")
                # print(i,j)
                average_value = 0
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = image[s, t]
                        # print(s,t,"=",image_val)
                        average_value = average_value + image_val
                new_image[i, j] = average_value / (m * n)

        # print(new_image[40,50])
        # print(new_image)
        return new_image

    def geometric_mean_filter(self, image, window_size, order):
        """
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        f(x,y) = (mul(g(s,t)))^(1/mn)
        """
        # window_size = [3, 3]  ##by default
        print("Geometric mean filter called")
        # print(order)

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        # print(image)
        # print("----------------")
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                # print("----")
                # print(i,j)
                average_value = 1 / 10
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 1 / 10
                        else:
                            image_val = image[s, t] / 10
                        # print(s,t,"=",image_val)
                        average_value = average_value * image_val
                new_image[i, j] = int(int(average_value * 10 ** (m * n)) ** (1 / (m * n)))
                # print(new_image[i,j])

        return new_image

    def harmonic_mean_filter(self, image, window_size, order):
        """
            window size can be square like 3 X 3, 5 X 5, by default 3 X 3
            f(x,y) = mn/(sum(1/g(s,t)))
        """
        # window_size = [3, 3]  ##by default
        print("Harmonic mean filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                # print("----")
                # print(i,j)
                average_value = 0
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1] or image[s,t]==0:
                            image_val = 1
                        else:
                            image_val = image[s, t]
                        # print(s,t,"=",image_val)
                        average_value = average_value + (1 / image_val)
                        # print(average_value)
                new_image[i, j] = (m * n) / average_value
        # print(new_image)
        return new_image

    def contraharmoic_mean_filter(self, image, window_size, order):
        """f(x,y)= (sum(g(s,t)^(q+1))/(g(s,t)^q)
        q = order, by default 1, can be negative
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        # window_size = [3, 3]  ##by default
        # order = -1
        print("Contraharmonic mean filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                # print("----")
                # print(i,j)
                average_value = 0
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1] or image[s,t]==0:
                            image_val = 1
                        else:
                            image_val = float(image[s, t])
                        # print(s,t,"=",image_val)
                        average_value = average_value + (image_val ** (order + 1)) / (image_val ** order)
                        # print(average_value)
                new_image[i, j] = int(average_value)
        # print(new_image)

        return new_image

    def choose_mean_filter(self, image, filter_number, window_size):
        """A function that identifies which mean filter (arithmetic, geometric, harmonic) is selected.
        Default is arithmatic
        """
        print("inside choose_mean_filter")
        #order = 1
        if filter_number == 12:
            filtered_image = self.geometric_mean_filter(image, window_size, order = 0)
        elif filter_number == 13:
            filtered_image = self.harmonic_mean_filter(image, window_size, order = 0)
        elif filter_number == 14:
            filtered_image = self.contraharmoic_mean_filter( image, window_size, order = 2)
        else:
            filtered_image = self.arithmatic_mean_filter( image, window_size, order = 0)

        return filtered_image

    ############################# Order Statistic Filters #################################
    def median_filter(self, image, window_size):
        """
        f(x,y) = (1/(m*n-d))*sum(gr(s,t))
        We delete the / 2 lowest and the / 2 highest intensity values of g(s,t).
        gr(s,t) represent the remaining mn-d pixels.
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        #window_size = [3, 3]  ##by default
        d = 4  ##by deafult
        print("Midpoint Order statistic filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                gr = []
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = image[s, t]
                        gr.append(image_val)
                gr = sorted(gr)
                gr = gr[int(len(gr) / 2)]
                new_image[i, j] = gr
        # print(new_image)
        return new_image

    def max_filter(self, image, window_size):
        """
        f(x,y) = max(g(s,t))
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        #window_size = [3, 3]  ##by default
        print("Midpoint Order statistic filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                max_value = -9999
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = int(image[s, t])
                        if max_value < image_val:
                            max_value = image_val
                new_image[i, j] = max_value
        # print(new_image)
        return new_image

    def min_filter(self, image, window_size):
        """
        f(x,y) = max(g(s,t))
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        #window_size = [3, 3]  ##by default
        print("Midpoint Order statistic filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                min_value = 9999
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = int(image[s, t])
                        if min_value > image_val:
                            min_value = image_val
                new_image[i, j] = min_value
        # print(new_image)
        return new_image

    def midpoint_filter(self, image, window_size):
        """
        f(x,y) = (1/2)*[max{g(s,t)}+min{g(s,t)}]
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        window_size = [3, 3]  ##by default
        print("Midpoint Order statistic filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                max_value = -9999
                min_value = 9999
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = float(image[s, t])
                        if max_value < image_val:
                            max_value = image_val
                        if min_value > image_val:
                            min_value = image_val
                new_image[i, j] = int(0.5 * (max_value + min_value))
        # print(new_image)
        return new_image

    def alpha_trimmed_mean_filter(self, image, window_size):
        """
        f(x,y) = (1/(m*n-d))*sum(gr(s,t))
        We delete the / 2 lowest and the / 2 highest intensity values of g(s,t).
        gr(s,t) represent the remaining mn-d pixels.
        window size can be square like 3 X 3, 5 X 5, by default 3 X 3
        """
        window_size = [3, 3]  ##by default
        d = 4  ##by deafult
        print("Midpoint Order statistic filter called")

        m = window_size[0]
        n = window_size[1]

        new_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                sum_gr = 0
                gr = []
                for s in range(i - math.floor(m / 2), i + math.ceil(m / 2)):
                    for t in range(j - math.floor(n / 2), j + math.ceil(n / 2)):
                        if s < 0 or t < 0 or s >= image.shape[0] or t >= image.shape[1]:
                            image_val = 0
                        else:
                            image_val = image[s, t]
                        gr.append(image_val)
                gr = sorted(gr)
                gr = gr[int(d / 2):int(len(gr) - d / 2)]
                sum_gr = sum(gr)
                new_image[i, j] = int((1 / ((m * n) - d)) * sum_gr)
        # print(new_image)
        return new_image

    def choose_order_statistic_filter(self, image, filter_number, window_size):
        """
        A function that identifies which order-statistic filter (median, max, min, midpoint, alpha-trimmed) is selected.
        Default is median
        """

        if filter_number == 24:
            filtered_image = self.midpoint_filter(image, window_size)
        elif filter_number == 25:
            filtered_image = self.alpha_trimmed_mean_filter(image, window_size)
        elif filter_number == 23:
            filtered_image = self.min_filter(image, window_size)
        elif filter_number == 22:
            filtered_image = self.max_filter(image, window_size)
        else:
            filtered_image = self.median_filter(image, window_size)

        return filtered_image

    ############################## Adaptive Filters #######################################
    def adatptive_local_filter(self, image, window_size, noise_variance):
        nh = window_size[0]
        nv = noise_variance
        b = np.floor(nh / 2)
        finalImage = np.zeros(image.shape)

        for i in range(int(b), int(image.shape[0] - 2 * b + 1)):
            for j in range(int(b), int(image.shape[1] - 2 * b + 1)):
                sum = 0
                sumsq = 0

                for ih in range(int(-b), int(b)):
                    for jh in range(int(-b), int(b)):
                        sum += image[i + ih][j + jh]
                        sumsq += pow(image[i + ih][j + jh], 2)
                mean = sum / pow(nh, 2)
                variance = (sumsq / pow(nh, 2)) - pow(mean, 2)
                alpha = nv / variance
                if (alpha > 1.0):
                    alpha = 1.0
                finalImage[i][j] = (1 - alpha) * (image[i][j]) + (alpha * mean)
        finalfinalImage = finalImage.astype(int)
        return finalfinalImage
        #return finalfinalImage

    def adaptive_median_filter(self, image, window_size, noise_variance):
        nh = window_size[0]
        nv = noise_variance
        b = np.floor(nh / 2)
        finalImage = np.zeros(image.shape)

        for i in range(int(b), int(image.shape[0] - 2 * b + 1)):
            for j in range(int(b), int(image.shape[1] - 2 * b + 1)):
                z = []
                for ih in range(int(-b), int(b)):
                    for jh in range(int(-b), int(b)):
                        z.append(image[i + ih][j + jh])
                A1 = np.median(z) - np.min(z)
                A2 = np.median(z) - np.max(z)
                if A1 > 0 > A2:
                    B1 = image[i][j] - np.min(z)
                    B2 = image[i][j] - np.max(z)
                    if B1 > 0 > B2:
                        finalImage[i][j] = image[i][j]
                    else:
                        finalImage[i][j] = np.median(z)
                else:
                    nh += nh
                    if nh > 7:
                        finalImage[i][j] = np.median(z)

        return finalImage




    def choose_adaptive_filter(self, image, filter_number, window_size, noise_variance):
        """
        A function that identifies which order-statistic filter (median, max, min, midpoint, alpha-trimmed) is selected.
        Default is median
        """

        if filter_number == 32:
            filtered_image = self.adaptive_median_filter(image, window_size, noise_variance)
        else:
            filtered_image = self.adatptive_local_filter(image, window_size, noise_variance)

        return filtered_image

    ############################## choose which filter ############################################

    def choose_filter(self, image, filter_number, filter_selection, window_selection, noise_variance):
        """A function that identifies which mean filter (arithmetic, geometric, harmonic) is selected.
        Default is arithmatic
        """
        print("inside choose filter of filtering.py")
        #print(filter_selection, window_selection)
        #####select the window_size
        if window_selection == 1077:
            window_size = [7, 7]
        elif window_selection == 1055:
            window_size = [5, 5]
        else:
            window_size = [3, 3]  ##default is 3 X 3

        #noise_variance = 500

        ####select the filter types####

        if filter_selection == 'mean':
            final_filter_image = self.choose_mean_filter(image, filter_number, window_size)
        elif filter_selection == 'order':
            final_filter_image = self.choose_order_statistic_filter(image, filter_number, window_size)
        else:
            final_filter_image = self.choose_adaptive_filter(image, filter_number, window_size, noise_variance)


        #output_image_name =  str(filter_number) + "_order_statistic_filter" + ".jpg"
        #cv2.imwrite(output_image_name, final_filter_image)

        return final_filter_image

