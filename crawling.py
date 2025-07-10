from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Chrome 설정
options = Options()
# options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options) 

keywords = ["ai", "grit", "developer"]

all_results = []

for keyword in keywords:
    print(f"\n 키워드: {keyword}")
    url = f"https://www.ted.com/search?q={keyword}"
    driver.get(url)
    time.sleep(6)  # 충분히 로딩 기다림

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.select('div[class^="SearchResult"]')

    #print('실행확인 1차차')

    count = 0
    for result in results:
        print('실행확인 2차')
        if count >= 1:  # 1개만 크롤링
            break
        
        print(f"1차확인: {keyword}, {title_tag}, {speaker}, {link}")
        title_tag = result.select_one("h4")
        speaker_tag = result.select_one("h5")
        link_tag = result.select_one("a")

        if title_tag and speaker_tag and link_tag:
            title = title_tag.text.strip()
            speaker = speaker_tag.text.strip()
            href = link_tag["href"]
            link = "https://www.ted.com" + href if href.startswith("/") else href

            print(f"2차확인: {keyword}, {title}, {speaker}, {link}")

            print(f"{count+1}. {title} by {speaker}")
            print(link)
            print("------")

            all_results.append([keyword, title, speaker, link])
            count += 1

driver.quit()

# CSV 저장
with open("ted_top10_per_keyword.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Keyword", "Title", "Speaker", "Link"])
    writer.writerows(all_results)

print("\n CSV 저장 완료: ted_top10_per_keyword.csv")
