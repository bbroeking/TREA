import pandas as pd
import os
import datetime
import unicodedata
import fuzzymatcher

#########################################
#      Accented Names Dict              #
#########################################
spd = dict()
spd["Kik? Hern?ndez"] = "Kike Hernandez"
spd["Jos? Ram?rez"] = "Jose Ramirez"
spd["Aledmys D?az"] = "Aledmys Diaz"
spd["Jos? Ure?a"] = "Jose Urena"
spd["Jos? Altuve"] = "Jose Altuve"
spd["Yo?n Moncada"] = "Yoan Moncada"
spd["Christian V?zquez"] = "Christian Vazquez"
spd["Carlos Beltr?n"] = "Carlos Beltran"
spd["German M?rquez"] = "German Marquez"
spd['Od?bel Herrera'] = "Odubel Herrera"
spd['Jos? Berr?os'] = "Jose Berrios"
spd['Jesse Ch?vez'] = "Jesse Chavez"
spd['Jos? Mart?nez'] = "Jose Martinez"
spd['Henderson ?lvarez'] = "Henderson Alvarez"
spd['Yasmany Tom?s'] = "Yasmany Tomas"
spd['Andr?s Blanco'] = "Andrez Blanco"
spd['Mart?n Prado'] = "Martin Prado"
spd['Edwin Encarnaci?n'] = "Edwin Encarnacion"
spd['Mart?n P?rez'] = "Martin Perez"
spd['Eduardo N??ez'] = "Eduardo Nunez"
spd['Jaime Garc?a'] = "Jamie Garcia"
spd['Carlos G?mez'] = "Carlos Gomez"
spd['Carlos Mart?nez'] = "Carlos Martinez"
spd['Jos? Osuna'] = "Jose Osuna"
spd['Miguel Gonz?lez'] = "Miguel Gonzalez"
spd['Jes?s Sucre'] = "Jesus Sucre"
spd['Raffy L?pez'] = "Raffy Lopez"
spd['H?ctor Santiago'] = "Hector Santiago"
spd['Elias D?az'] = "Elias Diaz"
spd['Jos? Reyes'] = "Jose Reyes"
spd['Gr?gor Blanco'] = "Gregor Blanco"
spd['Miguel San?'] = "Miguel Sano"
spd['Rub?n Tejada'] = "Rubin Tejada"
spd['Jes?s Aguilar'] = "Jesus Aguilar"
spd['Sandy Le?n'] = "Sandy Leon"
spd['V?ctor Robles'] = "Victor Robles"
spd['Eugenio Su?rez'] = "Eugenio Suarez"
spd['Pedro ?lvarez'] = "Pedro Alvarez"
spd['C?sar Hern?ndez'] = "Cesar Hernandez"
spd['Adalberto Mej?a'] = 'Adalberto Mejia'
spd['Adri?n B?ltre'] = "Adrian Beltre" 
spd['Leury Garc?a'] = "Leury Garcia"
spd['Jos? Lobat?n'] = "Jose Lobaton"
spd['Jos? Quintana'] = "Jose Quintana"
spd['Jos? Pirela'] = "Jose Pirela"
spd['Jos? Iglesias'] = "Jose Iglesias"
spd['Asdr?bal Cabrera'] = "Asdrubal Cabrera"
spd['Teoscar Hern?ndez'] = "Teoscar Hernandez"
spd['Salvador P?rez'] = "Salvador Perez"
spd['Pedro Florim?n'] = "Pedro Florimon"
spd['Jos? Peraza'] = "Jose Peraza"
spd['Carlos Rod?n'] = "Carlos Rodon"
spd['Ram?n Torres'] = "Ramon Torres"
spd['Javier B?ez'] = "Javier Baez"
spd['Adri?n Gonz?lez'] = "Adrian Gonzalez"
spd['Manny Pi?a'] = "Manny Pina"
spd['Marwin Gonz?lez'] = "Marwin Gonzalez"
spd['Arismendy Alc?ntara'] = "Arismendy Alcantara"
spd['Carlos Gonz?lez'] = "Carlos Gonzalez"
spd['Michael Mart?nez'] = "Michael Martinez"
spd['Ubaldo Jim?nez'] = "Ubaldo Jimenez"
spd['Ra?l Mondesi'] = "Raul Mondesi"
spd['Yoenis C?spedes'] = "Yoenis Cespedes"
spd['Richard Ure?a'] = "Richard Urena"
spd['Yolmer S?nchez'] = "Yolmer Sanchez"
spd['Efr?n Navarro'] = "Efrin Navarro"
spd['Hern?n P?rez'] = "Hernan Perez"
spd['Marco Hern?ndez'] = "Marco Hernandez"
spd['Mart?n Maldonado'] = "Martin Maldonado"
spd['C?sar Puello'] = "Cesar Puello"
spd['Roberto P?rez'] = "Roberto Perez"
spd['Hanley Ram?rez'] = "Hanley Ramirez"
spd['Gary S?nchez'] = "Gary Sanchez"
spd['Omar Narv?ez'] = "Omar Narvaez"
spd['Jos? Abreu'] = "Jose Abreu"
spd['Ren? Rivera'] = "Rene Rivera"
spd['J?nior Guerra'] = "Junior Guerra"
spd['H?ctor S?nchez'] = "Hector Sanchez"
spd['Avisa?l Garc?a'] = "Avisail Garcia"
spd['Jos? Bautista'] = "Jose Bautista"
spd['Sean Rodr?guez'] = "Sean Rodriguez"
spd['Robinson Can?'] = "Robinson Cano"
spd['Christian V?zquez'] = "Christian Vazquez"
spd['Gio Gonz?lez'] = "Gio Gonzalez"
spd['Eduardo Rodr?guez'] = "Eduardo Rodriguez"
spd['Yandy D?az'] = "Yandy Diaz"
spd['J.C. Ram?rez'] = "J.C. Ramirez"

