from urllib.request import Request, urlopen

from urllib.parse import urlencode, quote_plus

import xmltodict, json, csv, time

jsonObj = {}

url = 'http://apis.data.go.kr/B553077/api/open/sdsc/storeListInDong'

page = 1

key = 44

f = open("상가업소정보_202012_4.csv", 'a', newline='')
wr = csv.writer(f)

while True:
    now = time.localtime()
    queryParams = '?' + urlencode({
        quote_plus('ServiceKey'): 'L2P+0T9DkJwA6Ac+lUjSZ+JSBYFegWxLknhXJgJbn+N7vmjEzsPANAZnBpXIeYSfoow0XQxTr0yIEo72ZczzLw==',

        quote_plus('divId'): 'ctprvnCd',

        quote_plus('key'): key,

        quote_plus('numOfRows'): '1000',

        quote_plus('pageNo'): page,

        quote_plus('type'): 'xml',
    })

    request = Request(url + queryParams)

    time.sleep(0.5)

    request.get_method = lambda: 'GET'

    response_body = urlopen(request).read()

    dict = xmltodict.parse(response_body)

    jsonString = json.dumps(dict['response']['body'], ensure_ascii=False)

    jsonObj = json.loads(jsonString)

    print(jsonObj)

    print("%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec))


    if jsonObj == {'items':None}:
        if key == 50:
            print("프로그램을 종료합니다.")
            break

        if key == 44 or key == 45 or key == 46 or key == 47:
            page = 1
            key += 1
        elif key == 48:
            page = 1
            key = 50
    else:
        for item in jsonObj['items']['item']:
            wr.writerow([item['bizesId'], item['bizesNm'], item['brchNm'], item['indsLclsCd'], item['indsLclsNm'],
                         item['indsMclsCd'], item['indsMclsNm'], item['indsSclsCd'],
                         item['indsSclsNm'], item['ksicCd'], item['ksicNm'], item['ctprvnCd'], item['ctprvnNm'],
                         item['signguCd'], item['signguNm'], item['adongCd'],
                         item['adongNm'], item['ldongCd'], item['ldongNm'], item['lnoCd'], item['plotSctCd'],
                         item['plotSctNm'], item['lnoMnno'], item['lnoSlno'], item['lnoAdr'],
                         item['rdnmCd'], item['rdnm'], item['bldMnno'], item['bldSlno'], item['bldMngNo'],
                         item['bldNm'], item['rdnmAdr'], item['oldZipcd'], item['newZipcd'],
                         item['dongNo'], item['flrNo'], item['hoNo'], item['lon'], item['lat']])
        page += 1

f.close()