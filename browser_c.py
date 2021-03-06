from asyncio import Event
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys
from PyQt5 import QtCore
SavePageEvent = QWebEnginePage.SavePage
OpenLinkInNewTabEvent = QWebEnginePage.OpenLinkInNewTab

from models import *
from utils import *
from style import loader


########classe pour afficher le page de connexion ###################
class Ui_ConnectForm(QWidget):

    def __init__(self, mainwindow):
        super(Ui_ConnectForm, self).__init__()
        self.setupUi()
        self.installEventFilter(self)
        self.mainwindow=mainwindow
     
    def setupUi(self):  
        self.setFixedSize(300, 200)
        self.setWindowTitle("connexion au compte")
        self.Usernameedit = QLineEdit()
        self.Passwordedit = QLineEdit()
        self.Passwordedit.setEchoMode(QLineEdit.Password)

        self.connecterButton = QPushButton()
        self.cancelButton = QPushButton()
        self.connecterButton.clicked.connect(self.getValues)
        self.cancelButton.clicked.connect(lambda: self.close())
 
        self.connecterButton.setText("Connecter")
        self.cancelButton.setText("Cancel")
        self.Usernameedit.setPlaceholderText("Username")
        self.Passwordedit.setPlaceholderText("Password")
         
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.Usernameedit)
        vbox.addWidget(self.Passwordedit)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.connecterButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
         
    def getValues(self):
        user=User.get(User.username == self.Usernameedit.text(),User.password==self.Passwordedit.text())
        if user is not None:
            t=self.Usernameedit.text()
            self.mainwindow.close()
            t=t[0:2].capitalize()
            main=MainWindow(lt=t, con=True)
            self.close()
        else:
            msg = QMessageBox.warning(None, "Error", "mom d'utilisateur ou mot de passe incorrect" )
            return
########classe pour afficher le page de cr??ation de compte ###################
class Ui_RegisterForm(QWidget):

    def __init__(self, mainwindow):
        super(Ui_RegisterForm, self).__init__()
        self.setupUi()
        self.installEventFilter(self)
        self.mainwindow=mainwindow
     
    def setupUi(self):  
        self.setFixedSize(300, 200)
        self.setWindowTitle("Make a new account ")
        self.Usernameedit = QLineEdit()
        self.Passwordedit = QLineEdit()
        self.confirmPasswordedit = QLineEdit()
        self.Passwordedit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordedit.setEchoMode(QLineEdit.Password)
         
        self.confirmButton = QPushButton()
        self.cancelButton = QPushButton()
        self.confirmButton.clicked.connect(self.getValues)
        self.cancelButton.clicked.connect(lambda: self.close())
 
        self.confirmButton.setText("Confirm")
        self.cancelButton.setText("Cancel")
        self.Usernameedit.setPlaceholderText("Username")
        self.Passwordedit.setPlaceholderText("Password")
        self.confirmPasswordedit.setPlaceholderText("Confirm Password")
        self.confirmPasswordedit.returnPressed.connect(self.getValues)
         
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.Usernameedit)
        vbox.addWidget(self.Passwordedit)
        vbox.addWidget(self.confirmPasswordedit)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.confirmButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
         
    def getValues(self):
        if self.Passwordedit.text() == self.confirmPasswordedit.text():
            #values = [self.Usernameedit.text(), self.Passwordedit.text(), self.confirmPasswordedit.text()]
            user= User.create(username=self.Usernameedit.text(), password=self.Passwordedit.text())
            user.save()
            t=self.Usernameedit.text()
            print(t)
            self.mainwindow.close()
            t=t[0:2].capitalize()
            main=MainWindow(lt=t, con=True)
            self.close()
        else:
            msg = QMessageBox.warning(None, "Error", "passwords not matching" )
            return
             
