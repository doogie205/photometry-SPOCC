from statistics import *
import numpy as np

def get_Range(val_list):
    min_val = min(val_list)
    max_val = max(val_list)
    rge = max_val - min_val
    return rge

with open("AP_Bac.csv", "r") as f:
    AP_BS = f.read()

BS_list = AP_BS.split(",")
BS_list = [float(i) for i in BS_list]
avg_BS = mean(BS_list)
sum_BS = sum(BS_list)
std_BS = stdev(BS_list)
med_BS = median(BS_list)
rge_BS = get_Range(BS_list)


with open("AP_Res.csv", "r") as f:
    AP_RI = f.read()

RI_list = AP_RI.split(",")
RI_list = [float(i) for i in RI_list]
avg_RI = mean(RI_list)
sum_RI = sum(RI_list)
std_RI = stdev(RI_list)
med_RI = median(RI_list)
rge_RI = get_Range(RI_list)


with open("AP_Stats.txt", "w+") as f:
    f.write("The total amount of points from the background subtracted image is: {}\n".format(len(BS_list)))
    f.write("The average of the background subtracted image's pixels: {}\n".format(avg_BS))
    f.write("The sum of the background subtracted image's pixels: {}\n".format(sum_BS))
    f.write("The standardDev of the background subtracted image's pixels: {}\n".format(std_BS))
    f.write("The median of the background subtracted image's pixels: {}\n".format(med_BS))
    f.write("The range of the background subtracted image's pixels: {}\n".format(rge_BS))

    f.write("\n")

    f.write("The total amount of points from the residual image is: {}\n".format(len(RI_list)))
    f.write("The average of the residual image's pixels: {}\n".format(avg_RI))
    f.write("The sum of the residual image's pixels: {}\n".format(sum_RI))
    f.write("The standardDev of the residual image's pixels: {}\n".format(std_RI))
    f.write("The median of the residual image's pixels: {}\n".format(med_RI))
    f.write("The range of the residual image's pixels: {}\n".format(rge_RI))

    f.write("\n")

    f.write("The max value for BS image is: {}\n".format(max(BS_list)))
    f.write("The min value for BS image is: {}\n".format(min(BS_list)))
    f.write("The max value for RI image is: {}\n".format(max(RI_list)))
    f.write("The min value for RI image is: {}\n".format(min(RI_list)))


Stats_CSV = "{},{},{},{},{},{},{},{},{},{},{},{}".format(len(BS_list),avg_BS,sum_BS,std_BS,med_BS,rge_BS,len(RI_list),avg_RI,sum_RI,std_RI,med_RI,rge_RI)

with open("AP_Stats.csv", "w+") as f:
    f.write(Stats_CSV)

print("Successfully created Stats.")
