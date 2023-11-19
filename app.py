from selenium import webdriver
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import json


options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

try:
    jobtitlequery_input = input("Nhập tiêu đề công việc: ")
    location_input = input("Nhập địa điểm: ")

    url = f'https://www.totaljobs.com/jobs/{jobtitlequery_input}/in-{location_input}'
    driver.get(url)
    height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    driver.set_window_size(driver.get_window_size()["width"], height)
    print(url)
    driver.save_screenshot("screenshot.png")


    element_res_di2r7c = driver.find_element(By.CLASS_NAME, 'res-di2r7c')

    res_di2r7c_outer_html = element_res_di2r7c.get_attribute('outerHTML')

    doc = pq(res_di2r7c_outer_html)
    span_elements = doc('span.res-vurnku > span')
    last_span_element = span_elements[-1]
    totalPage = int(last_span_element.text)

    output_data = {
        'location': location_input,
        'job': jobtitlequery_input,
        'data': []
    }

    with open('output.json', 'w') as output_file:

        for page in range(1, totalPage + 1):
            page_url = f'{url}&page={page}'
            driver.get(page_url)

            articles = driver.find_elements(By.CLASS_NAME, 'res-1tps163')

            current_page_data = {
                'current_page': page,
                'data': []
            }

            for article in articles:
                job_title = article.find_element(By.CSS_SELECTOR, '.res-vurnku .res-nehv70').text
                job_recruitment = article.find_element(By.CLASS_NAME, 'res-1j1rn10').text
                job_location = article.find_element(By.CSS_SELECTOR, '.res-ms5eyo .res-1ejryu9 .res-1qil8oy').text
                job_location_href = article.find_element(By.CSS_SELECTOR, 'a.res-1na8b7y').get_attribute('href')

                article_data = {
                    'job_title': job_title,
                    'job_recruitment': job_recruitment,
                    'job_location': job_location,
                    'job_location_href': job_location_href
                }

                current_page_data['data'].append(article_data)

            output_data['data'].append(current_page_data)

        json.dump(output_data, output_file, indent=2)
finally:
    driver.quit()
