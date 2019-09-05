#I want to grab the stD of the residual image, multiple it by 4 (4 standard deviations.)
#Then I want to make sure no number is above or below that, if it is then we will
#change that value to the median value.
#Then we will have to convert this back to a NP array so we can redisplay this as a graph???

with open("AP_Stats.csv", "r") as f:
    All_stats = f.read()
#Make the CSV into a list.
Stat_list = All_stats.split(",")
#Grab Residual images STD
std_Res = Stat_list[9]
#Go out 4 stDs
FourStd = float(std_Res)*4
#Grab the median of Residual Image
med_Res = Stat_list[10]
#Parse
med_Res = float(med_Res)
#Generate Range
min_val = med_Res-FourStd
max_val = med_Res+FourStd
#If the value of each point is larger than the min value but smaller then the max value it's fine
#If it's OUTSIDE that range, change it to the median.
def valueShift(target_val):
    if(target_val > max_val or target_val < min_val):
        return med_Res
    else:
        return target_val


#Aquire the residual_image points and turn them into a list.
with open("AP_Res.csv", "r") as f:
    Res_img = f.read()

Res_list = Res_img.split(",")

#Run the threshold program
for _ in range(len(Res_list)):
    new_val = valueShift(float(Res_list[_]))
    if Res_list[_] != new_val:
        #print("New Value, change {} to {}".format(Res_list[_], new_val))
        Res_list[_] = new_val
    else:
        print("HMM {} or {}".format(Res_list[_],new_val))

Res_list = [str(i) for i in Res_list]

ResCsv = ",".join(Res_list)
#Aquire the residual_image points and turn them into a list.
with open("APC_Res.csv", "w") as f:
    f.write(ResCsv)

print("Threshold Complete")
