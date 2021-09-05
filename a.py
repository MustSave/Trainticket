#!/usr/bin/python 
# #-*- encoding: utf-8 -*-# 
import requests 
from bs4 import BeautifulSoup
from urllib import parse
import alarm
import time as t
import re

# 코레일 데이터 크롤링 
def get_info(Year, Month, Day, Hour):
    diff = 6 - len(Hour)
    if diff > 0:
        for i in range(0, diff):
            Hour = Hour+"0"

    url = 'https://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do'

    
    postData = {'txtGoAbrdDt' : Year+Month+Day
    , 'txtGoHour' : Hour
    , 'selGoYear' : Year
    , 'selGoMonth' : Month
    , 'selGoDay' : Day
    , 'selGoHour' : '09'
    , 'txtGoPage' : '2'
    , 'txtGoStartCode' : '0001'
    , 'txtGoStart' : '%EC%84%9C%EC%9A%B8'
    , 'txtGoEndCode' : '0015'
    , 'txtGoEnd' : '%EB%8F%99%EB%8C%80%EA%B5%AC'
    , 'selGoTrain' : '05'
    , 'selGoRoom' : ''
    , 'selGoRoom1' : ''
    , 'txtGoTrnNo' : ''
    , 'useSeatFlg' : ''
    , 'useServiceFlg' : ''
    , 'selGoSeat' : ''
    , 'selGoService' : ''
    , 'txtPnrNo' : ''
    , 'hidRsvChgNo' : ''
    , 'hidStlFlg' : ''
    , 'radJobId' : '1'
    , 'SeandYo' : ''
    , 'hidRsvTpCd' : '03'
    , 'selGoSeat1' : '015'
    , 'selGoSeat2' : ''
    , 'txtPsgCnt1' : '1'
    , 'txtPsgCnt2' : '0'
    , 'txtMenuId' : '11'
    , 'txtPsgFlg_1' : '1'
    , 'txtPsgFlg_2' : '0'
    , 'txtPsgFlg_3' : '0'
    , 'txtPsgFlg_4' : '0'
    , 'txtPsgFlg_5' : '0'
    , 'txtPsgFlg_8' : '0'
    , 'chkCpn' : 'N'
    , 'txtSeatAttCd_4' : '015'
    , 'txtSeatAttCd_3' : '000'
    , 'txtSeatAttCd_2' : '000'
    , 'txtGoStartCode2' : ''
    , 'txtGoEndCode2' : ''
    , 'hidDiscount' : ''
    , 'hidEasyTalk' : ''
    , 'adjcCheckYn' : 'N'}

    data = requests.post(url, postData) 
    plain_text = data.text 
    soup = BeautifulSoup(plain_text, 'html.parser') 
    result = soup.find('table', id="tableResult")
    # f = open('a.html', 'w', -1, 'utf-8')
    # f.write(str(result))
    # f.close()
    return result


if __name__=='__main__':
    time = '13:00'

    while True:
        time = time[:2]+time[-2:]
        res = get_info('2021', '09', '18', time)

        trs = res.find_all('tr')
        del trs[0]

        for tr in trs:
            tds = tr.find_all('td')
            dep = tds[2].text.strip()
            dep = [dep[:-5], dep[-5:]]
            #다음날 출발, 출발시간 거르기
            if int(dep[1][:2]) >= 19:
                break

            arr = tds[3].text.strip()
            arr = [arr[:-5], arr[-5:]]
            # 도착시간 거르기
            if int(arr[1][:2]) >= 21:
                continue
            ilbansil = tds[5].find('img').attrs['alt'].strip()
            try:
                reserve = tds[9].find('img').attrs['alt'].strip()
            except:
                reserve = "매진"

            if ilbansil != "좌석매진":
                alarm.telegram(dep[0] + " " + dep[1] + " → " + arr[0]+ " " + arr[1] + " " + "좌석 예약하기")
            elif reserve != "매진":
                alarm.telegram(dep[0] + " " + dep[1] + " → " + arr[0]+ " " + arr[1] + " " + "예약 대기 신청하기")
        
        #다시 처음부터
        if int(dep[1][:2]) >= 19:
             time = '13:00'
             print("시간 초기화")
             t.sleep(10)
        else :
            time = arr[1]
    
        
        