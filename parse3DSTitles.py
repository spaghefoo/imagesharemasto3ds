import json
from PIL import Image, ExifTags

class NintendoParseUtils:


    def __new__(cls):
        """
        Creation d'un singleton.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(NintendoParseUtils, cls).__new__(cls)
        return cls.instance



    def loopExif(self, searchTag, image):
        img = Image.open(image)
        img_exif = img.getexif()

        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                if ExifTags.TAGS[key] == searchTag:
                    return val
        
    def getModel(self, image):
        exig = self.loopExif('Model', image)
        return exig


    def is3DSOrWiiU(self, image):
        """
            Returns True if the image comes from a 3DS or False if it's from a WiiU
        """
        if self.getModel(image) == 'Nintendo 3DS':
            return True
        elif 'WiiU' in image.filename:
            return False
        else:
            raise TypeError("This image comes neither from a 3DS or a WiiU")


class Parse3DSTitles():

    def getSoftwareId(self, image):
        exig = NintendoParseUtils().loopExif('Software', image)
        if NintendoParseUtils().getModel(image) != 'Nintendo 3DS':
            raise TypeError("This image is not coming from a 3DS")
        elif exig is None:
           raise ValueError("This image is not coming from a 3DS")
        else:
           return exig

    def returnNameFromTitleID(truncated):
        
        """
        Recherche le nom a partir des 5 caracteres du champ software de EXIF.
        """
        try:
    
            print(truncated)
            # Jeux préinstallés dans la 3ds(TODO)
            if truncated == '0022n': #La guerre des Têtes
                return 'Face Raiders'
            elif truncated == '00204':
                return 'Nintendo 3DS Camera'
            elif truncated == '0022o':
                return 'RA Games' # Jeux en RA
            elif truncated == '00087': #Notes de jeu(dans le menu)
                return 'Game Notes'
            #TO BE CONTINUED...


            datas = []
            regions = ['GB', 'JP', 'KR', 'TW', 'US'] # Les differentes regions...(GB = EUR)
            for region in regions: # pour chaque region.
                db = open("title/3ds/list_"+region+".json") 
                datas.append(json.load(db))
                db.close()
            titleName = None
        except ValueError as val:
            print(val)
        except TypeError as error:
            print(error)
        else:
            searchString = "000400000"+truncated.upper()+"00" #Les games id(hors mise à jours...) se présentent comme ça : 00040000 0022o 00
            for data in datas:
                for i in data:
                    if searchString == i['TitleID']:
                        titleName = i['Name']
                        break

            if titleName is None:
                raise ValueError("This titleID isn't valid.") # Title id Pas valide si None...(la boucle s'est executé jusqu'à la fin)
            
            return titleName
    


class ParseWiiUTitles():
    
    def __returnTitleId(self,filename):
        array = filename.split('_') #Les fichiers que la WiiU envoyent on le nom avec le format WiiU_screenshot_(gamepad ou tv)_(titleId).jpg
        return array[3].split('.')[0]

    def returnNameFromTitleId(self, filename):
        titleName = None
        truncated = self.__returnTitleId(filename)
        if truncated == '004A2': # Liste des logiciels préinstallés.(TODO)
            return 'Mii Maker'
        #TO BE CONTINUED...
        db = open('title/wiiu/json')
        datas = json.load(db)
        searchString = "000500001"+truncated.lower()+"00" #Title ids(des jeux les dlc c'est different mais osef) wiiu ont ce format la...
        for data in datas:
            if searchString == data['titleID']:
                titleName = data['name']
                break

        if titleName is None:
            raise ValueError("This titleID isn't valid.")
        return titleName
    

if __name__ == '__main__':
    #ParseUtils = NintendoParseUtils()
    
    #TEST 3DS
    try:
        TitleId = Parse3DSTitles().getSoftwareId('HNI_0082_JPG.JPG')
        list = Parse3DSTitles.returnNameFromTitleID(TitleId).split()
    except ValueError as e:
        print(e)
    except FileNotFoundError as fileE:
        print(fileE)
    else:
        stri = ''.join(list).lower()
        print(stri)
    
    # TEST WIIU
    try:
        print(ParseWiiUTitles().returnNameFromTitleId("WiiU_screenshot_TV_010ED.jpg"))
    except ValueError as e:
        print(e)
    except FileNotFoundError as fileE:
        print(fileE)
    else:
        stri = ''.join(list).lower()
        print(stri)

