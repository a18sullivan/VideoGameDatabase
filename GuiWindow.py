import sqlite3 as sql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QRadioButton, QMessageBox, \
    QListWidget, QCheckBox


class search_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Database")
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
        self.label.resize(100, 61)
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
            sql2 = ("""SELECT title, regionName, seriesName, systemName, numID, patch From Console 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN System USING (systemID) 
                        WHERE Console.title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results = cursor.fetchall()
            for x in results:
                input=str(x)
                self.table.addItem(input)
            sql2 = (f"""SELECT title, regionName, seriesName, PC.year, osName From PC 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN OS USING (osID) 
                        WHERE title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results2=cursor.fetchall()
            for x in results2:
                input=str(x)
                self.table.addItem(input)
        elif pc:
            sql2 = (f"""SELECT title, regionName, seriesName, PC.year, osName From PC 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN OS USING (osID) 
                        WHERE title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results = cursor.fetchall()
            for x in results:
                input=str(x)
                self.table.addItem(input)
        elif console:
            sql2 = ("""SELECT title, regionName, seriesName, systemName, numID, patch From Console 
                                    JOIN Region USING (regionID)
                                    JOIN Series USING (seriesID)
                                    JOIN System USING (systemID) 
                                    WHERE Console.title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
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
        self.setWindowTitle("Update Data")
        self.title = QLabel(self)
        self.game_title = QLineEdit(self)
        self.game_region = QLineEdit(self)
        #self.game_region.setValidator(QIntValidator())
        self.series_title = QLineEdit(self)
        #self.series_title.setValidator(QIntValidator())
        self.release_year = QLineEdit(self)
        self.release_year.setValidator(QIntValidator())
        self.operating_system = QLineEdit(self)
        #self.operating_system.setValidator(QIntValidator())
        self.search_button = QPushButton(self)
        self.patch = QLineEdit(self)
        self.numID = QLineEdit(self)

        self.search_bar = QLineEdit(self)
        self.finalize = QPushButton(self)
        self.table = QListWidget(self)
        self.pc = QCheckBox(self)
        self.console = QCheckBox(self)

        self.where = None
        self.game_type = None

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 432, 600)
        self.title.setText("Update a Game")
        self.title.move(160, 10)
        self.title.resize(111, 61)

        #Using search to find possible games to update
        self.search_bar.resize(113, 20)
        self.search_bar.move(10, 80)
        self.search_bar.setPlaceholderText("Enter Game Title")

        self.search_button.move(140, 80)
        self.search_button.resize(75, 23)
        self.search_button.setText("search")
        self.search_button.clicked.connect(self.search)

        self.console.move(320, 50)
        self.console.resize(70, 17)
        self.console.setText("Console")

        self.pc.move(320, 70)
        self.pc.resize(70, 17)
        self.pc.setText("PC")

        self.table.resize(411, 301)
        self.table.move(10, 110)
        self.table.itemClicked.connect(self.on_select)

        #Update fields
        self.numID.move(10, 530)
        self.numID.resize(121, 21)
        self.numID.setPlaceholderText("numID")
        self.numID.hide()

        self.game_title.move(10, 430)
        self.game_title.resize(411, 21)
        self.game_title.setPlaceholderText("Game Title")

        self.game_region.move(10, 480)
        self.game_region.resize(121, 21)
        self.game_region.setPlaceholderText("Game Region")

        self.series_title.move(150, 480)
        self.series_title.resize(121, 21)
        self.series_title.setPlaceholderText("Series Title")

        self.operating_system.move(290, 480)
        self.operating_system.resize(121, 21)
        self.operating_system.setPlaceholderText("OS / Console")

        self.release_year.move(10, 530)
        self.release_year.resize(121, 21)
        self.release_year.setPlaceholderText("Release Year")

        self.patch.move(150, 530)
        self.patch.resize(113, 20)
        self.patch.setPlaceholderText("Patch")
        self.patch.hide()

        self.finalize.move(330, 530)
        self.finalize.resize(75, 23)
        self.finalize.setText("Submit")
        self.finalize.clicked.connect(self.update_video_game)
    def clear_select(self): #clears off selections so that you can't accidentally update non-visibly selected data
        self.game_type = None
        self.where = None

        self.game_title.setText("")
        self.game_region.setText("")
        self.series_title.setText("")
        self.operating_system.setText("")
        self.release_year.setText("")
        self.numID.setText("")
        self.patch.setText("")
    def on_select(self, item):
        conn = sql.connect("game_database.sqlite3")
        cursor = conn.cursor()
        selected = item.text()
        selected = selected.strip("()")
        selected = selected.replace("'", "")
        selected = selected.split(",")
        for i in range(len(selected)):  #sanitizing a bit
            selected[i] = selected[i].strip(" ")
        print(selected)
        self.where = (selected[0], selected[3], selected[4])

        if len(selected) == 6: #detecting and swapping between Console and PC entries
            sql2 = ("""SELECT * From Console
                                            JOIN Region USING (regionID)
                                            JOIN Series USING (seriesID)
                                            JOIN System USING (systemID)
                                            WHERE Console.title = ? AND systemName = ? AND numID = ?""")
            cursor.execute(sql2, self.where)
            results = cursor.fetchall()
            self.where = (results[0][0], results[0][3], results[0][4])
            self.game_type = True #Console flag
            self.numID.show()
            self.patch.show()
            self.release_year.hide()
            self.operating_system.setPlaceholderText("Console")
            #setting boxes with existing data
            self.game_title.setText(selected[0])
            self.game_region.setText(selected[1])
            self.series_title.setText(selected[2])
            self.operating_system.setText(selected[3])
            self.numID.setText(selected[4])
            self.patch.setText(selected[5])
        elif len(selected) == 5:
            sql2 = ("""SELECT * From PC
                                                        JOIN Region USING (regionID)
                                                        JOIN Series USING (seriesID)
                                                        JOIN OS USING (osID)
                                                        WHERE PC.title = ? AND PC.year = ? AND osName = ?""")
            cursor.execute(sql2, self.where)
            results = cursor.fetchall()
            self.where = (results[0][0], results[0][3], results[0][4])
            self.game_type = False #PC flag
            self.numID.hide()
            self.patch.hide()
            self.release_year.show()
            self.operating_system.setPlaceholderText("OS")
            #setting boxes with existing data
            self.game_title.setText(selected[0])
            self.game_region.setText(selected[1])
            self.series_title.setText(selected[2])
            self.operating_system.setText(selected[4])
            self.release_year.setText(selected[3])
        else:
            self.clear_select()
    def search(self):
        self.table.clear()
        conn = sql.connect("game_database.sqlite3")
        cursor = conn.cursor()

        query = self.search_bar.text()
        pc = self.pc.isChecked()
        console = self.console.isChecked()

        if pc == True and console == True:
            #sql2 = (f"""SELECT * From Console WHERE Console.title LIKE '%' || ? || '%'""")
            sql2 = ("""SELECT title, regionName, seriesName, systemName, numID, patch From Console 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN System USING (systemID) 
                        WHERE Console.title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results = cursor.fetchall()
            for x in results:
                input = str(x)
                self.table.addItem(input)
            #sql2 = (f"""SELECT * From PC WHERE title LIKE '%' || ? || '%'""")
            sql2 = (f"""SELECT title, regionName, seriesName, PC.year, osName From PC 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN OS USING (osID) 
                        WHERE title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results2 = cursor.fetchall()
            for x in results2:
                input = str(x)
                self.table.addItem(input)
        elif pc:
            #sql2 = (f"""SELECT * From PC WHERE title LIKE '%' || ? || '%'""")
            sql2 = (f"""SELECT title, regionName, seriesName, PC.year, osName From PC 
                        JOIN Region USING (regionID)
                        JOIN Series USING (seriesID)
                        JOIN OS USING (osID) 
                        WHERE title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results = cursor.fetchall()
            for x in results:
                input = str(x)
                self.table.addItem(input)
        elif console:
            #sql2 = (f"""SELECT * From Console WHERE Console.title LIKE '%' || ? || '%'""")
            sql2 = ("""SELECT title, regionName, seriesName, systemName, numID, patch From Console 
                       JOIN Region USING (regionID)
                       JOIN Series USING (seriesID)
                       JOIN System USING (systemID) 
                       WHERE Console.title LIKE '%' || ? || '%'""")
            cursor.execute(sql2, (query,))
            results = cursor.fetchall()
            for x in results:
                input = str(x)
                self.table.addItem(input)
        else:
            self.table.addItem("No results")
        conn.close()
        self.clear_select()


    def update_video_game(self):
        conn = sql.connect("game_database.sqlite3")
        cursor = conn.cursor()
        series = self.series_title.text()   #creating NULLs in proper places
        cursor.execute("""SELECT * FROM Series WHERE seriesName = ?""", (self.series_title.text(),))
        series = cursor.fetchone()
        cursor.execute("""SELECT * FROM Region WHERE regionName = ?""", (self.game_region.text(),))
        regionID = cursor.fetchone()
        if self.game_type == None:
            msg = QMessageBox()
            msg.setText("Error - no game selected")
            msg.exec_()
        elif series == None:
            msg = QMessageBox()
            msg.setText("Error - series not present")
            msg.exec_()
        elif regionID == None:
            msg = QMessageBox()
            msg.setText("Error - region not present")
            msg.exec_()
        elif self.game_type:    #Console Update
            if series == "":
                series = None
            else:
                series = series[0]
            regionID = regionID[0]
            patch = self.patch.text()   #creating NULLs in proper places
            if patch == "":
                patch = None
            cursor.execute("""SELECT * FROM System WHERE systemName = ?""", (self.operating_system.text(),))
            systemID = cursor.fetchone()
            if systemID != None:
                try:
                    query = ("""UPDATE Console SET
                    title = ?, regionID = ?, seriesID = ?, systemID = ?, numID = ?, patch = ?
                    WHERE title = ? AND systemID = ? AND numID = ?""")
                    cursor.execute(query, (self.game_title.text(), regionID, series,
                             systemID[0], self.numID.text(), patch,
                             self.where[0], self.where[1], self.where[2]))
                    conn.commit()
                    msg = QMessageBox()
                    msg.setText("Game updated successfully")
                    msg.exec_()
                except Exception as e:
                    msg = QMessageBox()
                    msg.setText("Error - Game already in Database")
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setText("Error - system not present")
                msg.exec_()
        else:   #PC Update
            if series == "":
                series = None
            else:
                series = series[0]
            regionID = regionID[0]
            #cursor.execute("""SELECT EXISTS(SELECT 1 FROM OS WHERE osID = ?)""", (self.operating_system.text(),))
            cursor.execute("""SELECT * FROM OS WHERE osName = ?""", (self.operating_system.text(),))
            osID = cursor.fetchone()
            if osID != None:
                try:
                    query = ("""UPDATE PC SET
                                title = ?, regionID = ?, seriesID = ?, year = ?, osID = ?
                                WHERE title = ? AND year = ? AND osID = ?""")
                    cursor.execute(query, (self.game_title.text(), regionID, series,
                             self.release_year.text(), osID[0],
                             self.where[0], self.where[1], self.where[2]))
                    conn.commit()
                    msg = QMessageBox()
                    msg.setText("Game updated successfully")
                    msg.exec_()
                except Exception as e:
                    msg = QMessageBox()
                    msg.setText("Error - Game already in Database")
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setText("Error - OS not present")
                msg.exec_()
        conn.close()



class add_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("add data")
        self.title = QLabel(self)
        self.game_title = QLineEdit(self)
        self.game_region = QLineEdit(self)
        self.series_title = QLineEdit(self)
        self.release_year = QLineEdit(self)
        self.release_year.setValidator(QIntValidator())
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
        series_title = self.series_title.text()  # creating NULLs in proper places
        if series_title == "":
            series_title = None
        game_region = self.game_region.text()
        release_year = self.release_year.text()
        operating_system = self.operating_system.text()
        patch = self.patch.text()   # creating NULLs in proper places
        if patch == "":
            patch = None
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
            cursor.execute("""SELECT count(title) FROM Console WHERE title is ? AND numID is ?""", (game_title, numID))
            cursor.execute("""SELECT count(title) FROM PC WHERE title is ? AND PC.year is ? AND osID is ?""", (game_title, release_year, operating_system))
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
            cursor.execute("""SELECT count(title) FROM Console WHERE title is ? AND numID is ?""", (game_title, numID))
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
