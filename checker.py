import requests
from bs4 import BeautifulSoup as bs

def mfa_parse():
  url = "https://france.mfa.gov.ua/"
  headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-platform': '"Windows"'
    }
  response = requests.get(url, headers=headers)
  soup = bs(response.text, "html.parser")
  text_box = soup.find("div", class_="slider_main__col slider_main__text")
  date = text_box.find("p", class_="slider_main__date").contents[0]
  link = url + text_box.find("a")['href']
  text = text_box.find("a").contents[0]
  return({
    "date": date,
    "link": link,
    "text": text
  })

if __name__ == "__main__":
  print(mfa_parse()["text"])
  