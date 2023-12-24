def parse_constitution(path_to_chromedriver):
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    from time import sleep
    import requests
    import datetime as dt

    from lxml import etree

    from selenium import webdriver as wb
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    from IPython.display import clear_output
    from dateutil.parser import parse

    s = Service(path_to_chromedriver)
    br = wb.Chrome(service=s)

    url = 'http://www.vybory.izbirkom.ru/region/izbirkom'
    br.get(url)

    # Открываем вкладку с фильтрами
    filters_show = br.find_element(By.CSS_SELECTOR, ".filter")

    filters_show.click()

    # Проставляем временные ограничения для поиска. Вставленные значения - для примера. Это просто переменные, куда пойдет
    # введенная пользователем инфа
    inp_start_date = '01.01.2020'
    inp_end_date = '31.12.2020'
    date_start = parse(inp_start_date, dayfirst=True)
    date_finish = parse(inp_end_date, dayfirst=True)
    # Проверяем, что дата начала не позже даты конца
    if date_start > date_finish:
        print('ERROR')
        assert False, f'Дата начала ({date_start.strftime("%Y-%m-%d")}) не может быть позже даты конца ({date_finish.strftime("%Y-%m-%d")})'

    start_date = br.find_element(By.CSS_SELECTOR, "#start_date")
    start_date.clear()
    start_date.send_keys(inp_start_date)

    end_date = br.find_element(By.CSS_SELECTOR, "#end_date")
    end_date.clear()
    end_date.send_keys(inp_end_date)

    # Устанавливаем значение фильтра по уровню выборов.
    elect_level = br.find_element(By.CSS_SELECTOR, ".select2-search__field")
    elect_level_allopt = ['Федеральный', "Региональный", 'Административный центр', 'Местное самоуправление']
    elect_level_useropt = ['Федеральный']

    for i in elect_level_useropt:
        elect_level.send_keys(i)
        elect_level.send_keys(Keys.ENTER)
        elect_level.clear()

    # Фильтр на вид выборов
    elect_vid_allopt = ['Референдум', 'Выборы на должность', 'Выборы депутата', 'Отзыв депутата',
                        'Отзыв должностного лица', 'Голосование']
    elect_vid_useropt = []

    elect_vid = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-vidvibref-container']")
    for i in elect_vid_useropt:
        elect_vid.send_keys(i)
        elect_vid.send_keys(Keys.ENTER)
        elect_vid.clear()

    # Фильтр на тип выборов
    elect_type_allopt = ['Основные', 'Основные повторные', 'Основные отложенные',
                         'Основные отдельные', 'Дополнительные', 'Дополнительные повторные', 'Довыборы',
                         'Повторное голосование', 'Повторное голосование', 'Основные выборы и повторное голосование']
    elect_type_useropt = []

    elect_type = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-vibtype-container']")
    for i in elect_type_useropt:
        elect_type.send_keys(i)
        elect_type.send_keys(Keys.ENTER)
        elect_type.clear()

    # Фильтр на существующие сейчас субъекты
    elect_actreg_allopt = ['Адыгея', 'Алтай', 'Башкортостан', 'Бурятия', 'Дагестан', 'Донецкая Народная Республика',
                           'Ингушетия', 'Кабардино-Балкарская', 'Калмыкия', 'Карачаево-Черкесская', 'Карелия', 'Коми',
                           'Крым',
                           'Луганская Народная Республика', 'Марий Эл', 'Мордовия', 'Саха (Якутия)', 'Северная Осетия',
                           'Татарстан', 'Тыва', 'Удмуртская',
                           'Хакасия', 'Чеченская', 'Чувашская', 'Алтайский край', 'Забайкальский край',
                           'Камчатский край', 'Краснодарский край',
                           'Красноярский край', 'Пермский край', 'Приморский край', 'Ставропольский край',
                           'Хабаровский край', 'Амурская область',
                           'Архангельская область', 'Астраханская область', 'Белгородская область', 'Брянская область',
                           'Владимирская область',
                           'Волгоградская область', 'Вологодская область', 'Воронежская область', 'Запорожская область',
                           'Ивановская область',
                           'Иркутская область', 'Калининградская область', 'Калужская область', 'Кемеровская область',
                           'Кировская область',
                           'Костромская область', 'Курганская область', 'Курская область', 'Ленинградская область',
                           'Липецкая область',
                           'Магаданская область', 'Московская область', 'Мурманская область', 'Нижегородская область',
                           'Новгородская область',
                           'Новосибирская область', 'Омская область', 'Оренбургская область', 'Орловская область',
                           'Пензенская область',
                           'Псковская область', 'Ростовская область', 'Рязанская область', 'Самарская область',
                           'Саратовская область',
                           'Сахалинская область', 'Свердловская область', 'Смоленская область', 'Тамбовская область',
                           'Тверская область',
                           'Томская область', 'Тульская область', 'Тюменская область', 'Ульяновская область',
                           'Херсонская область', 'Челябинская область',
                           'Ярославская область', 'Москва', 'Санкт-Петербург', 'Севастополь', 'Еврейская', 'Ненецкий',
                           'Ханты-Мансийский',
                           'Чукотский', 'Ямало-Ненецкий', 'Российская Федерация', 'Федеральная территория Сириус']

    # elect_actreg_useropt = ['Адыгея']
    elect_actreg_useropt = elect_actreg_allopt[:]

    elect_actreg = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-actual_regions_subjcode-container']")
    for i in elect_actreg_useropt:
        elect_actreg.send_keys(i)
        br.implicitly_wait(1)
        elect_actreg.send_keys(Keys.ENTER)
        br.implicitly_wait(1)
        elect_actreg.clear()

    # Фильтр на упраздненные субъекты
    elect_oldreg_allopt = ['Камчатская область', 'Пермская область', 'Читинская область',
                           'Агинский Бурятский автономный округ', 'Коми-Пермяцкий автономный округ',
                           'Корякский автономный округ', 'Таймырский (Долгано-Ненецкий) автономный округ',
                           'Усть-Ордынский Бурятский автономный округ', 'Эвенкийский автономный округ']
    # elect_oldreg_useropt = []
    elect_oldreg_useropt = elect_oldreg_allopt[:]

    elect_oldreg = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-old_regions_subjcode-container']")
    for i in elect_oldreg_useropt:
        elect_oldreg.send_keys(i)
        sleep(1)
        br.implicitly_wait(5)
        elect_oldreg.send_keys(Keys.ENTER)
        elect_oldreg.clear()

    # Фильтр на электоральную систему
    # По какой-то причине поисковая строка не воспринимает слишком длинные названия, поэтому пользователю надо показать
    # полные, но на сайте ввести частично
    elect_syst_allopt_f = ['Мажоритарная',
                           'Мажоритарная - по общерегиональному округу и по отдельным избирательным округам',
                           'Мажоритарная по общерегиональному округу', 'Пропорциональная',
                           'Смешанная - пропорциональная и мажоритарная',
                           'Пропорциональная и мажоритарная по общерегиональному избирательному округу и отдельным избирательным округам']
    elect_syst_allopt_site = ['Мажоритарная', 'Мажоритарная - по общерегиональному округу',
                              'Мажоритарная по общерегиональному округу', 'Пропорциональная',
                              'Смешанная - пропорциональная и мажоритарная',
                              'Пропорциональная и мажоритарная по общерегиональному']

    # elect_syst_useropt = []
    elect_syst_useropt = elect_syst_allopt_site[:]

    elect_syst = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-sxemavib-container']")
    for i in elect_syst_useropt:
        elect_syst.send_keys(i)
        sleep(1)
        br.implicitly_wait(5)
        elect_syst.send_keys(Keys.ENTER)
        elect_syst.clear()

    # Нажимаем на кнопку поиска
    search_button = br.find_element(By.ID, "calendar-btn-search")
    search_button.click()

    # выбираем нужные выборы
    elections_button = br.find_element(By.CSS_SELECTOR,
                                       "#vibory > ul > li:nth-child(2) > div > div.col-12.col-md-8 > a")
    elections_button.click()

    page = br.page_source
    soup = BeautifulSoup(page)
    dom = etree.HTML(str(soup))

    regions = soup.find_all('li', attrs={'id': '100100163596969'})[0]

    links = set()

    for region in regions.find_all('li'):
        rel_link = region.find_all('a')[1].get('href')  # link
        full_link = 'http://www.vybory.izbirkom.ru/' + rel_link
        links.add(full_link)
        # break

    print(f'[INFO] найдено {len(links)} ссылок')

    for i, link in enumerate(links):
        # url = 'http://www.vybory.izbirkom.ru/region/izbirkom'
        # br.get(link)
        br = wb.Chrome(service=s)

        br.get(link)
        sleep(10)
        # выбираем раздел с результатами
        results_button = br.find_element(By.CSS_SELECTOR, "#vote-results-name")
        results_button.click()
        sleep(10)
        # выбираем нужное представление данных ("Сводная таблица итогов голосования")
        table_button = br.find_element(By.CSS_SELECTOR,
                                       r"#vote-results > table > tbody > tr.trReport.\32 0200701 > td > a")
        table_button.click()
        sleep(10)
        page = br.page_source
        soup = BeautifulSoup(page)
        # dom = etree.HTML(str(soup))
        # info = soup.find_all('div', attrs={'class': 'row tab-pane active show'})[0]
        commission_name = soup.find_all('table', attrs={'class': 'table-borderless', 'width': "100%"})[0].find_all('td',
                                                                                                                   attrs={
                                                                                                                       'class': 'text-center'})[
            0].text.strip()
        vote_data = soup.find_all('div', attrs={'class': 'table-wrapper'})[
            0]  # .find_all('td', attrs={'class': 'text-center'})[0].text.strip()
        sub_level_names = []

        # здесь можно в a href собрать ссылки на уровень ниже
        for sub_level_name in vote_data.find_all('th', attrs={'class': 'text-center'}):
            sub_level_names.append(sub_level_name.text)

        participation = []

        rows = vote_data.find_all('tr')

        for row in rows:
            cols = row.find_all('td', attrs={'align': 'right'})
            if len(cols) == 0:
                continue
            # break
            participation.append([col.text for col in cols])

        results_abs = []
        results_percent = []

        for row in rows:
            cols = row.find_all('td', attrs={'class': 'text-right'})
            if len(cols) == 0:
                continue
            # break
            results_abs.append([col.text.split()[0] for col in cols])
            results_percent.append([col.text.split()[1][:-1] for col in cols])  # чтобы избавиться от процента

        df = pd.DataFrame(
            {'region': [commission_name] * len(sub_level_names[1:]),
             'commission_name': sub_level_names[1:],
             'voters_number': participation[0],
             'issued_ballots_number': participation[1],
             'turned_ballots_number': participation[2],
             'bad_ballots_number': participation[3],
             'for_votes_number': results_abs[0],
             'for_votes_percent': results_percent[0],
             'against_votes_number': results_abs[1],
             'against_votes_percent': results_percent[1]
             }
        )

        df['for_votes_percent'] = df['for_votes_percent'].str.replace(',', '.')
        df['against_votes_percent'] = df['against_votes_percent'].str.replace(',', '.')

        if i == 0:
            stacked_df = df.copy()
        else:
            stacked_df = pd.concat([stacked_df, df])

    stacked_df.to_csv('result_constitution.csv', encoding='utf-8', index=False)

    return stacked_df




