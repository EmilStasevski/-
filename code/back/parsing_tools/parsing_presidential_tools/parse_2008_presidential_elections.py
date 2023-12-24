def parse_2008_presidential_elections(region_links_2008):
    """
    Функция для парсинга результатов выборов президента РФ в 2008 г.
    :param region_links_2008: list[str], ссылки на регионы, в которых нужно спарсить результат
    :return: pandas.DataFrame, с результатами выборов по всем регионам РФ на момент выборов
    с разбивкой по ТИК-ам
    """
    for i, link in enumerate(region_links_2008):
        print(f'[INFO] Собираю данные про регион №{i} из {len(region_links_2008)} \nURL: {link}')
        br = wb.Chrome(service=s)

        br.get(link)
        sleep(10)
        br.implicitly_wait(10)
        # выбираем раздел с результатами
        results_button = br.find_element(By.CSS_SELECTOR, "#election-results-name")
        results_button.click()
        sleep(10)
        br.implicitly_wait(10)
        try:
            # выбираем нужное представление данных ("Сводная таблица итогов голосования")
            table_button = br.find_element(By.CSS_SELECTOR,
                                           r"#election-results > table > tbody > tr:nth-child(2) > td > a")
            table_button.click()
            sleep(10)
            br.implicitly_wait(10)
        except:
            print(f'ERROR {link}')
            continue
        # забираем код страницы
        page = br.page_source
        soup = BeautifulSoup(page)
        # собираем данные

        # собираем данные
        # название комиссии
        commission_name = soup.find_all('table', attrs={'class': 'table-borderless',
                                                        'width': "100%"})[0].find_all('td')[1].text.strip()
        # дата
        vote_date_raw = soup.find_all('div', attrs={'id': 'election-info'})[0]
        vote_date_full = vote_date_raw.find_all('div')[-1].text.strip()
        vote_date_short = vote_date_full[-4:]
        # таблица с результатами
        vote_data_raw = soup.find_all('div', attrs={'class': 'table-wrapper'})[0]
        # собираю название регионов
        sub_level_names = []
        # здесь можно в a href собрать ссылки на уровень ниже
        for sub_level_name in vote_data_raw.find_all('th', attrs={'class': 'text-center'}):
            sub_level_names.append(sub_level_name.text)

        # собираю результаты
        full_data = []

        rows = vote_data_raw.find_all('tr')
        for row in rows:
            cols = row.find_all('td', attrs={'class': 'text-right'})
            if len(cols) == 0:
                continue
            full_data.append([col.text.strip() for col in cols])

        participation = full_data[:-4]
        vote_results_raw = full_data[-4:]

        results_abs = []
        results_percent = []

        for vote_results_for_candidate in vote_results_raw:
            results_abs.append([res.split()[0] for res in vote_results_for_candidate])
            results_percent.append([res.split()[1].replace('%', '') for res in vote_results_for_candidate])

        # df по региону
        df = pd.DataFrame(
            {'elections_year': [vote_date_full] * len(sub_level_names[1:]),
             'region': [commission_name] * len(sub_level_names[1:]),
             'commission_name': sub_level_names[1:],
             'voters_number': participation[0],
             'ballots_number_received': participation[1],
             'issued_ballots_number_early': participation[2],
             'issued_ballots_number_voting_day_incide': participation[3],
             'issued_ballots_number_voting_day_outside': participation[4],
             'ballots_number_extinguished': participation[5],
             'ballots_number_portable_boxes': participation[6],
             'ballots_number_stationary_boxes': participation[7],
             'ballots_number_invalid': participation[8],
             'ballots_number_valid': participation[9],
             'ballots_number_absentee_received': participation[10],
             'ballots_number_absentee_issued': participation[11],
             'voters_number_voted_on_absentee_ballots': participation[12],
             'number_absentee_ballots_unused': participation[13],
             'ballots_number_absentee_issued_to_tik_voters': participation[14],
             'ballots_number_lost': participation[15],
             'ballots_number_not_counted': participation[16],
             'number_absentee_ballots_lost': participation[17],
             'number_absentee_ballots_not_taken': participation[18],
             # голоса
             'bogdanov_andrey_vladimirovich_number': results_abs[0],
             'bogdanov_andrey_vladimirovich_percent': results_percent[0],
             'zhirinovsky_vladimir_volfovich_number': results_abs[1],
             'zhirinovsky_vladimir_volfovich_percent': results_percent[1],
             'zyuganov_gennady_andreevich_number': results_abs[2],
             'zyuganov_gennady_andreevich_percent': results_percent[2],
             'dmitry_anatolyevich_medvedev_number': results_abs[3],
             'dmitry_anatolyevich_medvedev_percent': results_percent[3]
             }
        )

        if i == 0:
            stacked_df = df.copy()
        else:
            stacked_df = pd.concat([stacked_df, df])

        br.close()
        clear_output(wait=True)

    return stacked_df
