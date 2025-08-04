from PyQt5.QtWidgets import QAction

class MenuBar:
    def __init__(self, parent, window, change_page_method):
        self.parent = parent
        self.change_page = change_page_method
        self.create_menu_bar(window)

    def create_menu_bar(self, window):
        # Create the menu bar
        self.menu_bar = self.parent.menuBar()
        # for macOS, must setNativeMenuBar to show the menu bar
        self.menu_bar.setNativeMenuBar(False)

        # create menu items
        encryption_item = self.create_menu_item("Encryption", lambda : self.change_page(2))
        decryption_item = self.create_menu_item("Decryption", lambda : self.change_page(3))
        about_item = self.create_menu_item("About", is_menu = True)
        project_item = self.create_menu_item("Introduction", lambda : self.change_page(0), about_item)
        credits_item = self.create_menu_item("Credits", lambda : self.change_page(1), about_item)
        quit_item = self.create_menu_item("Quit", self.parent.close, None, "Ctrl+Q")


    def create_menu_item(self, item_text, connect_method = None, parent_item_text = None, shortcut = None, is_menu = False):
        if is_menu:
            # create menu
            menu = self.menu_bar.addMenu(item_text)
            self.menu_bar.addSeparator()
            return menu
        else:
            if parent_item_text:
                # add parent menu item
                menu_item = QAction(item_text, self.parent)
                parent_item_text.addAction(menu_item)
                menu_item.triggered.connect(connect_method)
                self.menu_bar.addSeparator()
            else:
                # add menu item
                menu_item = QAction(item_text, self.parent)
                self.menu_bar.addAction(menu_item)
                menu_item.triggered.connect(connect_method)
                self.menu_bar.addSeparator()

            if shortcut:
                # add shortcut
                menu_item.setShortcut(shortcut)
            return  menu_item
