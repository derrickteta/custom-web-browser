# from PyQt5.QtWebEngineWidgets import *
# from PyQt5.QtPrintSupport import *

class CustomWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(QWebEngineView, self).__init__(*args, **kwargs)
        self.initialise_tab()

    def initialise_tab(self):
        settings = self.settings()

        # did not seem to work
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

        # added this because github was resquesting it
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(QWebEnginePage, self).__init__(*args, **kwargs)

    # Store external windows.
    external_windows = []
    my_web_signal = pyqtSignal(object)

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

