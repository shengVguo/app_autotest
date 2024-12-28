# app_autotest


# 测试策略
### 测试计划阶段
#### 测试目标
- 本次任务是新闻类app，可能着重于页面内容展示、响应性能、兼容性、算法推荐的结果等
#### 测试范围
- 测试范围：头条栏目主页、新闻内容页、更贴页
#### 测试资源
- 提前明确资源配置的方式，如运营后台配置，还是配置算法推荐，是否支持数据库插入
- app所需要的测试设备
#### 测试进度
- 依照排期、工作量、测试人力安排即可

### 测试设计阶段
#### 需求分析
- 首先最终要的是做需求分析，弄懂业务的需求是最重要，在需求评审阶段就应该尽量与各方达成理解一致，以减少提测后不必要的bug
- 有需求疑问及时对接产品经理沟通，有需求变更的地方一定要让其同步到各端侧
#### 测试方法
- 功能测试，接口功能测试
- 性能测试：客户端专项性能测试、接口性能测试
- 项目稳定后，可以维护到自动化测试
#### 用例设计
- 测试设计上主要从几个方面：功能测试（正常、异常），界面测试，兼容性测试，性能测试，安全测试，易用性测试
### 测试执行阶段
- 测试环境搭建和部署
- 执行测试用例：冒烟测试、测试执行、bug跟踪和管理、回归测试
### 测试评估阶段
### 分析测试结果
- 测试结果：统计用例执行情况、bug统计（等级、功能模块、bug类型等）、测试周期内bug数量分布情况，用于评估整体的质量
- 可以用缺陷率DI值来参考评估是否达标
### 编写测试报告
- 主要覆盖测试目标、测试结论、范围、缺陷统计、用例执行情况、结果分析、遗留问题等
### 项目复盘
- 可以开项目复盘会议，从需求质量、开发质量、测试质量等各个方面






# 自动化测试构思和步骤
#### 框架选型
- uiautomator2：主流`android`自动化测试框架，自带封装了很多移动端操作方法，相比与`Appium`，启动和定位元素速度快很多
- pytest: 主流测试框架，插件多

#### 设计模式
项目采用Page Object的模式,分层设计
- 基础层：`BasePage类`，定义与底层移动测试框架交互的方法，移动端通用操作方法
- 页面层：每个页面都是一个page对象，封装该页面常用的方法
- 用例层：专注编写测试用例，基于pytest
#### 环境准备
- python 3.8+
- 安装jdk、adb、sdk
- 手机开启开发者选项、打开USB调试，用数据线连接PC端后，执行adb命令，会生成adb key，若手机端无该公钥，则弹窗提示是否允许调试、允许即可，后续该手机再次连接该PC则不许再弹窗配对
#### 实现步骤
1、根据业务类型和需求，挑选适合自动化的用例

2、app模块中`App`类继承于`BasePage`类主要封装待测app的公共方法，如启动app、登录、注销、跳过开屏广告等，具体后的page类继承于`App`类；

3、对于这种信息卡片流应用，页面元素往往每次打开都不一样，滑动寻找元素方法比较实用

4、实际应用中，如果使用mock手段干预信息流接口的返回，可以塑造更稳定的场景数据
#### 运行方法
- 安装`requirements.txt`中的库后
- 准备上述环境
- 在项目根目录执行`pytest`即可，也可以根据需求写个运行脚本

#### To do
- 增加运行过程记录GIF，可定义一个装饰器函数，装饰`find_element`方法，每次操作元素都会截图，并在截图上标记元素边界方框（边界来自于元素本身的属性）用于示意被寻找的元素，每个用例的步骤截图可以用pillow工具拼接成Gif动图，并附在测试报告上，可直观查看运行情况和失败的具体步骤
- 部分不好定位的元素，可以补充图片对比辅助定位元素，如采用`airtest`库，可类似于`uiautomator2`中的元素对象，定义一个`ImageElement`，并继承图片元素的常用方法和属性，如点击、边界、坐标等，也方便扩展，具体Api可以参考`uiautomator2`的方法
- 环境部署：可以采用`Docker`部署的方式，若将来需要集成到其他机器运行，也可以快速部署测试环境，将python、adb、sdk、jdk都在Dockerfile中定义好构建就行

