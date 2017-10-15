import re
import time
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict

round_map = {"jeopardy_round" : "First Round", "final_jeopardy_round" : "Final Jeopardy", "double_jeopardy_round" : "Second Round"}

def get_show_data(url, season):
    print("Accessing %s" % url)
    file = urlopen(url)
    html = file.read()
    file.close()
    soup = BeautifulSoup(html, 'html.parser')
    game_title = soup.find("div", {"id": "game_title"}).text
    show_number, air_date = [x.strip() for x in game_title.split("-")]
    content = soup.find("div", {"id": "content"})
    round_divs = content.find_all("div", {"id": re.compile('.*_round')})
    data = []
    for round_div in round_divs:
        round_name = round_map[round_div["id"]]
        if "Final" in round_name:
            category = round_div.find("td", {"class" : "category"})
            category_name = category.find("td", {"class" : "category_name"}).text
            div    = round_div.find("div")
            clue   = "".join(div["onmouseout"].split(",")[2:])[2:-2]
            answer = div["onmouseover"].split('<em class=\\"correct_response\\">')[1].split('</em>')[0]
            triple_stumper = "Triple Stumper" if "Triple Stumper" in div["onmouseover"] else "No"
            clue_text = BeautifulSoup(clue, 'html.parser').text.replace("\\", "")
            answer_text = BeautifulSoup(answer, 'html.parser').text
            row = OrderedDict([("season", season),
                               ("air_date", air_date),
                               ("show_number", show_number),
                               ("round_name", round_name),
                               ("category", category_name),
                               ("clue", clue_text),
                               ("answer", answer_text),
                               ("triple_stumper", triple_stumper),
                               ("clue_value", "")])
            data.append(row)
        else:
            rnd        = round_div.find("table", {"class": "round"})
            categories = rnd.find_all("td", {"class" : "category_name"})
            categories = [x.text for x in categories]
            entries    = rnd.find_all("td", {"class" : "clue"})
            for idx, entry in enumerate(entries):
                if entry.text.strip() == "":
                    clue_text = ""
                    answer_text = ""
                    triple_stumper = ""
                    clue_value = ""
                else:
                    div    = entry.find("div")
                    clue_value = div.find("td", {"class" : re.compile('clue_value.*')}).text
                    clue   = ",".join(div["onmouseout"].split(",")[2:])[2:-2]
                    clue_text = BeautifulSoup(clue, 'html.parser').text.replace("\\", "")
                    answer = div["onmouseover"].split('<em class="correct_response">')[1].split('</em>')[0]
                    triple_stumper = "Triple Stumper" if "Triple Stumper" in div["onmouseover"] else "No"
                    answer_text = BeautifulSoup(answer, 'html.parser').text
                category = categories[idx % 6]
                row      = OrderedDict([("season", season),
                                        ("air_date", air_date),
                                        ("show_number", show_number),
                                        ("round_name", round_name),
                                        ("category", category),
                                        ("clue", clue_text),
                                        ("answer", answer_text),
                                        ("triple_stumper", triple_stumper),
                                        ("clue_value", clue_value)])
                data.append(row)
    return data


def get_season_data(season):
    print("Getting Season No. %s" % season)
    season_data = []
    url         = "http://www.j-archive.com/showseason.php?season=%s" % season
    file        = urlopen(url)
    html        = file.read()
    file.close()
    soup        = BeautifulSoup(html, 'html.parser')
    content     = soup.find("div", {"id": "content"})
    ignores     = ["College", "Celebrity", "Back to School", "Teen"]
    shows       = content.find_all("tr")
    failures    = []
    for show in shows:
        if any([x in show.text for x in ignores]):
            continue
        else:
            show_url = show.find("a")["href"]
            try:
                season_data.extend(get_show_data(show_url, season))
            except:
                failures.append(show_url)
                print(traceback.format_exc())
            time.sleep(3)
    # retry failures
    for failure in failures:
        try:
            season_data.extend(get_show_data(failure, season))
        except:
            print("Cannot access %s" % failure)
    return season_data


def main():
    seasons = range(23, 35, 1)   # get data from 23rd to 35th seasons (2008 to 2017)
    for season in seasons:
        data = get_season_data(season)
        df   = pd.DataFrame(data)
        df.to_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_%s.csv" % season)

def unite():
    seasons = range(23, 35)
    df_list = []
    for season in seasons:
        df = pd.read_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_%s.csv" % season, encoding='latin1')
        df_list.append(df)
    df_final = pd.concat(df_list)
    df_final.to_csv(r"C:\Users\alexschindele\Documents\jeopardy_data_season_all.csv")

if __name__ == "__main__":
    unite()
    # main()
    test = False
    if test:
        import pprint
        pprint.pprint(get_show_data("http://www.j-archive.com/showgame.php?game_id=1950", 22))