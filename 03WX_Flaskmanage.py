from flask import Flask
from flask_script import Manager
from flask import render_template,Flask,request,redirect,json,url_for,Response
import requests
import pymysql

# 设置数据库所在主机IP地址
localhost = '192.168.0.109'

app = Flask(__name__)
manager = Manager(app=app)

## 第一次运行程序需要建立新的数据库,需要运行下面注释的一行代码，下次运行得将其注释掉，否则将会删除所有以前的数据。
# 在已有的数据库上创建新的数据库（CaiWu_WX_Flask_db）并同时创建新的数据表（CaiWu_WX_Flask_table）
def create_database():
    # 在mysql中创建数据库CaiWu_WX_Flask_db
    # 实例化一个数据库对象db，连接数据库所在主机IP，用户名，密码信息，连接上对应主机上的数据库
    db = pymysql.connect('localhost', 'root', 'root')
    # 给数据库设置字符集
    db.set_charset("utf8")
    # 数据库名字是：CaiWu_WX_Flask_db
    name = 'CaiWu_WX_Flask_db'
    # 实例化一个数据库的操作对象cursor
    cursor = db.cursor()
    # 如果存在“CaiWu_WX_Flask_db”这个数据库就删除，不存在就创建。
    cursor.execute('drop database if exists ' + name)
    cursor.execute('create database if not exists ' + name)
    # 释放db数据库实例
    db.close()

    # 在数据库CaiWu_WX_Flask_db中创建数据表CaiWu_WX_Flask_table，实例化一个数据库表的对象db
    db = pymysql.connect('localhost', 'root', 'root', 'CaiWu_WX_Flask_db')
    cursor = db.cursor()
    name = 'CaiWu_WX_Flask_table'
    cursor.execute('drop table if exists ' + name)
    sql = """create table CaiWu_WX_Flask_table(
        #设置id为主键,并且自动递增的
        id int(10) primary key AUTO_INCREMENT,  
        #也可以设置name为主键且不为空: 
        1name varchar(30) not null,      
        # name varchar(30) not null,
        2BaoXiaoFrom varchar(10) not null, 
        3Money varchar(20) not null,       
        4Explain varchar(30) not null,
        5FaPiao varchar(10) not null, 
        6ShuJu varchar(10) not null,
        7XianJinRecord varchar(10) not null,
        8NetPayRecord varchar(10) not null,       
        9is_Apply  varchar(10) not null,       
        10Area varchar(10) not null, 
        11BaoXiaoData varchar(10) not null,       
        12is_dev varchar(10) not null)
        # is_delete int(10) default 0 not null)  #设置默认值为0
        """
    cursor.execute(sql)
    # 将改动的数据库的信息进行更新同步保存操作
    db.commit()
    # 断开数据库链接
    db.close()

#数据库新的数据的插入
def insert_db(name, BaoXiao_from, BaoXiao_Money,Explain,bill0, bill1,Payment_Record0,Payment_Record1,is_Apply,area,date,is_dev):
    db = pymysql.connect('localhost', 'root', 'root','CaiWu_WX_Flask_db')
    cursor = db.cursor()
    sql = "insert into CaiWu_WX_Flask_table (1name,2BaoXiaoFrom,3Money,4Explain,5FaPiao,6ShuJu,7XianJinRecord,8NetPayRecord,9is_Apply,10Area,11BaoXiaoData,12is_dev) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          (name, BaoXiao_from, BaoXiao_Money,Explain,bill0, bill1,Payment_Record0,Payment_Record1,is_Apply,area,date,is_dev)
    #执行SQL语句
    cursor.execute(sql)
    #将更改同步更新到数据库中去，才会生效，才算是保存成功
    db.commit()
    #断开数据库链接
    db.close()

'''参考flask代码：
@app.route('/hello')
def hello():
    return render_template("hello.html")
#---------------------------------------
#flask传递浏览器的参数信息
#http://127.0.0.1:9000/params/<hehe>/
#在浏览器中（输入：http://127.0.0.1:9000/params/<he>/）通过传递给params请求体一个参数<hehe>( < >内可以是任意内容，但是要有，
# 浏览器传递过来的参数信息内容就赋值到hehe这个变量中了)，以此就可以在浏览器网页上得到后台flask服务器返回给浏览器的信息内容："params获取参数"
#在浏览器通过在get/< >/中括号中输入内容，当浏览器执行这请求时候，这个内容就会被传递到后台flask服务器中来，此例子是将传递进来的参数赋值给hehe变量。
@app.route('/params/<hehe>/')
def params(hehe="你呵呵",ooo=110):
    print(type(hehe))
    print(hehe)
    return "params获取参数是：hehe%s"
    
    #http://127.0.0.1:9000/request/
#request请求传递参数信息,需要导入request方法
@app.route('/request/',methods=['GET','POST'])
def req():
    # print(request)
    # print(type(request))
    # print(request.args.get("name"))
    
    print(request.data)
    #arg:参数，get请求方法
    print(request.args.get('name'))
    #获取所有的参数值-getlist：
    print(request.args.getlist('password'))
    return "request请求获取浏览器的参数 传递给后台服务器"
#---------------------------------------
'''

