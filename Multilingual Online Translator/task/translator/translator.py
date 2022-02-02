import requests
from bs4 import BeautifulSoup
import sys


class Translator:
    languages = ["arabic", "german", "english",
                 "spanish", "french", "hebrew",
                 "japanese", "dutch", "polish",
                 "portuguese", "romanian", "russian",
                 "turkish"]

    def __init__(self):
        self.source = None
        self.target = None
        self.word = None
        self.translations = []

    def choose_language(self, source, target, word):
        self.source = source
        self.target = target
        self.word = word
        return f"https://context.reverso.net/translation/{self.source}-{self.target}/{self.word}"

    def get_translations(self, source, target, word):
        url = self.choose_language(source, target, word)
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(url, headers=headers)
        if page.status_code == 404:
            print(f"Sorry, unable to find {self.word}")
        elif page.status_code == 200:
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
        else:
            print("Something wrong with your internet connection")

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
                if page.status_code == 404:
                    print(f"Sorry, unable to find {self.word}")
                elif page.status_code == 200:
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
                else:
                    print("Something wrong with your internet connection")


user_source = sys.argv[1]
user_target = sys.argv[2]
user_word = sys.argv[3]
translator = Translator()
if user_target not in translator.languages and user_target != "all":
    print(f"Sorry, the program doesn't support {user_target}")
if user_target == "all":
    translator.translate_all(user_source, user_word)
else:
    translator.get_translations(user_source, user_target, user_word)
translator.print_and_save()
