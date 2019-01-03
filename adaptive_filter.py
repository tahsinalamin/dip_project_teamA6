import numpy as np
import cv2
import statistics


def adaptive_filter(image, nh, nv):
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
            if(alpha > 1.0):
                alpha = 1.0
            finalImage[i][j] = (1 - alpha) * (image[i][j]) + (alpha * mean)
    # finalfinalImage = finalImage.astype(int)
    return finalImage

def adaptive_median_filter(image, nh):
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
                    finalImage[i][j] = statistics.median(z)
    return finalImage

def main():
    image = cv2.imread("Lenna0.jpg", 0)
    # fImage = adaptive_filter(image, 5, 50000)           #First parameter is image, second is window size, third is noise variance.
                                                        #Suggested  value for noise variance is around 50,000
    fImage2 = adaptive_median_filter(image, 3)

    cv2.imwrite('final.png', fImage2)


if __name__ == "__main__":
    main()