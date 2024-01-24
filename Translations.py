import json
class Translations():

    def __init__(self):
        # Shall language be two letter codes...(fr, en, de, etc)
        db = open('translations/translations.json')
        self.translations = json.load(db)
        self.language = []

    def returnTranslation(self,language='en'):
        # Liste des languages supportés(tuple)
        
        supportedLocales = ('fr', 'en', 'de', 'it')
        previouslyUsedLocales = []
        # Petite optimisation, on tourne la boucle uniquement si le language n'a pas été set avant
        if language not in self.language:
            for locale in supportedLocales:
                if language.find(locale):
                    self.language.append(locale)
                    break
                else:
                    language = 'en'
                    self.language.append('en')
        #TO BE CONTINUED.
        return self.translations[f"{language}"]


if __name__ == '__main__':
    translations = Translations()
    array = translations.returnTranslation('dd')

    print(array)