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
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                # get word translations, save in a list
                self.translations.append(f"{self.target.capitalize()} Translations:\n")
                translation_links = soup.find_all("a", {"class": "translation"})
                for i in range(1, len(translation_links)):
                    self.translations.append(translation_links[i].text.strip().replace("\n", "").replace("\r", "") + "\n")
                self.translations.append("\n")
                # get example sentences, save in a list
                self.translations.append(f"{self.target.capitalize()} Examples:\n")
                examples = soup.find_all("div", {"class": "example"})
                for example in examples:
                    exp_sentence = example.find_all("span", {"class": "text"})
                    sentence = []
                    for exp in exp_sentence:
                        sentence.append(exp.text.strip().replace("\n", "").replace("\r", "") + "\n")
                    self.translations += sentence
                break

    def print_and_save(self):
        print(*self.translations, sep="")
        with open(f"{self.word}.txt", "w", encoding="utf-8") as tran_file:
            print(*self.translations, sep="", file=tran_file)

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
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, "html.parser")
                    translation_links = soup.find_all("a", {"class": "translation"})
                    x_translations = []
                    for link in translation_links:
                        x_translations.append(link.text.strip().replace("\n", "").replace("\r", ""))
                    self.translations.append(f"{self.target.capitalize()} Translations:\n")
                    self.translations.append(x_translations[1] + "\n")
                    self.translations.append("\n")
                    example = soup.find("div", {"class": "example"})
                    self.translations.append(f"{self.target.capitalize()} Example:\n")
                    exp_sentence = example.find_all("span", {"class": "text"})
                    for exp in exp_sentence:
                        self.translations.append(exp.text.strip().replace("\n", "").replace("\r", "") + "\n")
                    self.translations.append("\n")


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
translator.print_and_save()
