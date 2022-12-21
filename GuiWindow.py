import sqlite3 as sql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QRadioButton, QMessageBox, \
    QListWidget, QCheckBox


class search_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("search database")
        self.label = QLabel(self)
        self.search_bar = QLineEdit(self)
        self.finalize = QPushButton(self)
        self.table = QListWidget(self)
        self.pc = QCheckBox(self)
        self.console = QCheckBox(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 437, 454)
        self.label.setText("Search Database")
        self.label.resize(91, 61)
        self.label.move(170, 0)

        self.search_bar.resize(113, 20)
        self.search_bar.move(10, 80)
        self.search_bar.setPlaceholderText("Enter Game Title")

        self.finalize.move(140, 80)
        self.finalize.resize(75, 23)
        self.finalize.setText("search")
        self.finalize.clicked.connect(self.search)

        self.console.move(320, 50)
        self.console.resize(70, 17)
        self.console.setText("Console")

        self.pc.move(320, 70)
        self.pc.resize(70, 17)
        self.pc.setText("PC")

        self.table.resize(411, 301)
        self.table.move(10, 110)

    def search(self):
        self.table.clear()
        conn = sql.connect("game_database.sqlite3")
        cursor = conn.cursor()

        query = self.search_bar.text()
        pc = self.pc.isChecked()
        console = self.console.isChecked()

        if pc == True and console == True:
            sql2=(f"""SELECT * From Console WHERE Console.title LIKE '{query}%'""")
            cursor.execute(sql2)
            results = cursor.fetchall()
            for x in results:
                input=str(x)
                self.table.addItem(input)
            sql2=(f"""SELECT * From PC WHERE title LIKE '{query}%'""")
            cursor.execute(sql2)
            results2=cursor.fetchall()
            for x in results2:
                input=str(x)
                self.table.addItem(input)
        elif pc:
            sql2 = (f"""SELECT * From PC WHERE title LIKE '{query}%'""")
            cursor.execute(sql2)
            results = cursor.fetchall()
            for x in results:
                input=str(x)
                self.table.addItem(input)
        elif console:
            sql2 = (f"""SELECT * From Console WHERE Console.title LIKE '{query}%'""")
            cursor.execute(sql2)
            results = cursor.fetchall()
            for x in results:
                input = str(x)
                self.table.addItem(input)
        else:
            self.table.addItem("No results")
        conn.close()


class update_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("update data")
        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 600, 600)
        self.label.setText("test")


