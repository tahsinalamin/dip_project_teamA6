"""
WARNING: File dialog sometimes freezes computer! If I could find a better way to open a file, I would have used it.
Please be aware of this as you run this code
"""

import tkinter
import PIL
from PIL import Image, ImageTk
from tkinter import filedialog, IntVar, simpledialog, messagebox

import numpy as np
import cv2
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys
from Filtering import Filtering
from Noisy_Image import Noisy_Image

class GUI_Restoration:
    def image_browse(self):
        """Function browses for an image, resizes it and displays it on the canvas.
        Also adds buttons for noise and histogram"""

        #self.master.withdraw() # Makes the main window disappear
        imageName = filedialog.askopenfilename(title="Select an image",
                                               filetypes=(("JPEG Files", ("*.jpg", "*.jpeg")),
                                                          ("PNG Files", "*.png"),
                                                          ("Bitmap Files", "*.bmp"),
                                                          ("GIF Files", ".gif"),
                                                          ("TIFF Files", ("*.tif", "*.tiff")),))

        self.image = Image.open(imageName).convert('L') # Saves as PIL image. Can convert to numpy array later
        self.input_image = np.array(self.image) ##convert the image to an array
        self.displayImg = ImageTk.PhotoImage(self.image.resize((self.c_size[0], self.c_size[1]), Image.ANTIALIAS))
        self.canvas.delete(tkinter.ALL)
        self.canvas.create_image(((self.c_size[0]/2) + 2 + self.border_size), ((self.c_size[1]/2) + 2 + self.border_size),
                                 anchor=tkinter.CENTER, image=self.displayImg, tags="displayImage")

        """--------------------------------------------------Adds New Buttons--------------------------------------------------------------"""

        frame2 = tkinter.Frame(self.master, pady=10)
        tkinter.Button(frame2, text="Add a noise", command=self.add_a_noise, fg="white", bg="black").pack()
        self.noise_var.set("Gaussian")
        self.noise_dropdown = tkinter.OptionMenu(frame2, self.noise_var, "Gaussian", "Rayleigh", "Gamma", "Exponential", "Uniform", "Salt and Pepper")
        self.noise_dropdown.pack()
        frame2.grid(row=3)

        frame3 = tkinter.Frame(self.master, pady=10)
        tkinter.Button(frame3, text="Compute Histogram", command=self.compute_histogram, fg="white", bg="black").pack()
        frame3.grid(row=4)

        frame4 = tkinter.Frame(self.master, pady=7)
        tkinter.Button(frame4, text="Apply a filter", command=self.apply_filters, fg="white", bg="black").pack()
        frame4.grid(row=5)

        frame5 = tkinter.Frame(self.master, pady=5)
        self.circleToggle = tkinter.Checkbutton(frame5, text="Toggle Selection Circles", command=self.add_histocircles, variable=self.var)
        self.circleToggle.pack()
        frame5.grid(row=6)

        #Update and deiconify update the wondow and make it reappear
        self.master.update()
        self.master.deiconify()

        self.flag_hist = 0 ##if histogram is already created, 0=no

    def add_histocircles(self):
        if(self.var.get() == 1):
            # Creating circles and binding them to events
            self.point1_cir = self.canvas.create_oval(80, 80, 100, 100, fill="blue", tags="pointx")
            self.point2_cir = self.canvas.create_oval(200, 200, 220, 220, fill="green", tags="pointy")
            self.canvas.tag_bind('pointx', '<Button-1>', self.find_point1)
            self.canvas.tag_bind('pointx', '<B1-Motion>', self.find_point1)
            self.canvas.tag_bind('pointy', '<Button-3>', self.find_point2)
            self.canvas.tag_bind('pointy', '<B3-Motion>', self.find_point2)
        else:
            self.canvas.delete(self.point1_cir)
            self.canvas.delete(self.point2_cir)

    def add_a_noise(self):
        print("Adding a noise...")

        """type = tkinter.simpledialog.askstring("Input", "What type of noise to add? Options are Gaussian, Rayleigh, Salt and Pepper, Gamma, Uniform, Exponential")"""
        type = self.noise_var.get()
        ans = messagebox.askokcancel("Question", "Confirm if you want to add %s noise?" % type)
        
        if not ans:
            messagebox.showinfo("Information", "Not adding any noise!")
            return
        

        myobj = Noisy_Image()
        if type in ['gaussian','gauss','Gaussian','Gauss']:
            noisyimage, noisyhist = myobj.add_gaussian(self.input_image)
            print('Added gaussian noise to image')
        elif type in ['rayleigh','Rayleigh', 'ray', 'Ray']:
            noisyimage, noisyhist = myobj.add_rayleigh(self.input_image)
            print('Added rayleigh noise to image')
        elif type in ['saltandpepper','salt and pepper','Salt and Pepper', 'Salt And Pepper']:
            noisyimage, noisyhist = myobj.add_saltandpepper(self.input_image)
            print('Added salt and pepper noise to image')
        elif type in ['gamma','Gamma']:
            noisyimage, noisyhist = myobj.add_gamma(self.input_image)
            print('Added gamma noise to image')    
        elif type in ['uniform','Uniform']:
            noisyimage, noisyhist = myobj.add_uniform(self.input_image)
            print('Added uniform noise to image')   
        elif type in ['exp','exponential', 'Exp', 'Exponential']:
            noisyimage, noisyhist = myobj.add_exponential(self.input_image)
            print('Added exponential noise to image')  
        else:
            print('Noise type not found or implemented')
            noisyimage = self.input_image
            noisyhist = list(0 for i in range(0, 256))

        """display the noisy hist"""
        fig = Figure(figsize=(4,4),dpi=100)
        fig.suptitle('Noise Histogram', fontsize=20)
        plt = fig.add_subplot(111)
        
        if type in ['gaussian','gauss','Gaussian','Gauss', 'uniform', 'Uniform']:
            plt.plot([i for i in range(-128, 128)], noisyhist)
        else:
            plt.plot(noisyhist)
            if type not in ['saltandpepper','salt and pepper','Salt and Pepper', 'Salt And Pepper']:
                plt.set_xlim([-5, 130])
            
        if self.flag_hist == 1:
            self.canvas_hist.get_tk_widget().destroy()
        self.canvas_hist = FigureCanvasTkAgg (fig, self.master)
        self.canvas_hist.show()
        self.canvas_hist.get_tk_widget().grid(row=2,column=1)
        self.flag_hist = 1
        
        """noisyimage = myobj.add_rayleigh(self.input_image)"""

        """save noisy image array"""
        self.input_image = noisyimage

        """update the displayed image"""
        nnnimage = Image.fromarray(noisyimage)
        self.displayImg = ImageTk.PhotoImage(nnnimage.resize((self.c_size[0], self.c_size[1]), Image.ANTIALIAS))
        self.canvas.delete(tkinter.ALL)
        self.canvas.create_image(((self.c_size[0]/2) + 2 + self.border_size), ((self.c_size[1]/2) + 2 + self.border_size),
                                 anchor=tkinter.CENTER, image=self.displayImg)

        """cv2.namedWindow('Noise Lenna')
        cv2.imshow('Noise', noisyimage)
        cv2.waitKey(0)"""
        messagebox.showinfo("Information", "Added %s noise! Displaying %s noise histogram." % (type, type))


    def compute_histogram(self):
        """computes the histogram of the given image
        """
        #print("Goodbye World!")
        #img_array = np.array(image)
        use_selected_area = tkinter.messagebox.askyesno('Question', 'Do you want to use the selected area instead of the whole image to compute the histogram?')

        """assume user - point 1 is top left ; point 2 is bottom right"""

        if use_selected_area:
            scale_x = self.input_image.shape[0] / self.c_size[0]
            scale_y = self.input_image.shape[1] / self.c_size[1]

            i_min = int(round(self.point1_x * scale_x))
            i_max = int(round(self.point2_x * scale_x))
            j_min = int(round(self.point1_y * scale_y))
            j_max = int(round(self.point2_y * scale_y))
            print("Using selected area: (%d, %d) : (%d, %d)" % (self.point1_x, self.point1_y, self.point2_x, self.point2_y))
        else:
            i_min = 0
            i_max = self.input_image.shape[0]
            j_min = 0
            j_max = self.input_image.shape[1]
            print("image shape = ", self.input_image.shape)

        hist = list(0 for i in range(0, 256))

        for i in range(i_min, i_max):
            for j in range(j_min, j_max):
                pixel = self.input_image[i, j]
                hist[pixel] = hist[pixel] + 1
                

        """ copy incase something went wrong
        for i in range(0, self.input_image.shape[0]):
            for j in range(0, self.input_image.shape[1]):
                pixel = self.input_image[i, j]
                hist[pixel] = hist[pixel] + 1"""

        #text_histogram = tkinter.Label(self.master, text="Histogram", font=("Helvetica", 10)).grid(row=1,column =1)
        fig = Figure(figsize=(4,4),dpi=100)
        plt = fig.add_subplot(111)
        plt.plot(hist)
        if self.flag_hist == 1:
            self.canvas_hist.get_tk_widget().destroy()
        self.canvas_hist = FigureCanvasTkAgg (fig, self.master)
        self.canvas_hist.show()
        self.canvas_hist.get_tk_widget().grid(row=2,column=1)
        self.flag_hist = 1


    def apply_filters(self):
        """A function that shows the 3 types of filters and lets user decide to choose one filter"""
        print("Hello World 2!")
        #frame4_1.grid_forget()
        if self.flag_hist == 1:
            self.canvas_hist.get_tk_widget().destroy()

        self.frame4_0 = tkinter.Frame(self.master, pady=10)

        tkinter.Label(self.frame4_0, text="Please Select a Filter", font=("Helvetica", 10)).pack()
        self.string_var.set("Mean Filters")
        self.dropdown = tkinter.OptionMenu(self.frame4_0, self.string_var, "Mean Filters", "Order-Statistic Filters", "Adaptive Filters")
        self.dropdown.pack()
        tkinter.Button(self.frame4_0, text="Confirm", command=self.apply_sub_filters, fg="black", bg="white").pack()
        self.frame4_0.grid(row=2, column = 1)
        #print(frame4_1.grid(row=2, column = 1))


    def apply_sub_filters(self):
        """A function that shows the 4 types of mean filters and lets user decide to choose one filter"""
        #self.frame4_1.grid_forget(
        self.main_selection = self.string_var.get()
        print("you selected = ", self.main_selection)

        if self.main_selection == "Mean Filters":
            self.frame4_0.destroy()
            self.frame4_0 = tkinter.Frame(self.master, pady=10)
            tkinter.Label(self.frame4_0, text="Select Mean Filter type", font=("Helvetica", 10)).pack()
            self.string_var.set("Arithmetic Mean Filter")
            self.dropdown = tkinter.OptionMenu(self.frame4_0, self.string_var, "Arithmetic Mean Filter",
                                               "Geometric Mean Filter", "Harmonic Mean Filter", "Contraharmonic Mean Filter")
            self.dropdown.pack()
            tkinter.Button(self.frame4_0, text="Confirm", command=self.select_window_size, fg="black", bg="white").pack()
            self.frame4_0.grid(row=2, column=1)

        elif self.main_selection == "Order-Statistic Filters":
            self.frame4_0.destroy()
            self.frame4_0 = tkinter.Frame(self.master, pady=10)
            tkinter.Label(self.frame4_0, text="Select Order-Statistics Filter type", font=("Helvetica", 10)).pack()
            self.string_var.set("Median Filter")
            self.dropdown = tkinter.OptionMenu(self.frame4_0, self.string_var, "Median Filter",
                                               "Max Filter", "Min Filter",
                                               "Midpoint Filter", "Alpha-trimmed Filter")
            self.dropdown.pack()
            tkinter.Button(self.frame4_0, text="Confirm", command=self.select_window_size, fg="black",
                           bg="white").pack()
            self.frame4_0.grid(row=2, column=1)

        elif self.main_selection == "Adaptive Filters":
            self.frame4_0.destroy()
            self.frame4_0 = tkinter.Frame(self.master, pady=10)
            tkinter.Label(self.frame4_0, text="Select Adaptive Filter type", font=("Helvetica", 10)).pack()
            self.string_var.set("Local Noise Reduction Filter")
            self.dropdown = tkinter.OptionMenu(self.frame4_0, self.string_var, "Local Noise Reduction Filter",
                                               "Adaptive Median Filter")
            self.dropdown.pack()
            tkinter.Button(self.frame4_0, text="Confirm", command=self.select_window_size, fg="black",
                           bg="white").pack()
            self.frame4_0.grid(row=2, column=1)


    def select_window_size(self):
        self.filter_selection = self.string_var.get()
        print("checkbox is = ", self.filter_selection)

        self.frame4_0.destroy()
        self.frame4_0 = tkinter.Frame(self.master, pady=10)
        tkinter.Label(self.frame4_0, text="Select Window Size", font=("Helvetica", 10)).pack()
        self.string_var.set("3 X 3")
        tkinter.OptionMenu(self.frame4_0, self.string_var, "3 X 3",
                                               "5 X 5", "7 X 7").pack()
        tkinter.Button(self.frame4_0, text="Confirm", command=self.call_filters, fg="black", bg="white").pack()
        self.frame4_0.grid(row=2, column=1)

    def call_filters(self):
        print("checkbox is = ", self.filter_selection)
        print("windows size is = ", self.string_var.get())

        noise_variance = 0

        filter_name = ""
        ##selecting the filters
        if self.main_selection == "Adaptive Filters":
            filter_name = 'adaptive'
            noise_variance = tkinter.simpledialog.askinteger("Input",
                                                             "Enter the Noise variance, would suggest values between 50 to 50000")
        elif self.main_selection == "Order-Statistic Filters":
            filter_name = 'order'
        else:
            filter_name = 'mean'

        ##selecting window
        if self.string_var.get() == "7 X 7":
            window_selection = 1077
        elif self.string_var.get() == "5 X 5":
            window_selection = 1055
        else:
            window_selection = 1033

        filter_num = 0
        ##Selecting specific filter
        if self.filter_selection == "Arithmetic Mean Filters":
            filter_num = 11
        elif self.filter_selection == "Geometric Mean Filters":
            filter_num = 12
        elif self.filter_selection == "Harmonic Mean Filters":
            filter_num = 13
        elif self.filter_selection == "Contraharmonic Mean Filters":
            filter_num = 14
        elif self.filter_selection == "Median Filter":
            filter_num = 21
        elif self.filter_selection == "Max Filter":
            filter_num = 22
        elif self.filter_selection == "Min Filters":
            filter_num = 23
        elif self.filter_selection == "Midpoint Filters":
            filter_num = 24
        elif self.filter_selection == "Alpha-trimmed Filters":
            filter_num = 25
        elif self.filter_selection == "Local Noise Reduction Filter":
            filter_num = 31
        elif self.filter_selection == "Adaptive Median Filter":
            filter_num = 32


        print(noise_variance)

        Filter_obj = Filtering(self.input_image)
        output_array = Filter_obj.choose_filter(self.input_image, filter_num, filter_name, window_selection,
                                                noise_variance)

        out_text = self.main_selection + ", " + self.filter_selection + ", " + self.string_var.get()

        print("output array = ", output_array.shape)

        ##show the 2D array as an image
        output_image = PIL.Image.fromarray(output_array)

        self.frame5_1 = tkinter.Frame(self.master, pady=10)
        tkinter.Label(self.frame5_1, text="Filtered Image", font=("Helvetica", 14)).pack()
        self.frame5_1.grid(row=1, column=3)

        self.canvas2 = tkinter.Canvas(self.master, width=self.c_size[0], height=self.c_size[1], relief='solid',
                                      bd=self.border_size)
        self.displayImg2 = ImageTk.PhotoImage(output_image.resize((self.c_size[0], self.c_size[1]), Image.ANTIALIAS))
        # self.canvas2.delete(tkinter.ALL)
        self.canvas2.create_image(((self.c_size[0] / 2) + 2 + self.border_size),
                                  ((self.c_size[1] / 2) + 2 + self.border_size),
                                  anchor=tkinter.CENTER, image=self.displayImg2)
        self.canvas2.grid(row=2, column=3)

        self.out_label = tkinter.Label(self.master, text=out_text, font=("Helvetica", 10))
        self.out_label.grid(row=3, column=3)

        self.frame5 = tkinter.Frame(self.master, pady=5)
        tkinter.Button(self.frame5, text="Start Again", command=self.destroy_all, fg="white", bg="black").pack()
        self.frame5.grid(row=4, column=3)

    def destroy_all(self):
        self.frame4_0.destroy()
        # self.frame4_1.destroy()
        self.out_label.destroy()
        self.frame5.destroy()
        self.frame5_1.destroy()
        self.canvas2.destroy()
        self.canvas.delete(tkinter.ALL)
        self.canvas_hist.get_tk_widget().destroy()
        #self.label_filterimage.

    def find_point1(self, event):
        if(event.x >= 0 and event.x <= 400) and (event.y >= 0 and event.y <= 400): # Set barriers; can change later
            self.point1_x = event.x
            self.point1_y = event.y
            self.canvas.coords(self.point1_cir, self.point1_x - 20, self.point1_y - 20, self.point1_x + 20, self.point1_y + 20)


    def find_point2(self, event):
        if (event.x >= 0 and event.x <= 400) and (event.y >= 0 and event.y <= 400):
            self.point2_x = event.x
            self.point2_y = event.y
            self.canvas.coords(self.point2_cir, self.point2_x - 20, self.point2_y - 20, self.point2_x + 20,
                               self.point2_y + 20)

    def __init__(self, master, var):
        """Used grid to organize widgets in window"""
        self.master = master
        self.master.title("Image Restoration")
        self.c_size = (400, 400)
        self.border_size = 2
        self.point1_cir, self.point2_cir, self.image = None, None, None # Initializing circles
        self.var = var
        self.string_var = tkinter.StringVar(self.master)
        self.dropdown = None
        self.noise_var = tkinter.StringVar(self.master)
        self.noise_dropdown = None
        self.circleToggle = None
        self.point1_x, self.point2_x, self.point1_y, self.point2_y = 0,0,0,0 # initializing image points

        frame1 = tkinter.Frame(self.master, pady=10)
        self.text1 = tkinter.Label(self.master, text="Image Restoration", font=("Helvetica",16)).grid(row=0)

        tkinter.Button(frame1, text="Upload an Image", command=self.image_browse, fg="white", bg="black").pack()
        frame1.grid(row=1)


        #self.text1.pack()

        self.canvas = tkinter.Canvas(self.master, width=self.c_size[0], height=self.c_size[1], relief='solid',
                                     bd=self.border_size)
        self.canvas.grid(row=2)



def main():
    root = tkinter.Tk()
    var = IntVar()
    GUI_Restoration(root, var)
    root.mainloop()

if __name__ == "__main__":
    main()
