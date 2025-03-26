import pymorphy3

def lol(phrase):
    morph = pymorphy3.MorphAnalyzer()
    return ' '.join(morph.parse(word)[0].inflect({'gent'}).word for word in phrase.split()).capitalize()

phrase = "Английский язык"
print(lol(phrase))