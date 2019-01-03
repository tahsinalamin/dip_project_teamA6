import numpy as np

class Noisy_Image:
  
    def add_gaussian(self, image):
        """default parameters"""
        loc = 0.0
        scale = 15.0
        
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = np.random.normal(loc, scale)
                hist[int(round(value+128))] += 1
                value = image[i, j] + value
                if value > 255.0:
                    value = 255.0
                elif value < 0.0:
                    value = 0.0
                value = int(round(value))
                image[i, j] = value
                
        return image, hist
        
    def add_rayleigh(self, image):
        """default parameters"""
        loc = 0.0
        scale = 20.0
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = np.random.normal(loc, scale)
                value2 = np.random.normal(loc, scale)
                value3 = (value**2 + value2**2)**.5
                hist[int(round(value3))] += 1
                value4 = image[i, j] + value3
                if value4 > 255.0:
                    value4 = 255.0
                elif value4 < 0.0:
                    value4 = 0.0
                value4 = int(round(value4))
                image[i, j] = value4
        return image, hist
        
    def add_saltandpepper(self, image):
        """default parameters"""
        chance = .05
        salt_chance = .6
        pepper_chance = 1.0 - salt_chance
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                roll_chance = np.random.random_sample()
                if roll_chance < chance:
                    roll_salt_chance = np.random.random_sample()
                    if roll_salt_chance < salt_chance:
                        image[i, j] = 255
                        hist[255] += 1
                    else:
                        image[i, j] = 0
                        hist[0] += 1
        return image, hist   
    
    def add_uniform(self, image):
        """default parameters"""
        scale = 10.0
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                """ -scale to +scale range"""
                value = (np.random.random_sample() * scale * 2) - scale
                hist[int(round(value+128))] += 1
                value = image[i, j] + value
                if value > 255.0:
                    value = 255.0
                elif value < 0.0:
                    value = 0.0
                value = int(round(value))
                image[i, j] = value
        return image, hist   
    
    def add_gamma(self, image):
        shape = 2.0
        scale = 10.0
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = np.random.gamma(shape, scale)
                hist[int(round(value))] += 1
                value = image[i, j] + value
                if value > 255.0:
                    value = 255.0
                elif value < 0.0:
                    value = 0.0
                value = int(round(value))
                image[i, j] = value
        return image, hist   
        
    def add_exponential(self, image):
        scale = 5.0
        hist = list(0 for i in range (0, 256))
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = np.random.exponential(10.0)
                """use np.floor, or else distribution is skewed towards 1 because of rounding interaction"""
                hist[int(round(np.floor(value)))] += 1
                value = image[i, j] + value
                if value > 255.0:
                    value = 255.0
                elif value < 0.0:
                    value = 0.0
                value = int(round(np.floor(value)))
                image[i, j] = value
        return image, hist   