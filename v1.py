import requests, re, time
from PIL import Image
from io import BytesIO

class douban:
    def __init__(self):
        self.s = requests.Session()
        self.id = input('please input your Douban login id:')
        self.pw = input('please input your passward:')
        captcha_address = re.findall(r'https://www\.douban\.com/misc/captcha\S*size=s', 
                                        self.s.get('https://accounts.douban.com/login').text)
        if captcha_address:
            captcha_id = re.findall(r'id=(\S*en)', captcha_address[0])[0]
            Image.open(BytesIO(requests.get(captcha_address).content))
            captcha_solution = input('please input the captcha:')
            self.s.post('https://accounts.douban.com/login', 
                        data={'form_email': self.id, 'form_password': self.pw, 
                              'captcha-id':captcha_id, 'captcha-solution':captcha_solution,
                              'login': '%E7%99%BB%E5%BD%95', 'redir': 'https%3A%2F%2Fwww.douban.com%2F', 'source': 'None'})
        else:
            self.s.post('https://accounts.douban.com/login', data={'form_email': self.id, 'form_password': self.pw})


    def download_stat(self):
        print('Starting to download Douban statuses')
        with open('douban_stat.txt', 'w') as f:
            p = 1
            stat = re.compile(r'quote-clamp>\n  \n\n  <p>(.+)</p>\n</blockquote>\n\n\n\n</div>\n\n\n\n\n\n  \n<div class="actions">\n  \n  <span class="created_at" title="(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
            text = stat.findall(self.s.get('https://www.douban.com/people/unith/statuses').text)
            while text:
                for i in text:
                    f.write(i[1]+'\n')
                    f.write(i[0]+'\n')
                print('page %d succeeded!'%p)
                p = p + 1
                time.sleep(1)
                text = stat.findall(self.s.get('https://www.douban.com/people/unith/statuses', params={'p':'%d'%p}).text)


if __name__ == '__main__':
    db = douban()
    db.download_stat()