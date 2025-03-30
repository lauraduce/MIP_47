import random
import time #būs vajadzīgs, lai noteiktu AI gājienā patērēto laiku

import tkinter #izmanto grafiskajai saskarnei
from tkinter import * #izmanto vairākās funkcijās, kas saistītas ar grafisko saskarni (Label, Entry, Button, Tk)
from tkinter import messagebox #izmanto kļūdu logu izvadei

global virkne, speletaja_punkti, ai_punkti, nulltais, algoritms, speletajs #deklarē izmantojamos mainīgos pirms visām metodēm
virkne = []
speletaja_punkti = 0
ai_punkti = 0
nulltais = 0
algoritms = ""
speletajs = True

#--------------------------------------------------------SPĒLES KOKS---------------------------------------------------------
class Tree:
    def __init__(self, virkne, speletaja_punkti, ai_punkti):
        self.virkne = virkne
        self.speletaja_punkti = speletaja_punkti
        self.ai_punkti = ai_punkti
        self.children = []
        self.parent = None
        self.heiristiskais_vertejums = None

    def Pectecu_generesana(self):       
        for i in range(len(self.virkne)):
            new_virkne = self.virkne [:i] + self.virkne[i + 1:]#izņem i-to locekli no virknes
            child = Tree(new_virkne, self.speletaja_punkti, self.ai_punkti) #veido nākamo koku ar jauno virkni
            child.parent = self #norāda, ka katra jaunā apakškoka parent ir pašreizējais koks
            self.children.append(child) #pievieno child jeb jauno apakškoku children sarakstam

#------------------------------------------------MĒRĶA STĀVOKĻA PĀRBAUDE----------------------------------------------------
def Speles_beigas():
    global speletaja_punkti, ai_punkti

    for ieraksts in logs.winfo_children():
        ieraksts.destroy() #izdzēš visas pogas, laukus, tekstus, utt.

    logs.geometry("250x250")
    logs.columnconfigure(0, weight = 1)
    logs.columnconfigure(2, weight = 0)

    Label(logs, text = "Uzvarētājs:", font=("Arial", 10, "bold")).grid(row = 1, column = 1, pady = 5)

    if speletaja_punkti > ai_punkti:
        Label(logs, text = "Speletājs!").grid(row = 2, column = 1, pady = 5)

    else:
        Label(logs, text = "AI!").grid(row = 2, column = 1, pady = 5)

#----------------------------------------------------GĀJIENU APSTRĀDE--------------------------------------------------------
#========================================================= Dalīšana =========================================================
def Dalit(skaitlis, skaits):
    global speletaja_punkti, ai_punkti, virkne, algoritms, speletajs
    logs.columnconfigure(len(virkne) + 1, weight = 0)

    if speletajs: #pārbauda vai ir spēlētāja gājiens
        if skaitlis == 2: #pārbauda vai izvēlētais skaitlis ir 2 un veic turpmākās darbības
            
            for i in range(2):
                virkne.append(1) #pievieno divus "1" virknes beigās

            virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes

        else: #citādi skaitlim ir jābūt 4
            speletaja_punkti += 1 #pieskaita spēlētāja kopējam punktu skaitam 1 punktu

            for i in range(2):
                virkne.append(2) #pievieno divus "2" virknes beigās

            virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes
        
        speletajs = False #spēlētāja gājiens ir beidzies

    else:
        if skaitlis == 2: #pārbauda vai izvēlētais skaitlis ir 2 un veic turpmākās darbības
            
            for i in range(2):
                virkne.append(1) #pievieno divus "1" virknes beigās

            virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes

        else: #citādi skaitlim ir jābūt 4
            ai_punkti += 1 #pieskaita spēlētāja kopējam punktu skaitam 1 punktu

            for i in range(2):
                virkne.append(2) #pievieno divus "2" virknes beigās

            virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes
        
        speletajs = True #AI gājiens ir beidzies

    Gajiens()

#======================================================= Pieskaitīšana ======================================================
def Pieskaitit(skaitlis, skaits):
    global speletaja_punkti, ai_punkti, virkne, algoritms, speletajs
    logs.columnconfigure(len(virkne) + 1, weight = 0)

    if speletajs: #pārbauda vai ir spelētāja gājiens
        speletaja_punkti += skaitlis #ja ir, spēlētājam pieskaita izvēlēto punktu skaitu
        virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes

        speletajs = False #spēlētāja gājiens ir beidzies

    else:
        ai_punkti += skaitlis #citādi tas nozīmē, ka ir AI gājiens => pieskaita punktus AI kopējam punktu skaitam
        virkne.pop(skaits) #izņem skaitli, kurš izvēlēts punktu pieskaitīšanai, no spēles virknes

        speletajs = True #AI gājiens ir beidzies

    Gajiens()

