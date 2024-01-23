import json
class Translations():

    def __init__(self):
        # Shall language be two letter codes...(fr, en, de, etc)
        db = open('translations/translations.json')
        self.translations = json.load(db)

    def returnTranslation(self,language):
        supportedLocales = ['fr', 'en', 'de', 'it']
        for locale in supportedLocales:
            if locale in language:
                language = locale
                break
            else:
                language = 'en'
        #TO BE CONTINUED.
        return self.translations[f"{language}"]


if __name__ == '__main__':
    translations = Translations()
    array = translations.returnTranslation('en')
    print(array)