def accent_map(name):
    if name in spd.keys():
        return spd[name]
    return name

# In the future I might want to remember that the days on my ownerships,etc were off
# by a day so I fixed it here
set_of_things = set()
rootdir = "/Users/broeking/projects/TREA/ownerships"
for directory in os.listdir(rootdir):
    if directory == ".DS_Store":
        continue
    month = rootdir + "/" + directory
    for day in os.listdir(month):
        if "E" in day or ".DS_Store" == day:
            continue
        date = month + "/" + day
        for subdir, dirs, files in os.walk(date):
            for f in files:
                if ".DS_Store" == f:
                    continue
                datetime_date = datetime.datetime(2017, int(day.split(".")[0]), int(day.split(".")[1]))
                x = datetime_date + datetime.timedelta(days=1)
                contest = date+"/"+f
                df1 = pd.read_csv(contest)
                rotoguru = "/Users/broeking/projects/TREA/salaries/2017/" + str(x.month) + "_" + str(x.day) + "_2017.csv"
                df2 = pd.read_csv(rotoguru)
                df1 = df1.add_suffix("_left")
                df2 = df2.add_suffix("_right")

                df1['Player_left'].apply(accent_map)
                df1['Player_left'] = df1['Player_left'].str.normalize('NFKD')\
                                                       .str.encode('ascii', errors='ignore')\
                                                       .str.decode('utf-8')

                left_on = ["Player_left"]
                right_on = ["Name_right"]
                # df3 = fuzzymatcher.fuzzy_left_join(df1, df2, left_on, right_on)
                df3 = df1.merge(df2, left_on="Player_left", right_on="Name_right", how="inner")

                if not (os.path.exists(os.getcwd() + "/Ownership_Salaries/" + str(datetime_date.month) + "." + str(datetime_date.day))):
                    os.mkdir(os.getcwd() + "/Ownership_Salaries/" + str(datetime_date.month) + "." + str(datetime_date.day))

                df3.to_csv("Ownership_Salaries/" + str(datetime_date.month) + "." + str(datetime_date.day) + "/" + f)       