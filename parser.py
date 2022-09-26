import requests
import time


API_URL = "https://192.168.1.209:4021"
MAIN_URL = API_URL + "/admin/api/jsonrpc/"
LOGIN = "Ilya"
PASSWORD = "bkmz1337"

call_reg = []
def parse():
    login_session = requests.Session()

    login_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Safari/537.36",
    }

    login_params = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Session.login",
        "params": {
            "userName": LOGIN,
            "password": PASSWORD,
            "application": {
                "name": "Test",
                "vendor": "Keiro",
                "version": "1.0",
                "remember": True
            }
        }
    }

    login_response = login_session.post(headers=login_headers,
                                        url=MAIN_URL, json=login_params, verify=False)

    token = login_response.json()["result"]["token"]
    keiro_cookies = login_session.cookies.get_dict()

    fetch_phones_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Safari/537.36",
        "X-Token": token
    }

    fetch_phones_params = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Status.getCalls",
        "params": {
            "query": {
                "limit": -1,
                "start": 0,
                "orderBy": [
                    {
                        "columnName": "ANSWERED_DURATION",
                        "direction": "Asc"
                    }
                ]
            }
        }
    }

    fetch_phones_session = requests.Session()

    while True:
        fetch_phones_request = fetch_phones_session.post(
            headers=fetch_phones_headers, json=fetch_phones_params, url=MAIN_URL, verify=False, cookies=keiro_cookies)
        # print(fetch_phones_request.json())

        data = fetch_phones_request.json()
        # print(data)
        print(data)
        if data['result']['calls'] == []:
            print('No call for record')
        else:
            for item in data['result']["calls"]:
                id_call = item["id"].split(".")[0]  # add id only number and check record
                # call_reg.append(id_call)
                if not id_call in call_reg:
                    number = item["FROM"]["NUMBER"]
                    print('добавил звонок')
                    call_reg.append(id_call)
                    if not(number == '14') and not(number == '15'):
                        response = requests.post(f'https://okna360-crm.ru/ERPOKNA360/AddNewCalls.php?key=d41d8cd98f00b204e9800998ecf8427e&PhoneClient={number}')

        time.sleep(2)


if __name__ == "__main__":
    parse()
