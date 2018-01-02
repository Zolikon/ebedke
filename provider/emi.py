from datetime import datetime as dt
from datetime import timedelta
from provider.utils import get_dom

URL = "http://www.emikifozte.hu/menuk.php"

def getMenu(today):
    menu = ''
    try:
        if today.weekday() < 5:
            dom = get_dom(URL)
            menu = dom.xpath('/html/body//tr[@class="menutablasor"]/td[3]')
            menu = '<br>'.join(e.text_content().strip('(, )') for e in menu)
    except:
        pass

    return menu

menu =  {
    'name': 'Emi kifőzte',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=20),
    'cards': {
        'bank': True,
        'szep': True,
        'bozsi': True
    }
}

if __name__ == "__main__":
    print(getMenu(dt.today()))