#===================================================== Darbības apstrāde ====================================================  
def Darbiba(skaitlis, skaits):
    papildlogs = Toplevel(logs) #izveido papildlogu ar divām izvēles pogām - "Dalīt" un "Pieskaitīt"
    papildlogs.title("Izvēle")
    papildlogs.geometry("250x150")
    papildlogs.columnconfigure(0, weight = 1)
    papildlogs.columnconfigure(2, weight = 1)

    Label(papildlogs, text = "Izvēlieties darbību:", font=("Arial", 10, "bold")).grid(row = 1, column = 1, pady = 5)

    split = tkinter.Button(papildlogs, text = "Dalīt", command = lambda: [Dalit(skaitlis, skaits), papildlogs.destroy()]) #izveido pogu, kas nosūta vertības uz dalīsanas izpildi, kā arī izdzēš pašu papildlogu pēc izvēles veikšanas
    split.grid(row = 2, column = 1, pady = 5) #pogas novietojums logā

    pieskaitit = tkinter.Button(papildlogs, text = "Pieskaitīt", command = lambda: [Pieskaitit(skaitlis, skaits), papildlogs.destroy()]) #izveido pogu, kas nosūta vertības uz pieskaitīšanas izpildi, kā arī izdzēš pašu papildlogu pēc izvēles veikšanas
    pieskaitit.grid(row = 4, column = 1, pady = 5) #pogas novietojums logā

#===================================================== Spēlētāja gājiens ====================================================
def Speletaja_gajiens(skaitlis, skaits):
    if skaitlis == 2 or skaitlis == 4: #pārbauda vai izvelētais cipars ir dalāms
        Darbiba(skaitlis, skaits) #nosūta izvelēto skaitli un tā atrasanās vietu uz darbības izvēli

    else:
        Pieskaitit(skaitlis, skaits) #nosūta izvelēto skaitli un tā atrasanās vietu uz punktu pieskaitīšanu

#===================================================== Gājienu apstrāde =====================================================      
def Gajiens():
    global nulltais, speletajs

    if len(virkne) == 0:
        Speles_beigas()

    if nulltais == 0: #pārbauda vai gājiens ir nulltais, tādējādi pārbauda vai galvenais spēles logs ir izveidots
        for ieraksts in logs.winfo_children():
            ieraksts.destroy() #izdzēš visas pogas, laukus, tekstus, utt.=

        logs.geometry("950x200")
        logs.grid_columnconfigure(0, weight = 1) #izdzēš atstarpi pirms 0tās kolonnas, lai starp pogām nav tukšuma
        logs.grid_columnconfigure(2, weight = 0) #izdzēš atstarpi pēc 2trās kolonnas, lai starp pogām nav tukšuma
        logs.grid_columnconfigure(len(virkne) + 1, weight = 1) #izveido atstarpi pēc virknes, lai pogas būtu centrētas

        Label(logs, text = "Spēlētāja punkti: " + str(speletaja_punkti) + " | " + "AI punkti: " + str(ai_punkti)).grid(row = 1, column = 1, columnspan = len(virkne), pady = 5) #rāda spēlētāja un AI punktu skaitu

        for i in range(len(virkne)): 
            button = tkinter.Button(logs, text = virkne[i], width = 5, command = lambda skaitlis = virkne[i], skaits = int(i) : Speletaja_gajiens(skaitlis, skaits)) #virknes vērtības pārveido pogās. Nosapiestās pogas vērtību un pozīciju nosūta uz spēlētāja gājienu
            button.grid(row = 2, column = i + 1, pady = 5) #pogas novietojums logā

        nulltais += 1

    else:
        if speletajs: #pārbauda vai ir spelētāja gājiens
            logs.grid_columnconfigure(len(virkne) + 1, weight = 1) #izveido atstarpi pēc virknes, lai pogas būtu centrētas

            Label(logs, text = "Spēlētāja punkti: " + str(speletaja_punkti) + " | " + "AI punkti: " + str(ai_punkti)).grid(row = 1, column = 1, columnspan = len(virkne), pady = 5) #rāda spēlētāja un AI punktu skaitu

            for i in range(len(virkne)): 
                button = tkinter.Button(logs, text = virkne[i], width = 5, command = lambda skaitlis = virkne[i], skaits = int(i) : Speletaja_gajiens(skaitlis, skaits)) #virknes vērtības pārveido pogās. Nosapiestās pogas vērtību un pozīciju nosūta uz spēlētāja gājienu
                button.grid(row = 2, column = i + 1, pady = 5) #pogas novietojums logā
        
        #else:

