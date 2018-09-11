from bs4 import BeautifulSoup




def electric_meter_data(s):
    url = 'http://xh.shhanqian.com:10002/bid/monitor/measure/showElectricMeterList.htm?equipTypeId=8001'
    r = s.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'class': 'table-one-two-one sortable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])

    for d in data:
        for x in d:
            print x

if __name__ == '__main__':
    pass