#http://127.0.0.1:9000/request/
#request请求传递参数信息,需要导入request方法
@app.route('/request/',methods=['GET','POST'])
def req():
    #使用json无法传输中文
    # input_txt1 = str(json.loads(request.values.get("txt1")))
    #这个是用来与 ”0微信小程序与Flask后端数据交互-from手机号码查询练习“ 这个微信小程序进行
    #接收来自微信小程序上的数据信息，并赋值给变量用于python操作。
    BaoXiao_Money = request.values.get("BaoXiao_Money1")
    input_txt2 = request.values.get("BaoXiao_Money1")
    BaoXiao_from = request.values.get("BaoXiao_from1")
    Explain = request.values.get("Explain1")
    Payment_Record0 = request.values.get("Payment_Record0")
    Payment_Record1 = request.values.get("Payment_Record1")
    area = request.values.get("area1")
    #因为微信小程序传递至后端指明来自于哪里是传递的数据，不是文字信息，因此要做个判断，以输出到数据库中是文字形式
    if int(area) == 0:
        area = "铁电"
    elif int(area) == 1:
        area = "第三工程部"
    elif int(area) == 2:
        area = "财务部"
    elif int(area) == 3:
        area = "技术部"
    elif int(area) == 4:
        area = "中科土壤"
    elif int(area) == 5:
        area = "安通检测"
    bill0 = request.values.get("bill0")
    bill1 = request.values.get("bill1")
    date = request.values.get("date1")
    is_Apply = request.values.get("is_Apply1")
    username = request.values.get("username1")
    is_dev = request.values.get("is_dev1")

    # print(BaoXiao_Money)    # print(type(BaoXiao_Money))    # print(BaoXiao_from)    # print(type(BaoXiao_from))    # print(Explain)    # print(type(Explain))
    # print(bill0)    # print(type(bill0))    # print(bill1)    # print(type(bill1))    # print(date)    # print(type(date))
    # print(area)    # print(type(area))    # print(is_Apply)    # print(type(is_Apply))

    #如果传递进来的数据不为空则链接到数据库中去进行保存。
    if username != 'null':
        name = username
       #name还是字符串类型，可以实现将字符串和数字类型的数据存到MySQL数据库中去。

        # 将微信小程序客户端传过来的信息保存到MySQL80数据库中去。
        insert_db(name, BaoXiao_from, BaoXiao_Money,Explain,bill0, bill1,Payment_Record0,Payment_Record1,is_Apply,area,date,is_dev)

        # print("3:%s"% request.data)
        # #arg:参数，get请求方法
        # print("4:%s"% request.args.get('name'))
        # #获取所有的参数值-getlist：
        # print("5:%s"% request.args.getlist('password'))
        # return是一旦后端Flask接收到来自微信小程序的数据后，会自动返回下面这个数据，用于提示后端已经接收到微信小程序的数据了
        return "数据提交后端Flask保存成功，已获取微信小程序数据"
    # else:
    #     return "提交数据失败"
#---------------------------------------
if __name__ == '__main__':
    # 第一次运行程序需要建立新的数据库,需要运行下面注释的一行代码，下次运行得将其注释掉，否则将会删除所有以前的数据
    # create_database()

    #使用app直接运行模式，可以手动设置是否进入调试模式
    # app.run(debug=True,port=8000,host='0.0.0.0')
    # app.run()

    #使用managr管理APP运行模式，是综合调试，可是实时与前端后端交互数据，但是需要在终端中输入以下命令：
    # python 03WX_Flaskmanage.py runserver -d -r -h 0.0.0.0 -p 9000  -d:调试模式，-r自动加载修改后代码 0.0.0.0任何人都可以访问
    # ，方可进行进行调试，否则直接点击调试还是不会开启调试功能的，建议用manager模式。
    #但是该调试时，建议用manager。
    manager.run()
