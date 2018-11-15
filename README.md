## 项目介绍：
  基于Flask框架的租房小项目，已上传至腾讯云服务器，该项目有以下几个模块：
#### 1、主页
     
      1.1 根据上传房源的图片最多5个房屋图片展示，点击可跳转至房屋详情页面
      1.2 提供登陆/注册入口，登陆后显示用户名，点击可跳转至个人中心
      1.3 用户可以选择城区、入住时间、离开时间等条件进行搜索
      1.4 城区的区域信息需动态加载
      
#### 2、注册、登录

      2.1 用户账号默认为手机号
      2.2 图片验证码正确后才能发送短信验证码(云通讯)
      2.3 短信验证码每60秒可发送一次
      2.4 每个条件出错时有相应错误提示
      2.5 用手机号与密码登陆
      2.6 错误时有相应提示
      
#### 3、个人中心
  
      3.1 显示个人头像、手机号、用户名（用户名未设置时为用户手机号）
      3.2 个人头像采用七牛云存储技术实现对用户头像的存储
      3.3 用户名修改
      3.4 用户实名认证
      3.5 个人信息展示
      3.6 我的房源
      3.7 我的订单
      3.8 退出功能
      
#### 4、我的房源

      4.1 未实名认证的用户不能发布新房源信息
      4.2 按时间倒序显示已经发布的房屋信息
      4.3 点击房屋可以进入详情页面
      4.4 对实名认证的用户提供发布新房屋的入口
      
#### 5、客户订单(房东)
  
      5.1 按时间倒序显示用户下的订单
      5.2 对于新订单提供接单与拒单的功能
      5.3 拒单必须填写拒单原因
      5.4 提供客户对使用的房屋进行评价功能


### 此项目使用到的框架有：

alembic==0.9.4

certifi==2017.7.27.1

chardet==3.0.4

Flask==0.10.1

Flask-Migrate==2.1.0

Flask-Script==2.0.5

Flask-Session==0.3.1

Flask-SQLAlchemy==2.2

Flask-WTF==0.14.2

idna==2.5

itsdangerous==0.24

Jinja2==2.9.6

Mako==1.0.7

MarkupSafe==1.0

olefile==0.44

Pillow==4.2.1

pip==9.0.1

python-dateutil==2.6.1

python-editor==1.0.3

qiniu==7.1.4

redis==2.10.5

requests==2.18.3

setuptools==28.8.0

six==1.10.0

SQLAlchemy==1.1.12

urllib3==1.22

Werkzeug==0.12.2

wheel==0.29.0

WTForms==2.1


