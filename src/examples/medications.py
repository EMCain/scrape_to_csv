from string import ascii_lowercase
from requests import get
from bs4 import BeautifulSoup
import re

from compile.compile_results import ResultCompiler

def url_generator():
    url_base = "https://druginfo.nlm.nih.gov/drugportal/drug/names/"
    for letter in ascii_lowercase:
        yield url_base + letter 

def parse_result(page_text, page_url):
    letter_match = re.match(r"https://druginfo.nlm.nih.gov/drugportal/drug/names/(?P<letter>[a-z])", page_url)
    letter = letter_match.groups("letter")[0]

    soup = BeautifulSoup(page_text, features="html.parser")
    table = soup.find(
        "table", {"role": "presentation"}
    ).find("table", {"border": "1"})
    anchors = table.find_all("a")

    meds = ", ".join([a.string for a in anchors])
    count = len(anchors)

    return {
        "Letter": letter,
        "Count": count,
        "List of Meds": meds
    }

def save_results():
    rc = ResultCompiler(
        url_iterable=url_generator(),
        project_name="meds_example",
        column_names=["Letter", "Count", "List of Meds"],
        parse_callback=parse_result
    )
    rc.write_results()

if __name__ == "__main__":
    save_results()
