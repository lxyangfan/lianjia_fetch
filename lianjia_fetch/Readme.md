### 链家上海数据抓取

#### 要求
下载的数据按照如下格式整理：
- 城市|区域|城镇|名称|小区|街道|总价|单价|年限|简介|面积|房间数|大厅数|楼层|总楼层|朝向

#### URL 分析

URL: `http://sh.lianjia.com/ershoufang/pudongxinqu/`

- URL 表示上海、浦东的二手房数据
- `{URL}/d2` 表示分页第二页的数据

每一页房源列表`<ul class="js_fang_list" />`