################################################################
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(QWebEnginePage, self).__init__(*args, **kwargs)
        self.initialise_tab

    # Store external windows.
    external_windows = []
    my_web_signal = pyqtSignal(object)
    def initialise_tab(self):
        settings = QWebEngineSettings.globalSettings

        # did not seem to work
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.OfflineWebApplicationCacheEnabled, True)
        settings.enablePersistentStorage('cache.txt')

        # added this because github was resquesting it
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True) 

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        # if _type == QWebEnginePage.NavigationTypeLinkClicked:
        #     w = MainWindow(init_url=url)
        #     self.external_windows.append(w)
        #     return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def triggerAction(self, action, bool):
        if action == QWebEnginePage.SavePage:
            self.save_file()
        elif action == QWebEnginePage.ViewSource:
            self.toHtml(self.page_to_text)
        elif action == QWebEnginePage.OpenLinkInNewTab:
            data = self.contextMenuData()
            url = data.linkUrl()
            self.my_web_signal.emit({"event": OpenLinkInNewTabEvent, "url": url})
        elif action == QWebEnginePage.OpenLinkInNewWindow:
            data = self.contextMenuData()
            url = data.linkUrl()
            w = MainWindow(init_url=url)
            self.external_windows.append(w)

    def action(self, _action):
        print(_action)
        return super().action(_action)

    def save_file(self):
        self.my_web_signal.emit({"event": SavePageEvent})
        # filename, _ = QFileDialog.getSaveFileName(
        #     None,
        #     "Save Page As",
        #     "",
        #     "Hypertext Markup Language (*.htm *html);;" "All files (*.*)",
        # )

        # if filename:
        #     self.save(filename, QWebEngineDownloadItem.CompleteHtmlSaveFormat)

    def page_to_text(self, txt):
        # print(txt)
        # Get the text and either send a signal or something and see how to display the html content
        pass


def create_db_tables():
    db.create_tables([Folder, History, Bookmark, Link, User])
    # db.drop_tables([])
             
