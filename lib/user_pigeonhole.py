import requests
import re
import logging
import time
import os
import sys
import random
from urllib.parse import quote
from html import unescape
logger = logging.getLogger(__name__)

def _get_blog_id(username):
    try:
        html = requests.get('https://{}.lofter.com/'.format(username))
        id_reg = r'src="//www.lofter.com/control\?blogId=(.*)"'
        blogid = re.search(id_reg, html.text).group(1)
        logger.info('=> The blog id of {} is: {}'.format(username, blogid))
        return blogid
    except Exception as e:
        logger.info('=> get blog id from http://{}.lofter.com failed'.format(username))
        logger.info('please check your username')
        exit(1)


# time_pattern: re.compile('s%d\.time=(.*);s.*type' % (query_number-1))
def _get_timestamp(type, html, time_pattern):
    if not html:
        if type=='tag':
            timestamp = 0
        elif type=='USER':
            timestamp = round(time.time() * 1000)
    else:
        if type=='tag':
            timestamp=time_pattern.findall(html)[-1]
        elif type=='USER':
            timestamp = time_pattern.search(html).group(1)
    return str(timestamp)


def _create_query_data(type, id, timestamp, query_number, start_tag=0):
    '''
    :param blogid: blogid由_get_blog_id方法获得
    :param timestamp: 每篇blog都对应一个timestamp，POST请求得到某个blog的timestamp之后，会以该blog作为时间起点检索更早的blog
    :param query_number: 请求blog篇数
    :return: POST请求参数
    '''
    if type=='USER':
        data = {'callCount': '1',
                'scriptSessionId': '${scriptSessionId}187',
                'httpSessionId': '',
                'c0-scriptName': 'ArchiveBean',
                'c0-methodName': 'getArchivePostByTime',
                'c0-id': '0',
                'c0-param0': 'boolean:false',
                'c0-param1': 'number:' + id,
                'c0-param2': 'number:' + timestamp,
                'c0-param3': 'number:' + query_number,
                'c0-param4': 'boolean:false',
                'batchId': '123456'}
    elif type =='tag':
        data = {
            'callCount': '1',
            'scriptSessionId': '${scriptSessionId}187',
            'httpSessionId': '',
            'c0-scriptName': 'TagBean',
            'c0-methodName': 'search',
            'c0-id': '0',
            'c0-param0': 'string:' + id,
            'c0-param1': 'number:0',
            'c0-param2': 'string:',
            'c0-param3': 'string:new',
            'c0-param4': 'boolean:false',
            'c0-param5': 'number:0',
            'c0-param6': 'number:' + str(query_number),
            'c0-param7': 'number:' + str(start_tag),
            'c0-param8': 'number:' + timestamp,
            'batchId': '123456'
        }
    return data

def _create_headers(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Host': username + '.lofter.com',
        'Referer': 'http://%s.lofter.com/view' % username,
        'Accept-Encoding': 'gzip, deflate'
    }
    return headers

def _get_html(url, data, headers):
    i = 0
    start = time.time()
    while i<10:
        try:
            html = requests.post(url, data = data, headers = headers)
            return html
        except Exception as e:
            i += 1
            time.sleep(random.randint(0, 2))
    end = time.time()
    logger.error('=> network error, reconnection tried 10 times for {}s.'.format(end-start))
    exit(0)

def _get_html_blog(url, headers):
    i=0
    start = time.time()
    while i<5:
        try:
            html = requests.get(url, headers, timeout=5).text
            return html
        except Exception as e:
            i+=1
    end = time.time()
    logger.error('=> network error for get blog, reconnection tried 5 times for {}s.'.format(end-start))
    return 0

def _capture_blog(headers, url, hot_number, cfg):
    print(url)
    html=_get_html_blog(url, headers)
    if html==0:
        return 0

    title_pattern = re.compile('<title>((?:\n|.)*?)</title>')
    title = unescape(title_pattern.findall(html)[0].replace('\n', ''))
    user_pattern = re.compile('https://(.*?).lofter')
    if sys.platform == 'darwin' or 'linux' in sys.platform:
        title = title.replace('/', '\\')
    elif 'win' in sys.platform:
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", '_', title)
    else:
        logger.error('=> fail in determine your platform')
    blog_author = user_pattern.findall(url)[0]

    tag_pattern = re.compile('<meta name="Keywords" content="(.*?)"')
    tag_list = tag_pattern.findall(html)[0].split(',')
    if not hot_number or int(hot_number) < cfg.TARGET.HOT_THRE:
        return 0
    for want_title in cfg.TARGET.TITLE:
        if not want_title in title:
            return 0
    for tag_plus in cfg.TARGET.TAG_PLUS:
        if not tag_plus.lower() in [x.lower() for x in tag_list]:
            return 0
    for tag_minus in cfg.TARGET.TAG_MINUS:
        if tag_minus in tag_list:
            return 0
    blog_id = url.split('/')[-1]
    output_file_name = os.path.join(cfg.OUTPUT_DIR, '['+blog_author+']'+title+'_'+blog_id+'.html')
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(html)
        logger.info('=> success write {}'.format(output_file_name))