#--------------------------------------------------------ALGORITMI-----------------------------------------------------------
def Minmax():
    global algoritms, speletajs, nulltais

    if nulltais == 0: #pārbauda vai koks jau ir ģenerēts
        sakums = Tree(virkne, speletaja_punkti, ai_punkti) #izveido koku ar norādītajiem parametriem
        sakums.Pectecu_generesana() #ģenerē spēles koku
    
    else:
        if speletajs: #pārbauda vai ir spēlētāja gājiens
            Gajiens() #novirza spēlētāju uz gājiena izpildi

        #else:


def Alfa_beta():
    global algoritms, speletajs, nulltais

    if nulltais == 0: #pārbauda vai koks jau ir ģenerēts
        sakums = Tree(virkne, speletaja_punkti, ai_punkti) #izveido koku ar norādītajiem parametriem
        sakums.Pectecu_generesana() #ģenerē spēles koku
    
    else:
        if speletajs: #pārbauda vai ir spēlētāja gājiens
            Gajiens() #novirza spēlētāju uz gājiena izpildi

        #else:

#----------------------------------------------------ALGORITMA IZVĒLE--------------------------------------------------------
def Algoritma_izvele():
    global algoritms, speletajs

    for ieraksts in logs.winfo_children():
        ieraksts.destroy() #izdzēš visas pogas, laukus, tekstus, utt.

    Label(logs, text = "Izvēlieties algoritmu:", font = ("Arial", 10 , "bold")).grid(row = 1, column = 1, pady = 5)

    algoritms1 = tkinter.Button(logs, text = "Minmaksa", width = 10, command = lambda algoritms = "Minmaksa": Minmax()) #poga, kas izvēlas minmakasa aloritmu
    algoritms1.grid(row = 3,column = 1, pady = 5) #pogas novietojums logā

    algoritms2 = tkinter.Button(logs, text = "Alfa-beta", width = 10, command = lambda algoritms = "Alfa-beta": Alfa_beta()) #poga, kas izvēlas alfa-beta aloritmu
    algoritms2.grid(row = 5,column = 1, pady = 5) #pogas novietojums logā

    logs.mainloop() #turpina aplikācijas darbību

#------------------------------------------------SĀKUMA STĀVOKĻA IZVEIDE-----------------------------------------------------
def Sakuma_stavoklis():
    length = lauks.get() #iegūst ievades laukā ievadīto vērtību (var būt skaitlis vai burti)

    if length.isdigit():
        garums = int(length)

        if 15 <= garums <= 20:
            for i in range(garums):
                virkne.append(random.randint(1,4)) #pārbaudot ievadīto vērtību, izveido random virkni ar cipariem

            Algoritma_izvele()
        
        else:
            messagebox.showerror("Kļūda", "Ievadiet skaitli no 15 līdz 20") #kļūdas apstrāde

    else:
        messagebox.showerror("Kļūda", "Ievadiet skaitli") #kļūdas apstrāde

#--------------------------------------------HEIRISTISKĀ VĒRTĒJUMA FUNKCIJA-------------------------------------------------
#def Heiristiskais_vertejums():

#----------------------------------------------------GRAFISKĀ SASKARNE------------------------------------------------------
logs = tkinter.Tk() #izveido aplikācijas logu
logs.title("Divpersonu spēle")
logs.geometry("270x150")
logs.grid_columnconfigure(0, weight = 1) #izveido atstarpi 0tajā kolonnā
logs.grid_columnconfigure(2, weight = 1) #izveido atstarpi 2trajā kolonnā

Label(logs, text = "Ievadiet skaitli no 15 līdz 20:", font=("Arial", 10, "bold")).grid(row = 1, column = 1, pady = 5) #vnk teksts

lauks = Entry(logs) #izveido ievades lauku, kur ierakstīt virknes garumu
lauks.grid(row = 3, column = 1, pady = 5) #ievades lauka novietojums logā

generet = tkinter.Button(logs, text = "Ģenerēt virkni", width = 15, command = Sakuma_stavoklis) #poga, kas ģenerē ievadītā izmēra virkni
generet.grid(row = 5, column = 1, pady = 10) #pogas novietojums logā

logs.mainloop() #palaiž aplikāciju un turpina tās darbību

#------------------------------------------------------IZMANTOTIE AVOTI-----------------------------------------------------
## https://www.geeksforgeeks.org/python-gui-tkinter/
## https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
## https://www.geeksforgeeks.org/tkinter-cheat-sheet/

##https://www.youtube.com/watch?v=4r_XR9fUPhQ

## GitHub Copilot "font = ("Arial", 10 , "bold")", bugfix