import base64
import os
import pymysql
import configparser

from Crypto.Cipher import AES

db_name = "db_arc"
host = 'localhost'  #打包程序中使用的云服务器中的mysql server
user = 'root'
pwd = '123456'

table_user = db_name + ".user" #用户表
table_info = db_name + ".info"#信息表

G_key = '123456'#全局加密密钥

def init_project():
    filename = "user.ini"
    config = configparser.ConfigParser()
    if not (os.path.isfile(filename)):
        open('user.ini', 'x', encoding='utf-8').close()
        config.read(filename)
        config.add_section("user")
        config.add_section("set")

        config.set("user", "user", "")
        config.set("user", "password", "")
        config.set("set", "saved", "False")
        config.set("set", "auto", "False")

        with open(filename, "w", encoding='utf-8') as config_file:
            config.write(config_file)
        config_file.close()
    else:
        config.read(filename)

def connect_sql():
    conn = pymysql.connect(
        host=host,
        user=user,
        password=pwd,
        database=db_name
    )
    cur = conn.cursor()
    return cur, conn


def login(user, password):
    cur, conn = connect_sql()
    sql = f"select password from {table_user} where user='{user}'"
    # print(sql)
    print(cur.execute(sql))
    # 返回的是查询的数据条数
    data = cur.fetchall()
    # print(data)
    if data is None:
        return False
    if password == jiemi(data[0][0]):
        cur.close()
        conn.close()
        return True
    cur.close()
    conn.close()
    return False


def regist(user, password):
    cur, conn = connect_sql()
    sql = f"select password from {table_user} where user='{user}'"
    num = cur.execute(sql)
    # data = cur.fetchall()
    if num != 0:
        return False
    password = jiami(password)
    sql = f"insert into {table_user} values (null,'{user}','{password}')"
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    cur.close()
    conn.close()
    return True


def save_login(user, password="", saved=False, auto=False):#自动登录保存
    if not saved:
        password = ""

    filename = "user.ini"
    config = configparser.ConfigParser()
    config.read(filename)

    config.set("user", "user", user)
    config.set("user", "password", jiami(password))
    config.set("set", "saved", str(saved))
    config.set("set", "auto", str(auto))

    with open(filename, "w", encoding='utf-8') as config_file:
        config.write(config_file)
    config_file.close()


def is_login():  # 自动登录
    filename = "user.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    return eval(config.get("set", 'saved')), eval(config.get("set", "auto")), config.get("user",
                                                                                         "user"), jiemi(
        config.get(
            "user", "password"))


def save_line(user, atype, name, account, password, address, phone, remark):
    atype = jiami(atype)
    name = jiami(name)
    account = jiami(account)
    password = jiami(password)
    address = jiami(address)
    phone = jiami(phone)
    remark = jiami(remark)

    cur, conn = connect_sql()
    sql = f"insert into {table_info} values (null,'{user}','{atype}','{name}','{account}','{password}','{address}','{phone}','{remark}')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return True


def show(user):
    # 输出当前用户所有账号信息
    cur, conn = connect_sql()
    sql = f"select * from {table_info} where user ='{user}'"
    num = cur.execute(sql)  # 返回的是查询的数据条数
    data = cur.fetchall()
    cur.close()
    conn.close()

    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        for j in range(2, len(data[i])):
            data[i][j] = jiemi(data[i][j])

    if num == 0:
        return False

    return data


def search(user, mode, key):
    cur, conn = connect_sql()
    if mode == 'id':
        key = int(key)
        sql = f"select * from {table_info} where {mode} like {key} and user = '{user}'"
    else:
        key = jiami(key)
        sql = f"select * from {table_info} where {mode} like '{key}' and user = '{user}'"

    print(num := cur.execute(sql))
    # 返回的是查询的数据条数
    if num == 0:
        return False
    data = cur.fetchall()
    cur.close()
    conn.close()

    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        for j in range(2, len(data[i])):
            data[i][j] = jiemi(data[i][j])

    return data


def update(id, *args):
    cur, conn = connect_sql()
    print(args)
    args = list(args)
    for i in range(0, len(args)):
        args[i] = jiami(args[i])

    sql = f"update {table_info} set atype='{args[0]}',name='{args[1]}',account='{args[2]}',password='{args[3]}',address='{args[4]}',phone='{args[5]}',remark='{args[6]}' where id='{id}'"
    print(cur.execute(sql))
    conn.commit()
    cur.close()
    conn.close()


def delete(a_id):
    cur, conn = connect_sql()
    sql = f"delete from {table_info} where id = {a_id}"
    print(cur.execute(sql))
    conn.commit()
    cur.close()
    conn.close()


# 把str补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 转化为bytes


# 加密
def jiami(text):
    # 秘钥
    global G_key
    # 初始化加密器
    aes = AES.new(add_to_16(G_key), AES.MODE_ECB)
    # aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text.replace("\n", "")  # base64会存在\n的情况


# 解密
def jiemi(text):
    # 秘钥
    global G_key
    # 初始化加密器
    aes = AES.new(add_to_16(G_key), AES.MODE_ECB)
    # 逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypted_text