class add_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("add data")
        self.title = QLabel(self)
        self.game_title = QLineEdit(self)
        self.game_region = QLineEdit(self)
        self.series_title = QLineEdit(self)
        self.release_year = QLineEdit(self)
        self.operating_system = QLineEdit(self)
        self.finalize = QPushButton(self)
        self.systemType1 = QRadioButton(self)
        self.systemType2 = QRadioButton(self)
        self.patch = QLineEdit(self)
        self.numID = QLineEdit(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 437, 454)
        self.title.setText("Add a Game")
        self.title.move(160, 10)
        self.title.resize(111, 61)

        self.numID.resize(113, 20)
        self.numID.move(330, 130)
        self.numID.setPlaceholderText("numID (Console Only)")

        self.systemType1.resize(82, 17)
        self.systemType2.resize(82, 17)
        self.systemType1.move(160, 100)
        self.systemType2.move(250, 100)
        self.systemType1.setText("PC")
        self.systemType2.setText("Console")

        self.game_title.move(10, 100)
        self.game_title.resize(121, 21)
        self.game_title.setPlaceholderText("Game Title")

        self.game_region.move(10, 160)
        self.game_region.resize(121, 21)
        self.game_region.setPlaceholderText("Game Region")

        self.series_title.move(10, 130)
        self.series_title.resize(121, 21)
        self.series_title.setPlaceholderText("Series Title")

        self.release_year.move(10, 190)
        self.release_year.resize(121, 21)
        self.release_year.setPlaceholderText("Release Year")

        self.operating_system.move(10, 220)
        self.operating_system.resize(121, 21)
        self.operating_system.setPlaceholderText("OS / Console")

        self.patch.move(330, 100)
        self.patch.resize(113, 20)
        self.patch.setPlaceholderText("Patch (console only)")

        self.finalize.resize(75, 23)
        self.finalize.move(170, 320)
        self.finalize.setText("Submit")
        self.finalize.clicked.connect(self.add_video_game)

    def add_video_game(self):
        conn = sql.connect("game_database.sqlite3")
        cursor = conn.cursor()

        pc = self.systemType1.isChecked()
        console = self.systemType2.isChecked()
        game_title = self.game_title.text()
        series_title = self.series_title.text()
        game_region = self.game_region.text()
        release_year = self.release_year.text()
        operating_system = self.operating_system.text()
        patch = self.patch.text()
        numID = self.numID.text()

        if pc:
            cursor.execute("SELECT count(*) FROM OS WHERE osName is (?) ", (operating_system,))
            exists = cursor.fetchone()
            if exists[0] == 0:
                cursor.execute("""SELECT max(osID) FROM OS """)
                osID = cursor.fetchone()
                osID = osID[0]
                osID = osID + 1
                cursor.execute("""INSERT INTO OS (osID,osName) VALUES (?,?) """, (osID, operating_system,))
                conn.commit()
            else:
                cursor.execute("""SELECT osID FROM OS WHERE osName is (?)""", (operating_system,))
                osID = cursor.fetchone()
                osID = osID[0]

        if console:
            cursor.execute("""SELECT count(*) FROM System WHERE systemName = (?) """, (operating_system,))
            exists = cursor.fetchone()
            if exists[0] == 0:
                cursor.execute("""SELECT max(systemID) FROM System """)
                systemID = cursor.fetchone()
                systemID = systemID[0]
                systemID = systemID + 1
                cursor.execute("""INSERT INTO System (systemID,systemName) VALUES (?,?) """,
                               (systemID, operating_system,))
                conn.commit()
            else:
                cursor.execute("""SELECT systemID FROM System WHERE systemName is (?)""", (operating_system,))
                systemID = cursor.fetchone()
                systemID = systemID[0]

        cursor.execute("""SELECT count(*) FROM Region WHERE regionName=(?)""", (game_region,))
        exists = cursor.fetchone()
        if exists[0] == 0:
            cursor.execute("""SELECT max(regionID) FROM Region""")
            rID = cursor.fetchone()
            rID = rID[0]
            rID = rID + 1
            cursor.execute("""INSERT INTO Region (regionID, regionName) VALUES(?,?) """, (rID, game_region,))
            conn.commit()
        else:
            cursor.execute("""SELECT regionID FROM Region WHERE regionName is (?)""", (game_region,))
            rID = cursor.fetchone()
            rID = rID[0]

        cursor.execute("""SELECT count(*) FROM Series WHERE SeriesName=(?)""", (series_title,))
        exists = cursor.fetchone()
        if exists[0] == 0:
            cursor.execute("""SELECT max(seriesID) FROM Series""")
            sID = cursor.fetchone()
            sID = sID[0]
            sID = sID + 1
            cursor.execute("""INSERT INTO Series (SeriesID, seriesName) VALUES(?,?) """, (sID, series_title,))
            conn.commit()
        else:
            cursor.execute("""SELECT seriesID FROM Series WHERE seriesName is (?)""", (series_title,))
            sID = cursor.fetchone()
            sID = sID[0]
        if pc:
            cursor.execute("""SELECT count(title) FROM PC WHERE title is (?)""", (game_title,))
            exists = cursor.fetchone()
            if exists[0] == 0:
                cursor.execute("""INSERT INTO PC (title,regionID,seriesID,year,osID) VALUES(?,?,?,?,?)""",
                               (game_title, rID, sID, release_year, osID,))
                conn.commit()
                msg = QMessageBox()
                msg.setText("successfully added data")
                msg.exec_()
                add_window.close(self)
            else:
                msg = QMessageBox()
                msg.setText("game already exists")
                msg.exec_()
        if console:
            cursor.execute("""SELECT count(title) FROM Console WHERE title is (?)""", (game_title,))
            print(1)
            exists = cursor.fetchone()
            if exists[0] == 0:
                cursor.execute("""INSERT INTO Console (title,regionID,seriesID,systemID,numID,patch) VALUES(?,?,?,?,
                                ?,?)""",
                               (game_title, rID, sID, systemID, numID, patch))
                conn.commit()
                msg = QMessageBox()
                msg.setText("successfully added data")
                msg.exec_()
                add_window.close(self)
            else:
                msg = QMessageBox()
                msg.setText("game already exists")
                msg.exec_()
        conn.close()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = QLabel(self)
        self.add_button = QPushButton(self)
        self.search_button = QPushButton(self)
        self.update_button = QPushButton(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Game Database")
        self.setGeometry(200, 200, 362, 397)

        self.title.setText("Database Menu")
        self.title.move(140, 0)
        self.title.resize(131, 101)

        self.add_button.resize(111, 61)
        self.add_button.move(120, 90)
        self.add_button.setText("add")
        self.add_button.clicked.connect(self.build_add)

        self.search_button.resize(111, 61)
        self.search_button.move(120, 160)
        self.search_button.setText("search")
        self.search_button.clicked.connect(self.build_search)

        self.update_button.resize(111, 61)
        self.update_button.move(120, 230)
        self.update_button.setText("update")
        self.update_button.clicked.connect(self.build_update)

    def build_add(self):
        conn = sql.connect("game_database.db")
        curs = conn.cursor()
        self.add_window = add_window()
        self.add_window.show()

    def build_search(self):
        conn = sql.connect("game_database.db")
        curs = conn.cursor()
        self.search_window = search_window()
        self.search_window.show()

    def build_update(self):
        conn = sql.connect("game_database.db")
        curs = conn.cursor()
        self.update_window = update_window()
        self.update_window.show()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


main()
