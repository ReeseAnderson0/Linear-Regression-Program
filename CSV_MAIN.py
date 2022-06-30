from tkinter import *
from tkinter import filedialog
import tkinter
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

import tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        window = root
        window.title('File Explorer')
        window.title("CSV To Linegraph")
        window.geometry("700x300")
        window.resizable(False,False)
        panel.pack(side = "bottom", fill = "both")
        fileLocation = tkinter.Entry(window, width=50)
        fileLocation.place(relx=0.5, rely=0.20, anchor=CENTER)
        def browseFiles():
            fileLocation.delete(0,"end")
            filename = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (("Text files",
                                                                "*.csv*"),
                                                            ("all files",
                                                                "*.*")))
            fileLocation.insert(1, filename)
            MainApplication.plot_CSV(str(filename))
        btn_Search = Button(window,
            text = "Browse Files",
            command = browseFiles)
        btn_Close = Button(window,
            text = "Exit",
            command = exit)
        btn_Search.place(relx=0.5, rely=0.1, anchor=CENTER)
        btn_Close.place(relx=1, rely=1, anchor=SE)
    
    def CSV_Path(fileLocation):
        MainApplication.CSV_To_Dictonary(fileLocation)

    def CSV_To_Dictonary (path):
        while True:
            try:
                data=pd.read_csv(path)
                columns=(data.columns)
                tableDic={}
                for column in columns:
                    x=0 
                    tableDic[column] = {}
                    for y in range(len(data[columns])):
                        tableDic[column][x] = [data[column][y]] # Format of Array ex. --> tableDic['Weight'][index = 532] == 122.5699
                        x+=1
                return tableDic
            except FileNotFoundError:
                print("Couldnt Find File")
                return False 

    def Dic_To_List(Dictonary): # Xlist[0] Ylist[1]
        xList = []
        yList = []
        varList = [xList,yList]
        for x in range(len(Dictonary)):
            index = x
            key = list(Dictonary.keys())[index]
            for x in range(len(Dictonary[key])):
                convert = str([Dictonary[key][x]]) # STR
                convert = "".join(_ for _ in convert if _ in ".1234567890")
                convert = float(convert)
                varList[index] += [convert]
        return varList

    def simga_list(List): # xTimesY[0] xSquared[1] ySquared[2]
        xTimesY = []
        xSquared = []
        ySquared = []
        sigma_list = [xTimesY,xSquared,ySquared]
        for q in range(3):
            for w in range(len(List[0])):
                if (q == 0):
                    sigma_list[0] += [List[0][w] * List[1][w]]
                if (q == 1):
                    sigma_list[1] += [List[0][w] ** 2]
                if (q == 2):
                    sigma_list[2] += [List[1][w] ** 2]
        return sigma_list


    def get_equation(path):
        Dictonary = MainApplication.CSV_To_Dictonary(path)
        List = MainApplication.Dic_To_List(Dictonary)
        simga_lost = MainApplication.simga_list(List)
        SumXTimesY = sum(simga_lost[0])
        SumXSquared = sum(simga_lost[1])
        SumYSquared = sum(simga_lost[2])
        SumX = sum(List[0])
        SumY = sum(List[1])
        n = float(len(List[0]))
        r1 = (n * (SumXTimesY) - (SumX) * (SumY))
        r2 = math.sqrt((n * (SumXSquared)-(SumX) ** 2)) * math.sqrt((n * (SumYSquared)-(SumY) ** 2))
        r = r1 / r2
        m1 = (n*(SumXTimesY)-(SumX)*(SumY))
        m2 = (n*(SumXSquared)-(SumX)**2)
        m = m1 / m2
        ##print(f"{m1} = m1 | {m2} = m2 | {m} = m")
        b = (((SumY)- (m) * SumX) / n)
        m = float("{:.2f}".format(m))
        b = float("{:.2f}".format(b))
        y = f"y = {m}x + {b}"
        ##print(f"{y} | b = {m} | b = {b}")
        return y, m ,b, n, r

    def plot_CSV(path):
        Dic = MainApplication.CSV_To_Dictonary(path)
        List = MainApplication.Dic_To_List(Dic)
        equation,m,b,n,r = MainApplication.get_equation(path)
        x = np.array(List[0])
        y = np.array(List[1])
        xmin = min(List[0])
        xmax = max(List[0])
        ymax = max(List[1])
        xTitle = list(Dic.keys())[0]
        yTitle = list(Dic.keys())[1]
        df = pd.DataFrame({xTitle:x,yTitle:y})
        plt.figure(figsize=(8,5))
        r = int(r * 1000)
        r = r / 1000
        r2 = r ** 2
        r2 = int(r2 * 1000)
        r2 = r2 / 1000
        adjustR2 = 1 - ((1- r2) * (n - 1)) / (n - 2 - 1)
        adjustR2 = int(adjustR2 * 1000)
        adjustR2 = adjustR2 / 1000
        plt.title(f'{xTitle} vs {yTitle} \n {equation} | n={n} | r={r} | r²={r2} | Adjucted R² = {adjustR2}')
        sns.scatterplot(x=f'{xTitle}',y=f'{yTitle}',data=df).get_figure().savefig(f'{xTitle} vs {yTitle}.jpg')
        x = np.linspace(xmin,xmax)
        y = (m*x)+b
        plt.plot(x, y, '-r')
        plt.grid()
        plt.show()
        return


if __name__ == "__main__":
    root = tk.Tk()
    path = "marble.jpg" ## https://pixabay.com/illustrations/background-modern-computer-design-1747777/
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(root, image = img)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


       


