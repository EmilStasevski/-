from parsing_tools.parse import parse
from parsing_tools.parse_constitution import parse_constitution
from parsing_tools.parse_presidential import parse_presidential


def main(path_to_chromedriver=None, result_name='result.csv'):
    if path_to_chromedriver is None:
        path_to_chromedriver = input('Введите путь к вашему файлу chromedriver')

    question = input('Вы хотите выбрать название выгрузки? [Y/n]')
    if question.strip() == 'Y':
        result_name = input('Введите свое название выгрузки в формате: "my_name.csv"')

    data_type = input('Какие данные вы хотите выгрузить? ["выборы президента"/"поправки в конституцию"]')
    if data_type == "поправки в конституцию":
        print('[INFO] Начало процесса парсинга')
        df = parse_constitution(path_to_chromedriver=path_to_chromedriver)
        df.to_csv(result_name, encoding='utf-8', index=False)
        print(f'[INFO] Выгрузка сохранена под именем {result_name}')
    elif data_type == "выборы президента":
        df_2004, df_2008, df_2012, df_2018 = parse_presidential(path_to_chromedriver=path_to_chromedriver)
        df_2004.to_csv(f'{result_name}_2004', encoding='utf-8', index=False)
        df_2008.to_csv(f'{result_name}_2008', encoding='utf-8', index=False)
        df_2012.to_csv(f'{result_name}_2012', encoding='utf-8', index=False)
        df_2018.to_csv(f'{result_name}_2018', encoding='utf-8', index=False)
        print(f'[INFO] Выгрузки сохранены под именем {result_name} + год выборов')
    else:
        assert False, f'К сожалению, выбранный тип выборов ({data_type}) не поддерживается.'


if __name__ == "__main__":
    main()
    print('[INFO] Парсинг завершен')
