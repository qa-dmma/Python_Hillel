import codecs


def delete_html_tags(html_file, result_file='cleaned.txt'):
    """
    Cleaning text from HTML tags

    :param html_file: source html page
    :param result_file: cleaned txt file output
    """
    with codecs.open(html_file, 'r', 'utf-8') as file:
        html = file.read()
        result = ""
        tag = False

        for char in html:
            if char == "<":
                tag = True
            elif char == ">":
                tag = False
            elif not tag:
                result += char
        with codecs.open(result_file, "w", 'utf-8') as f:
            f.write("\n".join(line.strip() for line in result.splitlines() if line.strip()))


delete_html_tags("HomeTask01Materials/draft.html")
