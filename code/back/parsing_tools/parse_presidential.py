def parse_presidential(path_to_chromedriver):
    """
    Функция для парсинга результатов выборов президента РФ в 2004, 2008, 2012 и 2018 годах
    :param path_to_chromedriver: локальный путь к драйверу для работы selenium
    :return: х4 pandas.DataFrame с результатами выборов по всем регионам РФ на момент выборов
    с разбивкой по ТИК-ам
    """
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

    from parsing_presidential_tools.parse_2004_presidential_elections import parse_2004_presidential_elections
    from parsing_presidential_tools.parse_2008_presidential_elections import parse_2008_presidential_elections
    from parsing_presidential_tools.parse_2012_presidential_elections import parse_2012_presidential_elections
    from parsing_presidential_tools.parse_2018_presidential_elections import parse_2018_presidential_elections

    from IPython.display import clear_output
    from dateutil.parser import parse

    # Запускаем Google Chrome в автоматическом режиме
    s = Service(path_to_chromedriver)
    br = wb.Chrome(service=s)

    # Открываем стартовую страницу раздела с результатами выборов
    url = 'http://www.vybory.izbirkom.ru/region/izbirkom'
    br.get(url)

    # Открываем вкладку с фильтрами
    filters_show = br.find_element(By.CSS_SELECTOR, ".filter")
    filters_show.click()

    # Проставляем временные ограничения для поиска, берем даты, в которые входят
    # все выборы президента
    inp_start_date = '01.01.2000'
    inp_end_date = '31.12.2023'
    # Парсим даты
    date_start = parse(inp_start_date, dayfirst=True)
    date_finish = parse(inp_end_date, dayfirst=True)
    # Проверяем, что дата начала не позже даты конца (сделано для масштабирования в будущем)
    if date_start > date_finish:
        print('ERROR')
        assert False, f'Дата начала ({date_start.strftime("%Y-%m-%d")}) не может быть позже даты конца ({date_finish.strftime("%Y-%m-%d")})'

    # Вставляем даты в фильтр
    start_date = br.find_element(By.CSS_SELECTOR, "#start_date")
    start_date.clear()
    start_date.send_keys(inp_start_date)

    sleep(5)

    end_date = br.find_element(By.CSS_SELECTOR, "#end_date")
    end_date.clear()
    end_date.send_keys(inp_end_date)

    # Устанавливаем значение фильтра по уровню выборов
    elect_level = br.find_element(By.CSS_SELECTOR, ".select2-search__field")
    # Доступные поля
    elect_level_allopt = ['Федеральный', "Региональный", 'Административный центр', 'Местное самоуправление']
    elect_level_useropt = ['Федеральный']  # выбираем федеральный

    for i in elect_level_useropt:
        elect_level.send_keys(i)
        elect_level.send_keys(Keys.ENTER)
        sleep(5)
        elect_level.clear()

    # Фильтр на вид выборов
    elect_vid_allopt = ['Референдум', 'Выборы на должность', 'Выборы депутата', 'Отзыв депутата',
                        'Отзыв должностного лица', 'Голосование']
    elect_vid_useropt = []

    elect_vid = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-vidvibref-container']")
    for i in elect_vid_useropt:
        elect_vid.send_keys(i)
        elect_vid.send_keys(Keys.ENTER)
        sleep(5)
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
        sleep(5)
        elect_type.clear()

    # Фильтр на существующие сейчас субъекты
    elect_actreg_allopt = [
        'Адыгея', 'Алтай', 'Башкортостан', 'Бурятия', 'Дагестан', 'Донецкая Народная Республика', 'Ингушетия',
        'Кабардино-Балкарская', 'Калмыкия', 'Карачаево-Черкесская', 'Карелия', 'Коми', 'Крым',
        'Луганская Народная Республика', 'Марий Эл', 'Мордовия', 'Саха (Якутия)', 'Северная Осетия', 'Татарстан',
        'Тыва', 'Удмуртская', 'Хакасия', 'Чеченская', 'Чувашская', 'Алтайский край', 'Забайкальский край',
        'Камчатский край', 'Краснодарский край', 'Красноярский край', 'Пермский край', 'Приморский край',
        'Ставропольский край', 'Хабаровский край', 'Амурская область', 'Архангельская область', 'Астраханская область',
        'Белгородская область', 'Брянская область', 'Владимирская область', 'Волгоградская область',
        'Вологодская область', 'Воронежская область', 'Запорожская область', 'Ивановская область', 'Иркутская область',
        'Калининградская область', 'Калужская область', 'Кемеровская область', 'Кировская область',
        'Костромская область', 'Курганская область', 'Курская область', 'Ленинградская область', 'Липецкая область',
        'Магаданская область', 'Московская область', 'Мурманская область', 'Нижегородская область',
        'Новгородская область', 'Новосибирская область', 'Омская область', 'Оренбургская область', 'Орловская область',
        'Пензенская область', 'Псковская область', 'Ростовская область', 'Рязанская область', 'Самарская область',
        'Саратовская область', 'Сахалинская область', 'Свердловская область', 'Смоленская область',
        'Тамбовская область',
        'Тверская область', 'Томская область', 'Тульская область', 'Тюменская область', 'Ульяновская область',
        'Херсонская область', 'Челябинская область',
        'Ярославская область', 'Москва', 'Санкт-Петербург', 'Севастополь', 'Еврейская', 'Ненецкий', 'Ханты-Мансийский',
        'Чукотский', 'Ямало-Ненецкий', 'Российская Федерация', 'Федеральная территория Сириус']

    elect_actreg_useropt = elect_actreg_allopt[:]  # выбираем все

    elect_actreg = br.find_element(By.CSS_SELECTOR, "[aria-describedby='select2-actual_regions_subjcode-container']")
    for i in elect_actreg_useropt:
        elect_actreg.send_keys(i)
        sleep(1)  # немного ждем
        br.implicitly_wait(5)
        elect_actreg.send_keys(Keys.ENTER)
        sleep(1)  # немного ждем
        br.implicitly_wait(5)
        elect_actreg.clear()
        sleep(1)

    # Фильтр на упраздненные субъекты
    elect_oldreg_allopt = ['Камчатская область', 'Пермская область', 'Читинская область',
                           'Агинский Бурятский автономный округ', 'Коми-Пермяцкий автономный округ',
                           'Корякский автономный округ', 'Таймырский (Долгано-Ненецкий) автономный округ',
                           'Усть-Ордынский Бурятский автономный округ', 'Эвенкийский автономный округ']

    elect_oldreg_useropt = []  # не выбираем

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

    elect_syst_useropt = []  # не выбираем

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

    # Забираем код страницы
    page = br.page_source
    soup = BeautifulSoup(page)
    dom = etree.HTML(str(soup))

    # все найденные выборы
    elections = soup.find_all('ul', attrs={'class': 'list-group list-group-flush vibory-list'})[0]

    # Собираем ссылки на страницы с выборами каждого года
    elections_links = list()

    for election in elections.find_all('li'):
        election_info = election.find_all('a')
        if len(election_info) > 0:
            if 'президент' in election_info[0].text.lower():
                elections_links.append(election_info[0].get('href'))

    election_years = ['2004', '2008', '2012', '2018']
    region_links_all_years = []

    for i, elections_link in enumerate(elections_links):
        # Открываем ссылку с выборами
        br = wb.Chrome(service=s)

        br.get(elections_link)
        sleep(10)
        page = br.page_source
        soup = BeautifulSoup(page)
        dom = etree.HTML(str(soup))

        # Собираем ссылки на регионы в рамках этих выборов
        regions = soup.find_all('ul', attrs={'style': 'opacity: 1; transition-duration: 0.5s;'})[0]

        region_links = set()

        for region in regions.find_all('li'):
            if 'цик' in region.find_all('a')[1].text.lower():
                # уровень всей России не нужен
                continue
            rel_link = region.find_all('a')[1].get('href')  # link
            full_link = 'http://www.vybory.izbirkom.ru/' + rel_link
            region_links.add(full_link)

        print(f'[INFO] за {election_years[i]} год найдено {len(region_links)} ссылок')
        region_links_all_years.append(region_links)
        br.close()

    # Теперь проходим по каждым выборам и каждому региону, парсим данные
    for i, link in enumerate(region_links_all_years):

        if i == 0:  # 2004
            df_2004 = parse_2004_presidential_elections(region_links_all_years[i])
        elif i == 1:  # 2008
            df_2008 = parse_2008_presidential_elections(region_links_all_years[i])
        elif i == 2:  # 2012
            df_2012 = parse_2012_presidential_elections(region_links_all_years[i])
        elif i == 3:  # 2018
            df_2018 = parse_2018_presidential_elections(region_links_all_years[i])

    return df_2004, df_2008, df_2012, df_2018
