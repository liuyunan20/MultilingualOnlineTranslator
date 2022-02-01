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

    def choose_language(self, source, target, word):
        self.source = self.languages[source]
        self.target = self.languages[target]
        self.word = word
        print(f'You chose "{self.target}" as a language to translate "{self.word}".')
        return f"https://context.reverso.net/translation/{self.source}-{self.target}/{self.word}"

    def get_translations(self, source, target, word):
        url = self.choose_language(source, target, word)
        headers = {'User-Agent': 'Mozilla/5.0'}
        while True:
            page = requests.get(url, headers=headers)
            print(url)
            if page.status_code == 200:
                print("200 OK")

                soup = BeautifulSoup(page.content, "html.parser")
                translation_links = soup.find_all("a", {"class": "ltr"})
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
print("Type the number of language you want to translate to: ")
user_target = input()
print('Type the word you want to translate:')
user_word = input()
translator = Translator()
translator.get_translations(user_source, user_target, user_word)
