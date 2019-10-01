import re

from createwikicorpus import config


regex1 = re.compile('\n*.*<doc id=".*" url=".*" title=".*">\n([^\n]*)(.*\n*$)',
                    flags=re.S)  # make dot match newline


def get_cleaned_titles_and_bodies(output_folder_name, min_length):
    files_path = config.LocalDirs.root / output_folder_name
    print('Extracting bodies and titles in {}'.format(files_path))

    num_articles = 0
    titles = []
    bodies = []

    for file in files_path.rglob('wiki_*'):
        text = file.read_text()
        articles = re.split('</doc>', text)[:-1]
        num_articles += len(articles)

        for article in articles:

            # extract title and body
            title, body = get_title_and_body(article)

            # filter by length
            if len(body) < min_length:
                continue

            # remove trailing spaces
            body = remove_trailing_spaces(body)

            titles.append(title)
            bodies.append(body)

    assert len(bodies) == len(titles)
    print('Cleaned {} articles'.format(num_articles))

    return titles, bodies


def get_title_and_body(article):
    res = regex1.match(article)
    title = res.groups()[0]
    body = res.groups()[1]
    return title, body


def remove_trailing_spaces(string):
    """
    remove extra spaces, remove trailing spaces
    """
    return re.sub('\s+', ' ', string).strip()


