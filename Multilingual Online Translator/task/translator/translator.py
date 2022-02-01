import requests
from bs4 import BeautifulSoup


class Translator:
    languages = {"1": "arabic", "2": "german", "3": "english",
                 "4": "spanish", "5": "french", "6": "hebrew",
                 "7": "japanese", "8": "dutch", "9": "polish",
                 "10": "portuguese", "11": "romanian", "12": "russian",
                 "13": "turkish"}

    def __init__(self):
        self.source = None
        self.target = None
        self.word = None
        self.translations = []
        self.sentences = []

    def choose_language(self, source, target, word):
        self.source = self.languages[source]
        self.target = self.languages[target]
        self.word = word
        return f"https://context.reverso.net/translation/{self.source}-{self.target}/{self.word}"

    def get_translations(self, source, target, word):
        url = self.choose_language(source, target, word)
        headers = {'User-Agent': 'Mozilla/5.0'}
        while True:
            page = requests.get(url, headers=headers)
            print(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                # get word translations, save in a list
                translation_links = soup.find_all("a", {"class": "translation"})
                for link in translation_links:
                    self.translations.append(link.text.replace(" ", "").replace("\n", "").replace("\r", ""))
                # get example sentences, save in a list
                examples = soup.find_all("div", {"class": "example"})
                for example in examples:
                    exp_sentence = example.find_all("span", {"class": "text"})
                    sentence = []
                    for exp in exp_sentence:
                        sentence.append(exp.text.strip().replace("\n", "").replace("\r", ""))
                    self.sentences += sentence
                break

    def save_translations(self):
        with open(f"{self.word}.txt", "a") as tran_file:
            tran_file.writelines(self.translations)
            tran_file.writelines(self.sentences)

    def print_translations(self):
        print(f"{self.target} Translations:")
        for translation in self.translations:
            if translation != "Translation":
                print(translation)
        print()
        print(f"{self.target} Examples:")
        for sentence in self.sentences:
            print(sentence)
        print()

    def translate_all(self, source, word):
        for x in self.languages:
            if x != source:
                # self.get_translations(source, x, word)
                # print(f"{self.target} Translations:")
                # print(self.translations[1])
                # print()
                # print(f"{self.target} Example:")
                # print(self.sentences[0])
                # print(self.sentences[1])
                # print()
                url = self.choose_language(source, x, word)
                headers = {'User-Agent': 'Mozilla/5.0'}
                page = requests.get(url, headers=headers)
                print(url)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, "html.parser")
                    translation_links = soup.find_all("a", {"class": "translation"})
                    for link in translation_links:
                        self.translations.append(link.text.replace(" ", "").replace("\n", "").replace("\r", ""))
                    print(f"{self.target} Translations:")
                    print(self.translations[1])
                    print()
                    example = soup.find("div", {"class": "example"})
                    print(f"{self.target} Example:")
                    exp_sentence = example.find_all("span", {"class": "text"})
                    for exp in exp_sentence:
                        print(exp.text.strip().replace("\n", "").replace("\r", ""))
                        self.sentences.append(exp.text.strip().replace("\n", "").replace("\r", ""))
                    print()


print('''Hello, you're welcome to the translator. Translator supports: 
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
Type the number of your language: ''')
user_source = input()
print("Type the number of language you want to translate to or '0' to translate to all languages: ")
user_target = input()
print('Type the word you want to translate:')
user_word = input()
translator = Translator()
if user_target == "0":
    translator.translate_all(user_source, user_word)
else:
    translator.get_translations(user_source, user_target, user_word)
    translator.print_translations()
translator.save_translations()
