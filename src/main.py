from datetime import datetime, timedelta
from email import message
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from jinja2 import Template

from src.utils.helper_email import send_email

driver = Chrome('PATH')

def date_format(some_date):
    if some_date < 10:
        return f'0{some_date}'
    else: return some_date

def main():
    full_name_accused = input('ФИО - ')
    email_accused = input('Почта - ')
    for i in range(0, 60):
        dt = datetime.now() + timedelta(days=i)
        day = date_format(dt.day)
        month = date_format(dt.month)
        
        url = f"https://hmray--hmao.sudrf.ru/modules.php?name=sud_delo&srv_num=1&H_date={day}.{month}.{dt.year}"
        driver.get(url)
        sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        try:
            trs = soup.find('div', id='tablcont').findAll('tr')
        except:
            continue
        information = []
        details = ''
        for tr in trs:
            if tr.text.find(f'{full_name_accused}') != -1:
                list_case = tr.findAll('td')
                url_lawlessness = 'https://hmray--hmao.sudrf.ru/' + list_case[1].find('a').get('href')
                information.append(list_case[1].text)
                information.append(list_case[2].text)
                information.append(list_case[4].text)
                information.append(list_case[5].text)
                information.append(list_case[6].text)

                driver.get(url_lawlessness)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                
                for i in range(1, 6):
                    try:
                        details += f"{soup.find('div', id=f'cont{i}').find('table')} <br><br>"
                    except:
                        continue

                date_court_session = f'{day}.{month}.{dt.year}'
                header_one = f'Дорогая {" ".join(full_name_accused.split()[1:])}, приглашаем Вас {date_court_session} в г. Ханты-Мансийск, ул. Ленина, д. 63 к {information[1]} на мероприятие под названием "суд по административному делу"!'
                with open('templates/email.html', 'r') as f:
                    page = Template(f.read())
                message = page.render(header_one=header_one, number_case=information[0], time_court_session=information[1], \
                                    case_info=information[2], fake_judge=information[3], result_court=information[4], details=details)
                
                send_email(email_accused, message, date_court_session)
                print('send email', date_court_session)
            




if __name__ == '__main__':
    main()