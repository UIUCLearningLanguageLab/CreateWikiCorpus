import re

'''
clean text files from wikicorpus project (http://www.cs.upc.edu/~nlp/wikicorpus/

Example:
EXCLUDE = ['\n', 'endofarticle.']
with p.open('rb') as in_f:
    content = in_f.read().lower().decode("utf-8", 'replace')
articles = re.split('<doc.*>', content)
# clean
for article in articles[:NUM_ARTICLES]:
    if article != '':
        cleaned = remove_trailing(
            remove_non_printed_chars(
                remove_special_chars(
                    remove_html_tags(article), EXCLUDE)))


'''

# TODO determine if these functions are useful


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remove_special_chars(text, char_list):
    for char in char_list:
        text=text.replace(char,'')
    return text.replace(u'\xa0', u' ')


def remove_non_printed_chars(string):
    reg = re.compile('[^a-zA-Zа-яА-ЯёЁ,.;\s\'-]')
    return reg.sub(' <NOTPR> ', string)


def remove_trailing(string):
    # remove extra spaces, remove trailing spaces, lower the case
    return re.sub('\s+',' ',string).strip()
