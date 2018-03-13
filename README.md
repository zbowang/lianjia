# 当前版本说明

## spider说明
目前可以通过解析获得所有二手房详细信息，通过在cmd中运行下面这条命令
```
scrapy crawl secondhand -a city=上海
```

当前`start_requests`只是拿一个数量较少的页面来抓取，要将其换成注释中的`start_requests`才是从首页开始抓取

## items

对应spider配置好了item

## 下一步要做

配置代理（当前还无法大规模抓取），将数据存储如mongodb