################################################################
class MainWindow(QMainWindow):
    def __init__(self, lt, con=False, init_url=None, *args, **kwargs):
        self.init_url = init_url
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.lt=lt
        self.setStyleSheet(loader.StyleLoader.load_style())
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(20, 20))
        navtb.setStyleSheet(loader.StyleLoader.load_style())
        self.addToolBar(navtb)

        self.bookmarks = get_bookmarks()

        back_btn = QAction(QIcon(os.path.join("images", "arrow-left.png")), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.back_btn_pressed)
        navtb.addAction(back_btn)

        next_btn = QAction(
            QIcon(os.path.join("images", "right-arrow.png")), "Forward", self
        )
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(
            QIcon(os.path.join("images", "reload.png")), "Reload", self
        )
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join("images", "home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-nossl.png")))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        
        ########################  stop button   ##################################
        stop_btn = QAction(
            QIcon(os.path.join("images", "cross.png")), "Stop", self
        )
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        ##################### insert user cercle when connected #################
        if(con):
            self.label_1 = QLabel(self.lt, self)
            #self.label_1.resize(80,80)
            self.label_1
            self.label_1.setStyleSheet("background-color:white;border: 3px solid blue;border-radius: 40px;")
            navtb.addWidget(self.label_1)   
        #########################################################################
        left_tb = QMenuBar()

        left_tb.setLayoutDirection(Qt.RightToLeft)

        menu = left_tb.addMenu(QIcon(os.path.join("images", "menu.png")), 'menu')
        ########### ajouter un  button de cr??ation de compte au menu  ##################
        
        new_tab_action = QAction("cr??er un compte", self)  
        new_tab_action.setStatusTip("cr??er un compte")
        new_tab_action.triggered.connect(self.createaccount)
        menu.addAction(new_tab_action)
        ############### ajouter un button de connexion au menu  ##################
        
        new_tab_action = QAction("connexion", self)  
        new_tab_action.setStatusTip("connexion")
        new_tab_action.triggered.connect(self.navconnexion)
        menu.addAction(new_tab_action)
        
        ############### ajout du  button de open New Tab au menu ##################
        
        new_tab_action = QAction(
            QIcon(os.path.join("images", "ui-tab--plus.png")), "Open New Tab", self
        )
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        menu.addAction(new_tab_action)
        
        #########################################################################

        file_menu = menu.addMenu("File")

        open_file_action = QAction(
            QIcon(os.path.join("images", "disk--arrow.png")), "Open file...", self
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(os.path.join("images", "disk--pencil.png")), "Save Page As...", self
        )
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(
            QIcon(os.path.join("images", "printer.png")), "Print...", self
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        #########################################################################

        self.bookmark_menu = menu.addMenu("History")
        # test load data to bookmarks
        for _link in self.bookmarks:
            bookmark_action = QAction(_link.text, self)
            bookmark_action.setStatusTip(_link.link)
            bookmark_action.triggered.connect(
                lambda _, url=_link.link: self.handle_bookmark_link_clicked(url)
            )
            self.bookmark_menu.addAction(bookmark_action)
        favourite_action = QAction(
            QIcon(os.path.join("images", "ui-tab--plus.png")), "Favourites", self
        )
        favourite_action.setStatusTip("Favourites")
        favourite_action.triggered.connect(lambda _: self.add_new_tab())
        menu.addAction(favourite_action)

        menu.addMenu("&Help")

        # for 16X16 icons the max size is 35X number of menus (icons)
        left_tb.setMaximumWidth(35)
        navtb.addWidget(left_tb)

        if self.init_url == None:
            self.add_new_tab(QUrl("http://www.google.com"), "Homepage")
        else:
            self.add_new_tab(QUrl(self.init_url))

        self.show()

        self.setWindowTitle("eSearch")
        self.setWindowIcon(QIcon(os.path.join("images", "ma-icon-64.png")))

    def add_new_tab(self, qurl=None, label="Blank"):

        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(self))


        if qurl is None:
            qurl = QUrl("")
            filename = "index.html"
            with open(filename, "r") as f:
                html = f.read()

            browser.setHtml(html)
            self.urlbar.setText(filename)
        else:
            browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        # More difficult! We only want to update the url when it's from the
        # correct tab
        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_urlbar(qurl, browser)
        )

        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.browser_load_finished(_, i, browser)
        )
        browser.page().my_web_signal.connect(self.handle_web_event)

    def browser_load_finished(self, flag, i, browser):
        self.tabs.setTabText(i, browser.page().title())
        url = browser.url().url()

        # add to history
        add_history(url, browser.title())
        self.add_link_to_bookmark(browser.title())

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()
        
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - eSearch" % title)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Hypertext Markup Language (*.htm *.html);;" "All files (*.*)",
        )

        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *html);;" "All files (*.*)",
        )

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, "w") as f:
                f.write(html.encode("utf8"))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == "https":
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-ssl.png")))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-nossl.png")))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_last_tab(self):
        new_tab_action = QIcon(os.path.join("images", "ui-tab--plus.png"))
        self.tabs.setTabIcon(-1, new_tab_action)
        self.tabs.setIconSize(QtCore.QSize(32, 32))

    def handle_web_event(self, data_obj):
        if "event" in data_obj:
            if data_obj["event"] == OpenLinkInNewTabEvent:
                url = data_obj["url"]
                self.add_new_tab(qurl=url)
            elif data_obj["event"] == SavePageEvent:
                self.save_file()

    def handle_bookmark_link_clicked(self, url=None):
        self.tabs.currentWidget().setUrl(QUrl(url))

    def add_link_to_bookmark(self, title):

        menus = self.findChildren(QMenu)
        for menu in menus:
            if menu.title() == "History":
                menu.clear()
                bookmarks = get_bookmarks()
                for _link in bookmarks:
                    bookmark_action = QAction(_link.text, self)
                    bookmark_action.setStatusTip(_link.link)
                    bookmark_action.triggered.connect(
                        lambda _, url=_link.link: self.handle_bookmark_link_clicked(url)
                    )
                    menu.addAction(bookmark_action)

    def update_toolbar(self):
        pass

    def back_btn_pressed(self):
        print(type(self.tabs.currentWidget()))
        self.tabs.currentWidget().back()
    def navconnexion(self):
        mainWin = Ui_ConnectForm(self)
        mainWin.show()
    def createaccount (self):
        mainWin = Ui_RegisterForm(self)
        mainWin.show()    
        
            
       


create_db_tables()

app = QApplication(sys.argv)
app.setApplicationName("eSearch")
app.setOrganizationName("eSearch")
app.setOrganizationDomain("eSearch")

window = MainWindow('')

app.exec_()


