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






class App:
    
    def __init__(self):
        
        #-------------------------#
        def SubmitEvent(self):
            
            global fileLocation
            #sigma_psf = 2.88
            SigmaPSF = SigmaPSFentry.get()
            sigma_psf = float(SigmaPSF)
            N_iters1 = nitersEntry.get()
            N_iters = float(N_iters1)
            print(SigmaPSF)
            print(N_iters)
            with fits.open(fileLocation) as hdul:
                image = hdul[0].data

            bkgrms = MADStdBackgroundRMS()
            std = bkgrms(image)

            iraffind = IRAFStarFinder(threshold=3.5*std, fwhm=sigma_psf*gaussian_sigma_to_fwhm, minsep_fwhm=0.01, roundhi=5.0, roundlo=-5.0, sharplo=0.0, sharphi=2.0)
            daogroup = DAOGroup(2.0*sigma_psf*gaussian_sigma_to_fwhm)

            mmm_bkg = MMMBackground()
            fitter = LevMarLSQFitter()
            psf_model = IntegratedGaussianPRF(sigma=sigma_psf)
            photometry = IterativelySubtractedPSFPhotometry(finder=iraffind, group_maker=daogroup, bkg_estimator=mmm_bkg, psf_model=psf_model, fitter=LevMarLSQFitter(), niters=N_iters, fitshape=(11,11))
            result_tab = photometry(image=image)
            residual_image = photometry.get_residual_image()

            phot_results = photometry(image)
            with open("output.txt", "w") as text_file:
                print(phot_results['x_fit', 'y_fit', 'flux_fit'], file=text_file)
            print(phot_results['x_fit', 'y_fit', 'flux_fit'])
            #Plot images made#
            plt.subplot(1, 2, 1)
            plt.imshow(image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('Raw Image')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            plt.subplot(1 ,2, 2)
            plt.imshow(residual_image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
            plt.title('Residual Image')
            plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
            plt.show()
        #-------------------------#

        self.root = Tk()
        self.root.title("PSF")
        self.root.minsize(width=500,height=400)

        ############MECHANISM##############
        #---------------------------------#
        ##Setup Data##
        ftypes = [('fits files',"*.fits")]
        ttl  = "File Finder"
        
        
        #---------------------------------#
        def BrowseButton(event):
            self.root.fileName = filedialog.askopenfilename(filetypes = ftypes, title = ttl)
            global fileLocation
            fileLocation = self.root.fileName
            
        #Beautification
        frame = Frame(self.root)
        frame.pack()
        Frame_Label = Label(frame, text="Before using this program you should have: \n -a text file to output to.\n -a .fits file.")
        Frame_Label.grid(row=1, column=0, sticky=N)
        
        SigmaPSFeL = Label(frame, text="Sigma PSF:")
        SigmaPSFeL.grid(row=3, column=0, sticky=W)
        SigmaPSFentry = Entry(frame)
        SigmaPSFentry.grid(row=3, column=1, sticky=W)
        SigmaPSFentry.insert(0, "2")
        
        nitersEL = Label(frame, text="niters:")
        nitersEL.grid(row=4, column=0, sticky=W)
        nitersEntry = Entry(frame)
        nitersEntry.grid(row=4, column=1, sticky=W)
        nitersEntry.insert(0, "1")
        
        Browse = Button(frame, text="Browse", fg="black")
        Browse.grid(row=5, column=0, sticky=W)
        Browse.bind("<Button-1>", BrowseButton)
        Submit = Button(frame, text="Submit", fg="black")
        Submit.grid(row=5, column=1, sticky=W)
        Submit.bind("<Button-1>", SubmitEvent)


    
app = App()

app.root.mainloop()
