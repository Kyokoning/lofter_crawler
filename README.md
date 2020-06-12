## Abstract

这是一个基于python的爬虫项目，它的目的在于抢救性保护同人tag和同人作者作品的项目。

目前实现的功能：

- 根据提供的lofter id保存所有blog
- 根据提供的lofter tag保存所有tag条目下可见的blog（会比tag显示参与数小）

联系我：<a href="weibo.com/2124977484" target="_blank">微博</a>

不要用本项目代码做不好的事情！

## Quick Start

1. 安装依赖：

`pip install -r requirements.txt`

2. 根据需要修改`config/test.yaml`配置文件

配置选项|默认值|描述
:-------:|:----:|-------
OUTPUT_DIR|output/|保存存档的地址
TYPE|tag|脚本运行模式，可选项有tag和USER，可以保存tag和保存user的blog
TAG|    |如果选择了tag运行模式，那么目标tag
USER|   |如果选择了USER运行模式，那么目标user
------|target细节部分|------ 
PICTURE|true|blog是图片的话是否保存
ARTICAL|true|blog是文章的话是否保存
HOT_THRE|0|高于多少热度的文章被保存
TITLE| [] |标题中有什么内容的会被保存，这是list格式的配置，意味着可以有很多个与的目标
TAG_PLUS| [] |文章的tag中要有什么才会被保存。同样是list格式配置
TAG_MINUS| [] |如果文章的tag有什么，就不会被保存。同样是list格式配置

3. 运行脚本

`python tool/crawler.py --cfg config/test.yaml`

结果会产生很多html文件和一个log文件（名字是`TYPE`-`name/id`-时间.log）

## 运行示例

①User模式（<a href="coldiron.lofter.com/" target="_blank">白的毛熊</a>）

![image.png](https://i.loli.net/2020/06/13/cJVedgBUXx6rFQ3.png)

![image.png](https://i.loli.net/2020/06/13/fXuybjWVKoerRSH.png)

②tag模式（爬了一下几百年前的冷圈墙头然后发现已经没有我cp的东西了

tag的问题是lofter tag学里面的一个小问题，参与tag数是不算后面加入的tag，所以爬虫爬下来会少（测试了一432参与的tag，实际爬完是338）

![image.png](https://i.loli.net/2020/06/13/n3vO7tfBC8cFGSm.png)