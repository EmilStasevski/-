from parsing_tools.parse import parse


def main(path_to_chromedriver=None, result_name='result.csv'):
    if path_to_chromedriver is None:
        path_to_chromedriver = input('Введите путь к вашему файлу chromedriver')

    question = input('Вы хотите выбрать название выгрузки? [Y/n]')
    if question.strip() == 'Y':
        result_name = input('Введите свое название выгрузки в формате: "my_name.csv"')

    print('[INFO] Начало процесса парсинга')
    df = parse(path_to_chromedriver=path_to_chromedriver)
    df.to_csv(result_name, encoding='utf-8', index=False)
    print(f'[INFO] Выгрузка сохранена под именем {result_name}')


if __name__ == "__main__":
    main()
    print('[INFO] Парсинг завершен')
