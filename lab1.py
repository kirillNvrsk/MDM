import csv

# значения в соотвествии с вариантом
CLIENT = '915642913'
FREE_MSG_COUNT = 5
FREE_IN_CALL_DUR = 0
FREE_OUT_CALL_DUR = 0
K_MSG = 1
K_IN_CALL = 1
K_OUT_CALL = 1
PATH = 'data.csv'


def read_csv_to_list_of_dict(filename):
    '''
    функция-парсер csv файла.
    :param filename: string
    :return: { column_name: [value1, value2, ...], key2: [...], ...}
    '''
    with open(filename) as file:
        reader = list(csv.reader(file))
        dict_keys = [key for key in reader[0]]
        count = len(reader[0])
        list_ = [[] for i in range(count)]
        print()
        for i in range(1, len(reader)):
            for j in range(0, count):
                list_[j].append(reader[i][j])
        dict_ = {}
        for i in range(0, count):
            dict_[dict_keys[i]] = list_[i]
    return dict_


def calculate(
        dict_from_CDR,
        client,
        k_in_call,
        k_out_call,
        k_msg,
        free_in_call_dur,
        free_out_call_dur,
        free_msg_count
):
    '''
    функция расчитывающая цену по тарифу
    :param dict_from_CDR: dict - словарь полученный вызовом метода read_csv_to_list_of_dict
    :param client: string - номер клиента
    :param k_in_call: int - коэффициент для входящих звонков
    :param k_out_call: int - коэффициент для исходящих звонков
    :param k_msg: int - коэффициент для сообщений
    :param free_in_call_dur: int - количество бесплатных входящих минут
    :param free_out_call_dur: int - количество бесплатных исходящих минут
    :param free_msg_count: int - количество бесплатных СМС
    :return: float - расчитанная цена
    '''
    out_call_dur = float(dict_from_CDR['call_duration'][dict_from_CDR['msisdn_origin'].index(client)])
    if out_call_dur <= free_out_call_dur:
        out_call_price = 0
    else:
        out_call_price = k_out_call * (out_call_dur - free_out_call_dur)


    in_call_dur = float(dict_from_CDR['call_duration'][dict_from_CDR['msisdn_dest'].index(client)])
    if in_call_dur <= free_in_call_dur:
        in_call_price = 0
    else:
        in_call_price = k_in_call * (in_call_dur - free_in_call_dur)

    msg_count = int(dict_from_CDR['sms_number'][dict_from_CDR['msisdn_origin'].index(client)])
    if msg_count <= free_msg_count:
        msg_price = 0
    else:
        msg_price = k_msg * (msg_count - free_msg_count)

    return msg_price + out_call_price + in_call_price


price = calculate(
    dict_from_CDR=read_csv_to_list_of_dict(PATH),
    client=CLIENT,
    k_in_call=K_IN_CALL,
    k_out_call=K_OUT_CALL,
    k_msg=K_MSG,
    free_in_call_dur=FREE_IN_CALL_DUR,
    free_out_call_dur=FREE_OUT_CALL_DUR,
    free_msg_count=FREE_MSG_COUNT)
print('Цена для абонента:',  price, 'рублей')