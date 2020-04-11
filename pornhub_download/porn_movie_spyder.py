import requests
import parsel
import time
import execjs
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


def get_pages_urls(star_name, page):
    target_url = []
    for i in range(1, page):
        url = 'https://www.pornhub.com/model/' + star_name + '/videos?page=' + str(i)
        response = requests.get(url, headers=headers)
        sel =parsel.Selector(response.text)
        movie_urls = sel.xpath('//*[@id="mostRecentVideosSection"]/li/div/div/div/a/@href').extract()
        head = 'https://www.pornhub.com'
        for movie_url in movie_urls:
            target_url.append(head + movie_url)
    return target_url

def get_movieurls(target_urls):
    for url in target_urls:
        response = requests.get(url)
        sel = parsel.Selector(response.text)
        # 获取执行得所有js
        js_source = sel.xpath('//*[@id="player"]/script[1]/text()').extract_first()
        name = sel.xpath('//*[@id="hd-leftColVideoPage"]/div[1]/div[3]/h1/span/text()').extract_first()
        # print(js_source)
        # 截掉后面playerObjList部分
        source = js_source.split('playerObjList')[0]
        #获得flashvars 脚本函数名
        key = re.findall(r'flashvars_\d+', source)[0]
        # 编译js
        js = execjs.compile(source)
        # 获取 key函数执行后的返回值
        data = js.eval(key)
        for md in data['mediaDefinitions']:
            video_url = md['videoUrl']
            quality = md['quality']
            _format = md['format']
            if _format == "mp4":
                movie = requests.get(video_url)
                with open(r'D:\pornhub\porn_movie\sweet-bunny\\' + name + '.mp4', 'wb') as f:
                    print('电影' + name + "正在下载")
                    f.write(movie.content)
                break





if __name__ == '__main__':
    try:
        target_urls = get_pages_urls('sweet-bunny', 2)
        print(len(target_urls))
        get_movieurls(target_urls)

    except Exception as e:
        print(e)



# movie_dict = {}
# for name, url in zip(movie_name_list, all_list):
#     movie_dict[name] = url




