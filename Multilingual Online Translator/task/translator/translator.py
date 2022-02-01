import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self, ipt, word):
        self.ipt = ipt
        self.source = None
        self.target = None
        self.word = word

    def choose_language(self):
        trans_pair = {"en": ["french", "english"], "fr": ["english", "french"]}

        self.source = trans_pair[self.ipt][0]
        self.target = trans_pair[self.ipt][1]

        return f"https://context.reverso.net/translation/{self.source}-{self.target}/{self.word}"

    def get_translations(self):
        print(f'You chose "{self.target}" as a language to translate "{self.word}".')
        url = self.choose_language()
        headers = {'User-Agent': 'Mozilla/5.0'}
        while True:
            page = requests.get(url, headers=headers)
            if page.status_code == 200:
                print("200 OK")

                soup = BeautifulSoup(page.content, "html.parser")
                translation_links = soup.find_all("a", {"class": "translation"})
                print(f"{self.target} Translations:")
                for link in translation_links:
                    print(link.text.replace(" ", "").replace("\n", "").replace("\r", ""))
                print()
                examples = soup.find_all("div", {"class": "example"})
                print(f"{self.target} Examples:")
                for example in examples:
                    exp_sentence = example.find_all("span", {"class": "text"})
                    for exp in exp_sentence:
                        print(exp.text.strip().replace("\n", "").replace("\r", ""))
                    print()
                break


print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
user_target = input()
print('Type the word you want to translate:')
user_word = input()
translator = Translator(user_target, user_word)
translator.choose_language()
translator.get_translations()