def person_blog(cfg, user):
    blogid = _get_blog_id(user)
    query_number = 40
    time_pattern = re.compile('s%d\.time=(.*);s.*type' % (query_number-1))
    blog_url_pattern = re.compile(r's[\d]*\.permalink="([\w_]*)"')
    hot_pattern = re.compile('s[\d]*.noteCount=(\d*)')

    POST_url = 'https://%s.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr' % user
    # 这是个人归档在下滑的时候的POST请求包

    POST_payload = _create_query_data(cfg.TYPE, blogid, _get_timestamp(cfg.TYPE, None, time_pattern), str(query_number))

    headers = _create_headers(user)

    num_blogs = 0
    logger.info('=> start !')
    while(True):
        html = _get_html(POST_url, POST_payload, headers).text
        new_blogs = blog_url_pattern.findall(html)
        blogs_hot = hot_pattern.findall(html)
        num_new_blogs = len(new_blogs)
        num_blogs += num_new_blogs

        if num_new_blogs:
            logger.info("=> NewBlog:{}\tTotalBlogs:{}".format(num_new_blogs, num_blogs))
            for blog, hot in zip(new_blogs, blogs_hot):
                url = 'https://%s.lofter.com/post/%s' % (user, blog)
                _capture_blog(headers, url, hot, cfg)
        if num_new_blogs != query_number:
            logger.info('================')
            logger.info('=> capture complete')
            logger.info('=> totle blogs: {}'.format(num_blogs))
            logger.info('________________')
            break
        POST_payload['c0-param2'] = 'number:' + _get_timestamp(cfg.TYPE, html, time_pattern)
        logger.info('=> The next Time stamp is: {}'.format(POST_payload['c0-param2'].split(':')[1]))

        time.sleep(random.randint(0,2))


def save_tag(cfg, tag):
    query_number = 20
    time_pattern = re.compile('publishTime=(.*?);s[\d]*.publisher')
    blog_url_pattern = re.compile('blogPageUrl="(.*?)"')
    hot_pattern = re.compile('postHot=(.*?);')
    user_pattern = re.compile('https://(.*?).lofter')
    tag_url = 'http://www.lofter.com/tag/{}'.format(tag)

    POST_url = 'http://www.lofter.com/dwr/call/plaincall/TagBean.search.dwr'
    tag_count = 0
    tag = quote(tag)
    POST_payload = _create_query_data(cfg.TYPE,
                                      tag,
                                      _get_timestamp(cfg.TYPE, None, time_pattern),
                                      query_number,
                                      tag_count)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Referer': 'http://www.lofter.com/tag/{}?from=tagsearch'.format(tag.upper()),
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.lofter.com'
    }
    num_blogs = 0
    while(True):
        html = _get_html(POST_url, POST_payload, headers).text
        new_blogs = blog_url_pattern.findall(html)
        blogs_hot = hot_pattern.findall(html)
        num_new_blogs = len(new_blogs)
        num_blogs += num_new_blogs

        if num_new_blogs:
            logger.info("=> NewBlog:{}\tTotalBlogs:{}".format(num_new_blogs, num_blogs))
            for url, hot in zip(new_blogs,blogs_hot):
                single_header = _create_headers(user_pattern.findall(url)[0])
                _capture_blog(single_header, url, hot, cfg)
        if num_new_blogs ==0 :
            logger.info('================')
            logger.info('=> capture complete')
            logger.info('=> totle blogs: {}'.format(num_blogs))
            logger.info('________________')
            break
        POST_payload['c0-param8']='number:'+_get_timestamp(cfg.TYPE, html, time_pattern)
        POST_payload['c0-param7']='number:'+str(num_blogs)
        logger.info('=> The next Time stamp is: {}'.format(POST_payload['c0-param8'].split(':')[1]))

        time.sleep(random.randint(0,2))

