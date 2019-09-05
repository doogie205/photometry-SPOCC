import re

with open("AP_RI.txt", "r") as f:
    AP_Res = f.read()

with open("AP_BS.txt", "r") as f:
    AP_Bac = f.read()


AP_Res = AP_Res.replace("[",",")
AP_Res = AP_Res.replace("]",",")
AP_Res = AP_Res.replace(" ",",")
AP_Res = AP_Res.replace(",,",",")
AP_Res = AP_Res.replace(",,,",",")
AP_Bac = AP_Bac.replace(",,",",")

AP_Bac = AP_Bac.replace("[",",")
AP_Bac = AP_Bac.replace("]",",")
AP_Bac = AP_Bac.replace(" ",",")
AP_Bac = AP_Bac.replace(",,",",")
AP_Bac = AP_Bac.replace(",,,",",")
AP_Bac = AP_Bac.replace(",,",",")

with open("AP_Res.txt", "w") as f:
    sf_R = AP_Res.replace(",","\n")
    f.write(sf_R)

with open("AP_Bac.txt", "w") as f:
    sf_B = AP_Bac.replace(",","\n")
    f.write(sf_B)

with open("AP_Res.csv", "w") as f:
    AP_Res = AP_Res.replace("\n","")
    AP_Res = AP_Res.replace(",,",",")
    try:
        AP_Res = AP_Res.replace(",","",1)
        a = re.search(",$",AP_Res)
        AP_Res = AP_Res[:a.span()[0]] + AP_Res[(a.span()[0]+1):]
    except:
        print("whoops something failed")
        pass
    f.write(AP_Res)

with open("AP_Bac.csv", "w") as f:
    AP_Bac = AP_Bac.replace("\n","")
    AP_Bac = AP_Bac.replace(",,",",")
    try:
        AP_Bac = AP_Bac.replace(",","",1)
        b = re.search(",$",AP_Bac)
        AP_Bac = AP_Bac[:b.span()[0]] + AP_Bac[(b.span()[0]+1):]
    except:
        print("whoops something failed")
        pass
    f.write(AP_Bac)

print("Successfully created CSV")
