import logging
import os

import scapy.all as sc
from openpyxl import load_workbook

import DB
from DB import create_tables
from dotenv import load_dotenv
import json

load_dotenv()
SUBNET_1 = os.getenv("SUBNET_1")
SUBNET_2 = os.getenv("SUBNET_2")


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def clear_mac_ip_pairs_table():
    try:
        if DB.conn is None or DB.cursor is None:
            logging.error('Отсутствует соединение с базой данных или указатель.')
            return

        DB.cursor.execute("DELETE FROM mac_ip_pairs;")
        DB.conn.commit()

        logging.info("Таблица mac_ip_pairs успешно очищена.")
    except Exception as e:
        logging.error(f'Ошибка при очистке таблицы mac_ip_pairs: {str(e)}')


def get_ip_mac_network(subnet):
    try:
        logging.info(f'Начинаем сканирование сети {subnet}')
        answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=subnet), timeout=1, verbose=False)[0]
        clients_list = [{'ip': element[1].psrc, 'mac': element[1].hwsrc} for element in answered_list]
        logging.info(f'Получены данные по MAC-адресам и IP-адресам: {clients_list}')
        return clients_list
    except Exception as e:
        logging.error(f'Ошибка в get_ip_mac_network: {str(e)}')
        return []


def ip_mac_to_database(mac_ip_list):
    try:
        if DB.conn is None or DB.cursor is None:
            logging.error('Отсутствует соединение с базой данных или указатель.')
            return

        for client in mac_ip_list:
            mac_address_upper = client['mac'].upper()

            DB.cursor.execute('''
                INSERT INTO mac_ip_pairs (mac_address, ip_address)
                VALUES (%s, %s)
            ''', (mac_address_upper, client['ip']))

        DB.conn.commit()
        logging.info('Данные добавлены в базу данных.')
    except Exception as e:
        logging.error(f'Ошибка при добавлении данных в базу данных: {str(e)}')


def scan_and_to_database(subnet):
    ip_mac_network = get_ip_mac_network(subnet)
    ip_mac_network.sort(key=lambda x: int(x['ip'].split('.')[3]))
    ip_mac_to_database(ip_mac_network)


def convert_excel_to_json(excel_file_path):

def update_html_with_json(json_file_path, html_file_path):

def get_column_names():



if __name__ == "__main__":
    create_tables()
    clear_mac_ip_pairs_table()

    scan_and_to_database(SUBNET_1)
    scan_and_to_database(SUBNET_2)


    logging.info('Программа успешно выполнена.')
