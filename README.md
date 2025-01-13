# 12306 微信小程序信息类 API 收集

**此合集不包括** `leftTicketDTO` **等购票类接口，不能用来刷票抢票，资源仅供学习交流使用。**

**如有遗漏请提交 PR 补充 :)**

## 通用注意事项

- 所有接口默认为 `POST` 请求，返回 `JSON` 数据。如有特殊情况会在接口说明中标明。
- 请用 `Python requests` 等库调用接口，大部分接口不能直接通过浏览器访问。
- 请勿频繁请求接口，以免被封禁 IP。
- 返回的坐标均采用 `GCJ-02` 格式，如需转换请自行查找相关库。

### 辅助链接

- 车站站名、电报码等列表：[https://kyfw.12306.cn/otn/resources/js/framework/station_name.js](https://kyfw.12306.cn/otn/resources/js/framework/station_name.js)
- 车次码、车次编号列表：[https://kyfw.12306.cn/otn/resources/js/query/train_list.js](https://kyfw.12306.cn/otn/resources/js/query/train_list.js)

### 参数格式

- 所有参数用 `application/x-www-form-urlencoded` 格式传递，可直接写入 `URL` 中（例如 `apiLink?param1=value1&param2=value2`）。
- 参数默认均为必填项，该合集采用的参数格式如下：
  - 【日期】：格式为 `YYYYMMDD`。
  - 【车次码】：旅客常用的车次码，例如 `G1234`。
  - 【车次编号】：车次的唯一编号，例如 `24000000D121`。
  - 【列车号】：列车的唯一编号，例如 `CR400BF-5033`。
  - 【车站】：一座车站的电报码，例如 `SHH`。
  - 【车站列表】：一座或多座车站的电报码列表，用逗号分隔，例如 `BJP,SHH`。
  - 【铁路局】：铁路局的简称：例如沪局为 `H`，京局为 `P`，完整列表目前未知。

### 图片链接

如接口返回的图片链接非完整 URL，默认有以下前缀：

- `https://eximages.12306.cn/travel-info-bucket/travelsys/`：旅游、服务须知相关图片。
- `https://wifi.12306.cn/resourcecenter/cateringimages/`：列车信息、餐饮相关图片。

## 常用/重要接口

- [车次运行信息](#车次运行信息-httpsmobile12306cnwxxcxwechatmaintravelserviceqrcodetraininfo)
- [车次走向](#车次走向-httpsmobile12306cnwxxcxwechatmaingettrainmapline)
- [车次停站信息](#车次停站信息-httpsmobile12306cnwxxcxwechatticketinfogetstopstation)
- [车站车次大屏](#车站车次大屏-httpsmobile12306cnwxxcxwechatbigscreenquerytrainbystation)

## 全部接口列表

### 配置信息 (https://mobile.12306.cn/wxxcx/wechat/main/conf)

- 参数：无
- 返回：小程序主页配置信息，包括图标、广告信息等。

### 广告信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/qrCode/getAdvInfo)

- 参数：`?reqType=form`
- 返回：暂无

### 当日车次所属铁路局 (https://mobile.12306.cn/wxxcx/wechat/bigScreen/queryTrainBureau)

- 参数：`?queryDate=【日期】&trainCode=【车次码】`
- 返回：当日车次所属铁路局信息。
- 注： `travelServiceQrcodeTrainInfo` 接口中包括了该接口全部信息。

### 车次所属铁路局 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/qrCode/getDeptByTrainCode)

- 参数：`?trainCode=【车次码】&reqType=form`
- 返回：车次所属铁路局、担当车底等信息。
- 注： `travelServiceQrcodeTrainInfo` 接口中包括了该接口全部信息。

### 旅游热门产品信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/tourism/tourismBase/api/scenic/getThemeProduct)

- **该接口使用 `GET` 请求**
- 参数：`?cityCode=0&vectorId=MR_0002&salesChannel=Z&version=2`
- 返回：旅游热门产品信息，包括名称、价格、图片等。

### 旅行服务图标列表 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/tourism/tourismBase/api/scenic/getIcons)

- 参数：`?smoothType=1`
- 返回：旅行服务图标列表，包括图标名称、图片、链接等。
- **`&citys=【城市列表】`** 为可选参数，例如 `&citys=["VNP","TIP","NKH","SHH"]`。

### 旅客须知图片列表 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/carService/getCarServiceByCarCode)

- 参数：`?bureauCode=&carCode=&reqType=form`
- 返回：旅客须知、禁限物品、畅行会员等图片链接。

### 车次运行信息 (https://mobile.12306.cn/wxxcx/wechat/main/travelServiceQrcodeTrainInfo)

- 参数：`?trainCode=【车次码】&startDay=【日期】&startTime=&endDay=&endTime=`
- 返回：当日车次运行信息，包含车站（含坐标）、到发时间、担当车底等等，比12306官网车次查询更详细。

### 铁路局小程序 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/bureauApplet/getBureauApplet)

- **该接口使用 `GET` 请求**
- 参数：`?trainCode=&bureauCode=【铁路局】&carCode=&reqType=form&startDay=&startTime=&endDay=&endTime=`
- 返回：铁路局小程序 ID、公司名称、图标等信息。

### 车站地图信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/stationEquipment/getIndexMapInfo)

- 参数：`?stationTelecode=【车站列表】&reqType=json`
- 返回：车站地图信息，包括车站名称、坐标、设施、周边景点、图标等。

### 车站设施信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/stationEquipment/getStationEquipmentInfoList)

- 参数：`?stationTelecode=【车站列表】&reqType=json`
- 返回：车站设施/服务信息，包括商务服务，行李寄存/搬运，中转换乘，网络订餐等。

### 车站信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/stationEquipment/getStationMapInfo)

- 参数：`?stationTelecode=【车站列表】&queryType=【种类】&reqType=json`
- 种类/返回：`1` - 行李与公司信息，`2` - 餐食库存信息

### 车次走向 (https://mobile.12306.cn/wxxcx/wechat/main/getTrainMapLine)

- 参数：`?version=v2&trainNo=【车次编号】`
- 返回：车次走向信息，每两个车站之间为一个 object，包含坐标列表。

### 车站周边水果等商品 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/tourism/tourismBase/changxing/getIconsV2)

- 参数：`?stationCode=【车站列表】&reqType=form`
- **该接口使用不同的车站列表格式**，例如 `["VNP","TIP","NKH","SHH"]`。
- 返回：车站周边水果等商品介绍、图片、产地等信息。

### 车站天气 (https://mobile.12306.cn/wxxcx/wechat/weather/total)

- 参数种类：
  - **该接口使用不同的日期格式**，例如 `2021-09-30`。
  - `?stationCode=【车站列表】`：返回 30 天比较粗略的天气预报
  - `?stationCode=【车站列表】&date=【日期】&type=forcast&version=v2`：返回当天比较粗略的天气预报
  - `?stationCode=【车站列表】&type=forcast&version=v2`：返回 24 小时比较详细（每小时一行）的天气预报

### 车次停站信息 (https://mobile.12306.cn/wxxcx/wechat/ticketInfo/getStopStation)

- 参数：`?train_no=【车次编号】&train_date=【日期】&f_station_telcode=`
- 返回：车次停站信息，包括车站名称、到发时间、停留时间、电报码等。
- **`f_station_telcode=【车站】`** 为可选参数，可提供出发车站的电报码。该参数估计是为了分辨过夜车次日期从哪个站开始计算。

### 换乘时间 (https://mobile.12306.cn/wxxcx/wechat/main/getLCLimitWaitTime)

- 参数：`?station_telecode=【车站】&train_date=【日期】`
- 返回：与相邻车站换乘需预留的时间。

### 车站地址 (https://mobile.12306.cn/wxxcx/wechat/bigScreen/getStationAddress)

- 参数：`?stationCode=【车站】`
- 返回：车站地址、坐标等信息。

### 列车车厢信息 (https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/trainStyleBatch/getCarDetail)

- **该接口使用 `GET` 请求**
- 参数：`?carCode=【列车号】&trainCode=【车次码】&runningDay=【日期】&reqType=form`
- 该接口有两种索引方式：
  - 根据车次与日期（列车号为空）：例如 `?carCode=&trainCode=G1234&runningDay=20210930`
  - 根据列车号（车次码与日期为空）：例如 `?carCode=CR400BF-5033&trainCode=&runningDay=`
- 返回：列车车厢信息，包括种类、车厢号、定员、座位图链接等。

### 车站车次大屏 (https://mobile.12306.cn/wxxcx/wechat/bigScreen/queryTrainByStation)

- 参数：`?train_start_date=【日期】&train_station_code=【车站】`
- 返回：日期参数以后所有途径该车站的车次信息，包括到发站/时间、管理信息（路局、管内/外、临客等）、担当车底/车辆段（包括普速和高铁）等，比12306官网车次查询更详细。

### 车次开行日期 (https://mobile.12306.cn/wxxcx/wechat/bigScreen/queryTrainDiagram)

- 参数：`?queryDate=【日期】&trainCode=【车次码】`
- 返回：三个月内该车次那些日期开行。