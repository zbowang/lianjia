# 当前版本说明

## spider说明
目前可以到达链家网所有城市二手房一级页面，通过在cmd中运行下面这条命令
```
scrapy crawl secondhand -a city=厦门
```

一级页面指类似这样的页面 
https://bj.lianjia.com/ershoufang/dongcheng/pg2/

现在是打印出了所有页的url（第一二页和最后一页）

## 其他

实现了user-agent的随机使用

## 下一步要做

1.写好`parse_simple`和`prase_detail`两个方法

- `parse_simple`需要从一级页面提取每一个房子的url
- `parse_detail`需要从每一个房子的页面提取详细信息

2.代码冗余改进

`parse_district` `parse_price`等方法的重复部分太多，需要简化代码

3.大规模抓取


