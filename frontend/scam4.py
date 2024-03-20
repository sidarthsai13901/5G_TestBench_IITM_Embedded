from customFTDI import Ftdi
lis1=Ftdi.show_devices()

lis2=[]
# print(lis1)
for i in lis1:
    lis2.append(i[0])

print(lis2)