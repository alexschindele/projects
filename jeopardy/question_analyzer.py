import re
import RAKE
import pandas as pd
from collections import Counter
Rake = RAKE.Rake(RAKE.SmartStopList())

# variable choose between "clue", "answer", "category"
def test(variable):
    df = pd.read_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_all.csv", encoding='latin1')
    df = df[df["triple_stumper"] == "Triple Stumper"]
    cnt = Counter()
    clues = [x for x in list(df[variable]) if isinstance(x, str)]
    clues = list(set(clues))
    for clue in clues:
        keywords = sorted(Rake.run(clue), key=lambda x: x[1])
        if len(keywords):
            keyword = keywords[-1][0]
            if "clue crew" not in keyword:
                cnt[keyword] += 1
    return cnt


def triple_stump_categories(variable):
    df = pd.read_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_all.csv", encoding='latin1')
    df = df[df["triple_stumper"] == "Triple Stumper"]
    cnt = Counter()
    clues = [x for x in list(df[variable]) if isinstance(x, str)]
    # clues = list(set(clues))
    for clue in clues:
        cnt[clue] += 1
    return cnt

def most_common_categories():
    df = pd.read_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_all.csv", encoding='latin1')
    df = df[df["round_name"] != "Final Jeopardy"]
    cnt = Counter()
    clues = [x for x in list(df["category"]) if isinstance(x, str)]
    # clues = list(set(clues))
    for clue in clues:
        cnt[clue] += 1
    for key in cnt:
        cnt[key] /= 5
    return cnt


def data_scrub(ls):
    nonwords = ["the ", "a ", "an ", '"',]
    regex = "[\(\[].*?[\)\]]"
    ls_new = []
    for string in ls:
        string = string.lower()
        string = re.sub(regex, "", string)
        # for nw in nonwords:
        #     string = string.replace(nw, "")
        string = string.strip()
        ls_new.append(string)
    return ls_new

def most_common_answers():
    df = pd.read_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_all.csv", encoding='latin1')
    cnt = Counter()
    clues = [x for x in list(df["answer"]) if isinstance(x, str)]
    # clues = list(set(clues))
    clues = data_scrub(clues)
    for clue in clues:
        cnt[clue] += 1
    return cnt

import pprint
pprint.pprint(most_common_answers().most_common(100))
# print(most_common_categories().most_common(50))
# print(triple_stump_categories("category").most_common(50))
# print(test("category").most_common(50))

# print(sorted(Rake.run('"Twelfth Night" opens with, "If music be the food of love," do this'), key=lambda x: x[1])[-1][0])
# print(Rake.run("THE NEW YORK TIMES MAGAZINE"))
# print(Rake.run("I'VE TRAVELED EACH & EVERY HIGHWAY"))

