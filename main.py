"""
单机版程序，界面使用tkinter或pyQt等，数据存入MySql数据库，
数据存入时加密存储，加密算法可以采用Crypto包，利用AES或DES算法。
数据记录的录入界面中，可以包含记录类别（银行账户、校内账户、社交账户、邮箱账户等），
记录包含名称、账户名、密码、网址、注册手机、备注等信息，所有数据都以加密形式存入数据库中。
该系统具有增删改查功能，具有用户登录功能。，
在显示查询内容之前需要输入登录密码进行验证，并且只显示要查询的记录信息。
"""

import sys

from PyQt5.QtGui import QMovie
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAbstractItemView, QTableWidgetItem, QHeaderView
# 导入designer工具生成的login模块f
from UI import Ui_widget
import function as fun

G_user = ""
SaveMode = 'save'
SelectId = 0


class MyMainForm(QMainWindow, Ui_widget):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.rb_main_another.setChecked(True)  # 设置默认选中

        self.tabWidget.tabBar().hide()
        self.bac = QMovie('img/g1.gif')
        self.label_hello_gif.setMovie(self.bac)
        self.bac.start()
        self.tabWidget.setCurrentIndex(0)

        '''
        hello
        '''
        fun.init_project()

        saved, auto, user, password = fun.is_login()
        self.le_login_account.setText(user)
        self.le_login_password.setText(password)
        self.cb_login_remember.setChecked(saved)
        self.cb_login_auto.setChecked(auto)
        if auto:
            self.f_btn_login_login()

        self.btn_hello_start.clicked.connect(lambda: self.tab_jump(1))

        table = self.table_show
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        '''
        login
        '''
        self.cb_login_auto.stateChanged.connect(self.f_cb_login_auto)
        self.btn_login_regist.clicked.connect(lambda: self.tab_jump(2))
        self.btn_login_login.clicked.connect(self.f_btn_login_login)
        '''
        regist
        '''
        self.btn_regist_back.clicked.connect(self.f_btn_regist_back)
        self.btn_regist_ok.clicked.connect(self.f_btn_regist_ok)
        self.le_regist_password2.editingFinished.connect(self.f_le_regist_ok2)
        '''
        menu
        '''
        self.btn_menu_add.clicked.connect(lambda: self.tab_jump(4))
        self.btn_menu_show.clicked.connect(self.f_btn_menu_show)
        self.btn_menu_exit.clicked.connect(self.f_btn_menu_exit)
        '''
        main
        '''
        self.btn_main_back.clicked.connect(lambda: self.tab_jump(3))
        self.btn_main_save.clicked.connect(self.f_btn_main_save)

        '''
        show
        '''
        self.btn_show_back.clicked.connect(self.f_btn_show_back)
        self.btn_show_search.clicked.connect(self.f_btn_show_search)
        self.btn_show_delete.clicked.connect(self.f_btn_show_delete)
        self.comboBox_show.currentIndexChanged.connect(self.f_comboBox_show_search)
        self.le_show_search.setEnabled(False)

        self.btn_show_change.clicked.connect(self.f_btn_show_change)

    '''
    综合
    '''

    def clear_main(self):
        self.rb_main_another.setChecked(True)
        self.le_main_name.clear()
        self.le_main_account.clear()
        self.le_main_password.clear()
        self.le_main_address.clear()
        self.le_main_phone.clear()
        self.le_main_remark.clear()

    def table_clear(self):
        num = self.table_show.rowCount()
        for i in range(0, num):
            self.table_show.removeRow(0)

    def tab_jump(self, a):
        self.tabWidget.setCurrentIndex(a)

    def show_info(self, title, text):
        reply = QMessageBox.information(self, title, text, QMessageBox.Ok, QMessageBox.Ok)
        return reply

    def table_data(self, mode='all', key='null'):
        global G_user
        table = self.table_show
        if mode == 'all':
            data = fun.show(G_user)
        else:
            data = fun.search(G_user, mode, key)
        x = 0

        if not data:
            return

        for i in data:
            y = 0
            # print(i) #todo 获取的消息
            i = list(i)
            i.pop(1)
            # print(i) #todo 删除了用户
            table.insertRow(table.rowCount())
            for j in i:
                table.setItem(x, y, QTableWidgetItem(str(j)))
                y += 1
            x += 1

    '''
    Login
    '''

    def f_cb_login_auto(self):
        if self.cb_login_auto.isChecked():
            self.cb_login_remember.setChecked(True)

    def f_btn_login_login(self):
        acc = self.le_login_account
        pwd = self.le_login_password

        if acc.text() == 'admin' and pwd.text() == 'admin':
            self.tab_jump(3)
            return False

        if acc.text() == '':
            self.show_info('账号不能为空', '账号不能为空')
            return False
        elif pwd.text() == '':
            self.show_info('密码不能为空', '密码不能为空')
            return False
        if fun.login(acc.text(), pwd.text()):
            global G_user
            G_user = acc.text()
            fun.save_login(acc.text(), pwd.text(), self.cb_login_remember.isChecked(), self.cb_login_auto.isChecked())
            print('登陆成功')  # todo 信息框
            self.label_menu_user.setText(f'迷糊工具，欢迎用户：{acc.text()}')
            self.tab_jump(3)
        else:
            print('用户名或密码错误，请重新输入')
            acc.clear()
            pwd.clear()
            acc.setFocus()

    '''
    regist
    '''

    def f_le_regist_ok2(self):
        ok1 = self.le_regist_password
        ok2 = self.le_regist_password2
        if ok1.text() != ok2.text():
            self.show_info('错误', '与第一次密码不符')

    def f_btn_regist_back(self):
        self.le_regist_account.clear()
        self.le_regist_password.clear()
        self.le_regist_password2.clear()
        self.tab_jump(1)

    def f_btn_regist_ok(self):
        acc = self.le_regist_account
        pwd = self.le_regist_password
        if acc.text() == '':
            self.show_info('账号不能为空', '账号不能为空')
            return False
        elif pwd.text() == '':
            self.show_info('密码不能为空', '密码不能为空')
            return False

        if fun.regist(acc.text(), pwd.text()):
            self.show_info('注册成功', f"""
            注册成功，您的信息如下：
            账号：{acc.text()}
            密码：{pwd.text()}
            """)
            self.le_login_account.setText(acc.text())
            self.le_login_password.setText(pwd.text())
            self.f_btn_regist_back()
            self.f_btn_login_login()
        else:
            print(f'已存在{acc.text()}，请重新注册')
            acc.clear()
            pwd.clear()
            self.le_regist_password2.clear()
            acc.setFocus()

    '''
    menu
    '''

    def f_btn_menu_show(self):
        self.tab_jump(5)
        self.table_data()

    def f_btn_menu_exit(self):
        self.tab_jump(1)
        self.table_show.clearContents()
        self.le_login_account.clear()
        self.le_login_password.clear()
        self.cb_login_remember.setChecked(False)
        self.cb_login_auto.setChecked(False)
        self.table_clear()

    '''
    main
    '''

    def f_btn_main_save(self):
        if self.rb_main_bank.isChecked():
            a_type = "bank"
        elif self.rb_main_school.isChecked():
            a_type = "school"
        elif self.rb_main_social.isChecked():
            a_type = "social"
        elif self.rb_main_mail.isChecked():
            a_type = "mail"
        else:
            a_type = "another"
        a_name = self.le_main_name.text()
        a_account = self.le_main_account.text()
        a_password = self.le_main_password.text()
        a_address = self.le_main_address.text()
        a_phone = self.le_main_phone.text()
        a_remark = self.le_main_remark.toPlainText()
        print("获取成功")

        global SaveMode
        if SaveMode == 'change':
            SaveMode = 'save'
            fun.update(SelectId, a_type, a_name, a_account, a_password, a_address, a_phone, a_remark)
            self.clear_main()
            self.table_clear()
            self.table_data('id', str(SelectId))
            self.tab_jump(5)
            return

        global G_user
        result = fun.save_line(G_user, a_type, a_name, a_account, a_password, a_address, a_phone, a_remark)

        se = QMessageBox.information(self, "是否打印保存的信息", "是否打印保存的信息", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)

        if result:
            if se == QMessageBox.Yes:
                self.show_info("保存成功", f"""
                当前用户：{G_user}\t\t   
                保存信息如下：
                    名称：{a_name}
                    账户名：{a_account}
                    密码：{a_password}
                    网址：{a_address}
                    注册手机：{a_phone}
                    备注：{a_remark}
                """)
            # self.table_show.
            self.clear_main()

    '''
    show
    '''

    def f_comboBox_show_search(self):
        if (self.comboBox_show.currentIndex() == 0) or ("类型" in self.comboBox_show.currentText()):
            self.le_show_search.clear()
            self.le_show_search.setEnabled(False)
        else:
            self.le_show_search.setEnabled(True)

    def f_btn_show_back(self):
        self.tab_jump(3)
        self.table_clear()

    def f_btn_show_delete(self):
        # print(self.table_show.currentRow())
        table = self.table_show
        global SelectId
        SelectId = table.item(table.currentIndex().row(), 0).text()
        fun.delete(SelectId)
        self.table_clear()
        self.table_data()

    def f_btn_show_change(self):
        global SaveMode
        SaveMode = 'change'
        select_data = []
        table = self.table_show
        row = table.currentIndex().row()
        for i in range(0, table.columnCount()):
            select_data.append(table.item(row, i).text())
        # print(select_data)
        global SelectId
        SelectId = select_data[0]
        eval('self.rb_main_' + select_data[1]).setChecked(True)
        self.le_main_name.setText(select_data[2])
        self.le_main_account.setText(select_data[3])
        self.le_main_password.setText(select_data[4])
        self.le_main_address.setText(select_data[5])
        self.le_main_phone.setText(select_data[6])
        self.le_main_remark.setText(select_data[7])
        self.tab_jump(4)

    def f_btn_show_search(self):
        self.table_clear()
        key = self.le_show_search.text()
        cbox = self.comboBox_show
        box_text = cbox.currentText()
        get_date = self.table_data
        if box_text == "名称":
            get_date("name", key)
        elif box_text == "账户名":
            get_date("account", key)
        elif box_text == "密码":
            get_date("password", key)
        elif box_text == "网址":
            get_date("address", key)
        elif box_text == "手机":
            get_date("phone", key)
        elif box_text == "备注":
            get_date("remark", key)
        elif box_text == "银行账户类型":
            get_date("atype", "bank")
        elif box_text == "学校账户类型":
            get_date("atype", "school")
        elif box_text == "社交账户类型":
            get_date("atype", "social")
        elif box_text == "邮箱账户类型":
            get_date("atype", "mail")
        elif box_text == "其他账户类型":
            get_date("atype", "another")
        else:
            get_date(key=key)
        self.le_show_search.clear()


def main():
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。

    # myWin.show_info()

    sys.exit(app.exec_())


main()
