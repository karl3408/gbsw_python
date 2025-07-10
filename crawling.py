from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)

keywords = ["ai", "grit", "developer"]
all_results = []

for keyword in keywords:
    url = f"https://www.ted.com/search?q={keyword}"
    driver.get(url)
    time.sleep(6)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 아래 selector는 실제 구조에 맞게 수정 필요!
    results = soup.select('div.search__result__content')
    print(f"{keyword} 검색 결과 개수: {len(results)}")

    count = 0
    for result in results:
        if count >= 1:  # 1개만 수집. 10개 원하면 10으로 수정
            break

        title_tag = result.select_one("a[data-ga-context='talks']")
        speaker_tag = result.select_one("span.search__result__speaker")
        link_tag = result.select_one("a[data-ga-context='talks']")

        if title_tag and speaker_tag and link_tag:
            title = title_tag.text.strip()
            speaker = speaker_tag.text.strip()
            href = link_tag["href"]
            link = "https://www.ted.com" + href if href.startswith("/") else href

            all_results.append([keyword, title, speaker, link])
            count += 1

driver.quit()

with open("ted_top10_per_keyword.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Keyword", "Title", "Speaker", "Link"])
    writer.writerows(all_results)

print("\nCSV 저장 완료: ted_top10_per_keyword.csv")