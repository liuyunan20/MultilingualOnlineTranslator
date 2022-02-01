import requests
from bs4 import BeautifulSoup


def choose_language():
    trans_pair = {"en": ["french", "english"], "fr": ["english", "french"]}
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
    ipt = input()
    source = trans_pair[ipt][0]
    target = trans_pair[ipt][1]
    print('Type the word you want to translate:')
    word = input()
    print(f'You chose "{target}" as a language to translate "{word}".')
    return f"https://context.reverso.net/translation/{source}-{target}/{word}"


url = choose_language()
headers = {'User-Agent': 'Mozilla/5.0'}
while True:
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        print("200 OK")
        print("Translations")
        soup = BeautifulSoup(page.content, "html.parser")
        translation_links = soup.find_all("a", {"class": "translation"})
        translations = []
        for link in translation_links:
            translations.append(link.text.replace(" ", "").replace("\n", "").replace("\r", ""))
        examples = soup.find_all("div", {"class": "example"})
        sentences = []
        for example in examples:
            exp_sentence = example.find_all("span", {"class": "text"})
            sentence = []
            for exp in exp_sentence:
                sentence.append(exp.text.strip().replace("\n", "").replace("\r", ""))
            sentences += sentence
        break
print(translations)
print(sentences)
