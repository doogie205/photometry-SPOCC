#THIS FILE USES TKINTER AND IS NOT AVAILABLE ON ALL PLATFORMS, AS SUCH IT SHOULD NOT BE USED IN THE LONG RUN.

#Grab the libraries/modules we need:
from photutils.psf import IterativelySubtractedPSFPhotometry
from photutils.detection import IRAFStarFinder
from photutils.psf import IntegratedGaussianPRF, DAOGroup
from photutils.background import MMMBackground, MADStdBackgroundRMS
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm
from astropy.io import fits
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import subprocess
import math
import numpy as np
from mpl_toolkits.mplot3d import axes3d

#This allows us to keep the application updating constantly
class App:
    #This is just something that's needed to initialize the app.
    def __init__(self):

        #-------------------------#
        #This is the event that's ran when the GUI's submit button is clicked, if you wish to see the gui you can head to the gui section
        def SubmitEvent(self):



            #Not a fan of globals but this is the easiest way to grab the file location
            global fileLocation
            #sigma_psf = 2.88
            #Grab the Sigma from the Entry box in the GUI
            SigmaPSF = SigmaPSFentry.get()
            #Turn the string into a float
            sigma_psf = float(SigmaPSF)
            #Grab the number of iterations from Entry box in GUI
            N_iters1 = nitersEntry.get()
            #Turn the string into a float
            N_iters = float(N_iters1)
            #Test cases to make sure that information was flowing from the GUI to the program
            #print(SigmaPSF)
            #print(N_iters)

            #Open the file as a fits (allows us to handle it) then turn that into readable data.
            with fits.open(fileLocation) as hdul:
                image = hdul[0].data

            #automatically gathered information needed to run the Star Finder
            bkgrms = MADStdBackgroundRMS()
            std = bkgrms(image)

            #Find the stars
            iraffind = IRAFStarFinder(threshold=3.5*std, fwhm=sigma_psf*gaussian_sigma_to_fwhm, minsep_fwhm=0.01, roundhi=5.0, roundlo=-5.0, sharplo=0.0, sharphi=2.0)
            #Group the stars
            daogroup = DAOGroup(2.0*sigma_psf*gaussian_sigma_to_fwhm)

            #More automatically gathered info needed for IS-PSFPhotometry to take places
            mmm_bkg = MMMBackground()
            fitter = LevMarLSQFitter()
            #Grabbed from the user input
            psf_model = IntegratedGaussianPRF(sigma=sigma_psf)
            #Run IS-PSFPhotometry
            photometry = IterativelySubtractedPSFPhotometry(finder=iraffind, group_maker=daogroup, bkg_estimator=mmm_bkg, psf_model=psf_model, fitter=LevMarLSQFitter(), niters=N_iters, fitshape=(11,11))
            #Do photometry on the image
            result_tab = photometry(image=image)
            #grab the resiudal image
            residual_image = photometry.get_residual_image()

            #Get the results of the photometry and print the aspects we want.
            phot_results = photometry(image)
            with open("output.txt", "w") as text_file:
                print(phot_results['x_fit', 'y_fit', 'flux_fit'], file=text_file)
            print(phot_results['x_fit', 'y_fit', 'flux_fit'])
            print("Sum of pixels: {}".format(sum(sum(residual_image))))
            #Plot images made#
            #Start by creating plots.
            plt.subplot(1, 5, 1)
            #Show the first plot (which is just the raw image)
            plt.imshow(image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('Raw')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            #Create the second plot
            plt.subplot(1 ,5, 2)
            #Show the residual_image
            plt.imshow(residual_image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('PSF')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            #Draw in the sum of pixels.
            plt.text(0, 65, "Sum of pixels: {}".format(sum(sum(residual_image))), fontsize=7)
            #Create the third plot which is the subtracted images combined.
            sb = image-residual_image
            plt.subplot(1 ,5, 3)
            plt.imshow(sb, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('PSF-S')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)


            with open("AP_RI.txt", "w") as f:
                for _ in range(len(residual_image)):
                    f.write(str(residual_image[_]))
            with open("AP_BS.txt", "w") as f:
                for _ in range(len(sb)):
                    f.write(str(sb[_]))

            print("Starting creation of CSV")
            subprocess.run(['py', 'create_CSV.py'], shell=False)

            print("Starting creation of Stats")
            subprocess.run(['py', 'create_info.py'], shell=False)

            print("Starting Threshold")
            subprocess.run(['py', 'threshold.py'], shell=False)

            with open("APC_Res.csv", "r") as f:
                APC_Res = f.read()
            APC_Res = APC_Res.split(",")
            APC_Res = [float(i) for i in APC_Res]









            #Every (SquareRoot of the Pixels) datapoints create a new array. Into a 2D Array.
            #I'm going to use the Correct_Res list as the main list and store the temp list every Sqrt(pix) in it,
            #then reset that list and continue until the pixel count is met.
            #Have an internal counter. Reset that every Sqrt(Pix)
            temp_list = np.array([])
            SqrPixels = math.sqrt(len(APC_Res))
            internal_counter = 0
            #print(SqrPixels)
            #print(len(APC_Res))
            Corrected_Res = np.array([[]])

            for _ in range(len(APC_Res)):
                if internal_counter <= SqrPixels-2:
                    try:
                        temp_list= np.append(temp_list,APC_Res[_-1])
                        #print(_)
                        if _+1 == (int(SqrPixels)*int(SqrPixels)):
                            Corrected_Res=np.append(Corrected_Res, temp_list)
                    except:
                        print("Not right 2.0")
                    internal_counter = internal_counter+1
                else:
                    internal_counter = 0
                    #print(temp_list)
                    Corrected_Res=np.append(Corrected_Res, temp_list)
                    temp_list = []
                    temp_list = np.append(temp_list,APC_Res[_-1])
                    #print("Resetting Counter & List {}".format(_))
                    if _+1 == (int(SqrPixels)*int(SqrPixels)):
                        Corrected_Res=np.append(Corrected_Res, temp_list)
                        #print(_+1)
                    #print("Iteration {}".format(_))
            #print(residual_image)
            #print("\n")
            #print(Corrected_Res)
            Corrected_Res = np.reshape(Corrected_Res,(int(SqrPixels),int(SqrPixels)))

            Correct_BS = image-Corrected_Res
            plt.subplot(1, 5, 4)
            plt.imshow(Corrected_Res, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('CPSF')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)


            plt.subplot(1 ,5, 5)
            plt.imshow(Correct_BS, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('CPSF-S')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)








	        #Number of bins
            n_bins = 20
	        #Not super sure why this works the way that it does if I’m being truthful, took tinkering to work, and lots of documentation examples.
            fig, axs = plt.subplots(1, 2)

            # We can set the number of bins with the `bins` kwarg
            axs[0].hist(residual_image, bins=n_bins)
            plt.title('Residual Image Hist')
            axs[1].hist(sb, bins=n_bins)
            plt.title('Background Subtracted Hist')
            #plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            #All Pixels from residual image


            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            delta=(6*(1/len(sb)))

            nx = ny = np.arange(-3.0, 3.0, delta)
            X, Y = np.meshgrid(nx, ny)
            #print(X)
            #print(Y)
            x, y, z = X * len(sb), Y * len(sb), sb
            ax.plot_surface(x,y,z, rstride=1, cstride=1, cmap='viridis')


            figi = plt.figure()
            axi = figi.add_subplot(111, projection='3d')
            deltai=(6*(1/len(sb)))

            nxi = nyi = np.arange(-3.0, 3.0, deltai)
            Xi, Yi = np.meshgrid(nxi, nyi)
            #print(X)
            #print(Y)
            xi, yi, zi = Xi * len(Correct_BS), Yi * len(Correct_BS), Correct_BS
            axi.plot_surface(xi,yi,zi, rstride=1, cstride=1, cmap='viridis')


            plt.show()

        #-------------------------#

        #Master/Root
        self.root = Tk()
        #Title of program
        self.root.title("PSF")
        #Smallest the window can be.
        self.root.minsize(width=500,height=400)

        ############MECHANISM##############
        #---------------------------------#
        ##Setup Data##
        #Set the types of files you need in the file dialog
        ftypes = [('fits files',"*.fits")]
        ttl  = "File Finder"


        #---------------------------------#
        #This is the event that happens when the browse button is hit.
        def BrowseButton(event):
            #Open a file dialog.
            self.root.fileName = filedialog.askopenfilename(filetypes = ftypes, title = ttl)
            #Set the fileLocation, this will be able to be grabbed "outside" the GUI
            global fileLocation
            fileLocation = self.root.fileName





        ##Beautification##
        #This is the main frame
        frame = Frame(self.root)
        #Pack the frame so it can be seen
        frame.pack()
        #Add a label telling people what they need.
        Frame_Label = Label(frame, text="Before using this program you should have: \n -a text file to output to.\n -a .fits file.")
        #Grid it up to make it look pretty.
        Frame_Label.grid(row=1, column=0, sticky=N)

        #Entry Label
        SigmaPSFeL = Label(frame, text="Sigma PSF:")
        #Grid it up
        SigmaPSFeL.grid(row=3, column=0, sticky=W)

        #Actual Entry Box
        SigmaPSFentry = Entry(frame)
        #Grit it up
        SigmaPSFentry.grid(row=3, column=1, sticky=W)
        #Add a base value to the Entry
        SigmaPSFentry.insert(0, ".409")

        #Label above entry box
        nitersEL = Label(frame, text="niters:")
        #Grid it up
        nitersEL.grid(row=4, column=0, sticky=W)
        #Create Entry for number of iterations
        nitersEntry = Entry(frame)
        #Dont forget to grid it up!
        nitersEntry.grid(row=4, column=1, sticky=W)
        #Insert a base value
        nitersEntry.insert(0, "7")

        #Create a button with the inner text saying "Browse"
        Browse = Button(frame, text="Browse", fg="black")
        #Never ever forget to grid it up.
        Browse.grid(row=5, column=0, sticky=W)
        #Create an action that happens when we left click the button (the second argument is a method we create)
        Browse.bind("<Button-1>", BrowseButton)
        #Create a button with the inner text saying "Submit"
        Submit = Button(frame, text="Submit", fg="black")
        #I hope you know to grid it up by now
        Submit.grid(row=5, column=1, sticky=W)
        #Binding this button to a function when it's clicked with the left mouse button.
        Submit.bind("<Button-1>", SubmitEvent)



#This runs the app upon the py file being ran.
app = App()
#This is necessary for tkinter
app.root.mainloop()
