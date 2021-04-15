

#  This is still work in progress...   MySQL will keep working while SQLite works

#  June 6 2018


import sqlite3


class DBManager_sqlite:
    def __init__(self):
        """Attributes"""
        self.GUIDB = 'my_database.db'      #database name...name as you wish
        self.connect_db()
        self.create_db()
        self.words = ["Select an account"]
                
    def connect_db(self):
        """Connecting to SQLite"""

        con_bd = sqlite3.connect(self.GUIDB)
             
        #creating the cursor to send commands to SQLite
        cursor = con_bd.cursor()

        #we return the connection and the cursor.
        return con_bd, cursor

    def close(self, cursor, con_bd):
        """To close the SQLite connection and cursor"""
        cursor.close()
        con_bd.close()
        
    def create_db(self):
        """Connecting and creating the SQLite db"""
        #connect and create Data Base!!!
        con_bd = sqlite3.connect(self.GUIDB)
                
        #creating the cursor to send commands to SQLite
        cursor = con_bd.cursor()

        # Creating the tables
        cursor.execute("CREATE TABLE IF NOT EXISTS Passwords        \
            (Pass_ID INTEGER PRIMARY KEY AUTOINCREMENT,   \
            Title_account TEXT,       \
            User_account TEXT,     \
            Password TEXT,        \
            Web_site TEXT)")        
        
        # Create child Table for Notes
        cursor.execute("CREATE TABLE IF NOT EXISTS Notes     \
            (notes_id INTEGER PRIMARY KEY AUTOINCREMENT, \
            Passwords_Notes_ID INTEGER,        \
            Notes TEXT,                 \
            FOREIGN KEY (Passwords_Notes_ID)      \
                REFERENCES Passwords(Pass_ID)   \
                ON DELETE CASCADE               \
            )")

        
    def show_Title_account(self):
        """To show information on the Scrolledtext.
        The information to display is added to a list."""
        con_db, cursor = self.connect_db()
         
        self.words = ["Select an account"]

        # execute command
        cursor.execute("SELECT Title_account FROM passwords")
        
        #create a var to name each item in the fetchall()
        list_titles = cursor.fetchall()
        
        #add each word to a list:
        for row in list_titles:
            self.words.append(row[0])
        
        # close cursor and connection
        self.close(cursor, con_db) 
       
    def extract_db_info(self, title_value):
        """Extract info from SQLite DB.  Passing the selection on the combobox as parameter
        It then cleans the data y adds it to a list"""
        
        con_db, cursor = self.connect_db()

        all_results = [] # To store values from DB.

        # passwords_db_values = ['title_account', 'user_account', 'password', 'web_site']

        # for value in passwords_db_values:        IMPROVE THIS CODE.   
        #     cursor.execute("SELECT (?) FROM passwords WHERE TITLE_ACCOUNT = (?);", [value, title_value])
        #     value_result = cursor.fetchall()
        #     all_results.append(value_result)

        cursor.execute("SELECT Title_account FROM passwords WHERE TITLE_ACCOUNT = (?)", [title_value])
        result_title = cursor.fetchall()
        all_results.append(result_title)

        cursor.execute("SELECT user_account FROM passwords WHERE TITLE_ACCOUNT = (?)", [title_value])
        result_user = cursor.fetchall()
        all_results.append(result_user)

        cursor.execute("SELECT password FROM passwords WHERE TITLE_ACCOUNT = (?)", [title_value])
        result_password = cursor.fetchall()
        all_results.append(result_password)

        cursor.execute("SELECT web_site FROM passwords WHERE TITLE_ACCOUNT = (?)", [title_value])
        result_web_site = cursor.fetchall()
        all_results.append(result_web_site)

        #To obtain the corresponding value for the notes chart:
        cursor.execute("SELECT pass_id FROM passwords WHERE TITLE_ACCOUNT = (?)", [title_value])
        pass_id_number = cursor.fetchall()[0][0]
        
        cursor.execute("SELECT notes FROM notes WHERE  passwords_notes_id = (?)", [pass_id_number])
        note_result = cursor.fetchall()
        all_results.append(note_result)

        all_results_clean = [] # All results after cleaning.

        for item in all_results:
            item_clean = item[0][0]
            all_results_clean.append(item_clean)
        
        self.close(cursor, con_db)

        return all_results_clean
        
    def insert_data(self, title_account, user_account, password, web_site, note_text):
        """Takes info from the Add info GUI and inserts it into the SQLlite DB"""
        con_db, cursor = self.connect_db()
        
        # insert data
        cursor.execute("INSERT INTO passwords (Title_account, User_account, Password, Web_site) \
            VALUES (?, ?, ?, ?)", (title_account, user_account, password, web_site))
            
        # last inserted auto increment value   
        keyID = cursor.lastrowid 
        print(keyID)
                
        cursor.execute("INSERT INTO notes (Passwords_Notes_ID, Notes) \
            VALUES (?, ?)", (keyID, note_text))               
        
        # commit transaction
        con_db.commit()

        # close cursor and connection
        self.close(cursor, con_db)

        self.show_Title_account()

    def update_data(self, title_value_edit, user_title_info_edit, user_info_edit,
	 				password_info_edit, website_info_edit, note_info_edit):
        """Takes info from the Update GUI and updates it into the SQLite db"""
        
        con_db, cursor = self.connect_db()
        
        # Get pass_id:
        cursor.execute("SELECT pass_id FROM passwords WHERE title_account = (?);", [title_value_edit])
        result_pass_id = cursor.fetchall()[0][0]
     
        # Update TITLE_ACCOUNT
        cursor.execute("UPDATE passwords SET title_account = (?) WHERE pass_id = (?);",  
                        (user_title_info_edit, result_pass_id))
       
        # Update USER_ACCOUNT
        cursor.execute("UPDATE passwords SET user_account = (?) WHERE pass_id = (?);",  
                        (user_info_edit, result_pass_id))

        # Update PASSWORD
        cursor.execute("UPDATE passwords SET password = (?) WHERE pass_id = (?);",  
                        (password_info_edit, result_pass_id))

        # Update WEB_SITE
        cursor.execute("UPDATE passwords SET web_site = (?) WHERE pass_id = (?);",  
                        (website_info_edit, result_pass_id))

        # Update NOTES
        cursor.execute("UPDATE notes SET notes = (?) WHERE notes_id = (?);",  
                        (note_info_edit, result_pass_id))
        
        con_db.commit()

        self.close(cursor, con_db)

        self.show_Title_account() #Updates changes into the GUI

    def delete_data(self, title_value_delete):
        """Deletes a row of information from the SQLite db"""
        con_db, cursor = self.connect_db()

        # Obtain PASS_ID
        cursor.execute("SELECT pass_id FROM passwords WHERE title_account = (?);", [title_value_delete])
        result_pass_id = cursor.fetchall()[0][0]
        # Delete records on PASS_ID
        cursor.execute("DELETE from passwords WHERE pass_id = (?);", [result_pass_id])
        
        con_db.commit()

        self.show_Title_account()

        self.close(cursor, con_db)

    def drop_db(self):
        """Eliminates completely the DB.  Use with caution!"""
        con_db, cursor = self.connect_db()
                
        cursor.execute("DROP DATABASE ()", (self.GUIDB))
        
        self.close(cursor, con_db)