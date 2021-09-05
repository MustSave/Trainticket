#!/usr/bin/python
#-*- encoding: utf-8 -*-#

import requests
from bs4 import BeautifulSoup

url = 'http://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do'

postData = {
'selGoTrain': '05',
'txtPsgFlg_1': '1',
'txtPsgFlg_2': '0',
'txtPsgFlg_8': '0',
'txtPsgFlg_3': '0',
'txtPsgFlg_4': '0',
'txtPsgFlg_5': '0',
'txtSeatAttCd_3': '000',
'txtSeatAttCd_2': '000',
'txtSeatAttCd_4': '015',
'selGoTrainRa': '05',
'radJobId': '1',
'txtGoStart': '서울',
'txtGoEnd': '영천',
'selGoYear': '2021',
'selGoMonth': '09',
'selGoDay': '18',
'selGoHour': '09',
'txtGoHour': '090000',
'txtGoYoil': '토',
'selGoSeat1':'015',
'txtPsgCnt1': '1',
'txtPsgCnt2': '0',
'txtGoPage': '1',
'txtGoAbrdDt': '20210918',
'SeandYo': 'N',
'checkStnNm': 'Y',
'chkInitFlg': 'Y',
'txtMenuId': '11',
'ra': '1',
'strChkCpn': 'N',
'txtSrcarCnt': '0',
'txtSrcarCnt1': '0',
'hidRsvTpCd': '03',
'txtPsgTpCd1': '1',
'txtPsgTpCd2': '3',
'txtPsgTpCd3': '1',
'txtPsgTpCd5': '1',
'txtPsgTpCd7': '1',
'txtPsgTpCd8': '3',
'txtDiscKndCd1': '000',
'txtDiscKndCd2': '000',
'txtDiscKndCd3': '111',
'txtDiscKndCd5': '131',
'txtDiscKndCd7': '112',
'txtDiscKndCd8': '321',
'txtCompaCnt1': '0',
'txtCompaCnt2': '0',
'txtCompaCnt3': '0',
'txtCompaCnt4': '0',
'txtCompaCnt5': '0',
'txtCompaCnt6': '0',
'txtCompaCnt7': '0',
'txtCompaCnt8': '0'
}

data = requests.post(url, postData)
f = open('a.html', 'w', -1, 'utf-8')
f.write(data.text)
f.close()
soup = BeautifulSoup(data.text, 'html.parser')

result = soup.find('table', id='tableResult')
print(result)
result = result.find('td', title="KTX")

#좌석 매진 검사
count = 0

for i in range(0, 6):
    result = result.find_next('td')
    data = str(result)

    if data.find('btn_selloff.gif') > 0:
        count += 1

if count < 3:
    print("예매 ㅇㅇ")