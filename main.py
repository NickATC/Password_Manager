version = "Version 1.3"

######################
#####   TO FIX   #####
# 1.  Once the Passsword Generator is closed, it won't open again.  Partially solved.  All code in one file?

# 2.  User guide?  Tool tips?
# 
# 3.  Update SQLite to fully work. 
		#  Delete the whole DB!!  Add the code to the menu option!

# 4. Create the Hashing function to add some security
# 5. Implement the encription to protect passwords and the info in general!
# 6. Impromve the toogle show/hide pass on the password Generator window
          
######################
#####   BUG   #####
#  When deleting a record, SQLite is not cascading.  There are orphan records on Notes table
######################

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import scrolledtext
from tkinter import messagebox as msg 
from pass_manager_slqlite import DBManager_sqlite  
import random
import pyperclip
import webbrowser


##################
###### MAIN GUI  ######

window = tk.Tk()
window.title("Password Manager   " + version)
window.geometry("800x600")
window.resizable(False, False)
window.wm_iconbitmap("icons/pass_man.ico")

db_manager_sqlite = DBManager_sqlite()   #  Instance of Data Base!  Using SQLite
 
def open_pass_gen():                             ########  fix this error. SEE ERROR 1 above  #######
	"""Opens the Password Generator program"""
	
	#Chars, numbers & symbols to use
	LETTERS = ('abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ')
	NUMBERS = ('0123456789')
	SYMBOLS = ('@-!#$%+*~&¿?;:/=')     #Are they all accepted?  

	def show_tips():
		"""Function to show the tips on a PDF file"""
		import os
		os.startfile('docs/tips.pdf')
				
	def _msgBox(title = "Invalid entry!", message = "Enter a valid number between 8 and 500"):
		"""Function to show different errors and messageBox"""
		msg.showwarning(title, message)

	def _open_PassGen_Guide():
		"""Function to show the user guide on a PDF file"""
		import os
		os.startfile('PassGen_guide.pdf')

	def _copyClipboard():
		"""Function to copy the password to the clipboard"""
		pyperclip.copy(scr_pass.get(1.0,"end"))

	def generate_password():
		"""Function to analize user entries and generate the password"""
		scr_pass.delete(1.0,"end")
		password = []
		values_for_password = []
		
		try:
			if int(password_length.get()) < 8:
				_msgBox()
				
			elif int(password_length.get()) > 5000:
				_msgBox(message = "Sorry, Can't generate a password this long!")
				
			else:
				#Dictionary to check and store user values.
				variable_values = {'chVarLetters' : chVarLetters.get(),
								'chVarNumbers' : chVarNumbers.get(),
								'chVarSymbols' : chVarSymbols.get()
								}
			
				#To check the user preferences.  If checked, it'll be added to list values_for_password.	
				for key, value in variable_values.items():
					if value == 1:
						values_for_password.append(key)
					else:
						continue
		
				if not values_for_password:
					_msgBox(title = "Error!", message = "At least one option must be checked!")

				else:
					#Dictionary to match the variable name from the buttons and the varibale value (LETTERS, NUMBERS or SYMBOLS)
					equivalent_values = { 'chVarLetters' : LETTERS,
											'chVarNumbers' : NUMBERS,
											'chVarSymbols' : SYMBOLS
										}
					
					if len(values_for_password) == 3:
						for i in range(round(int(password_length.get()) / 3)):
							item = values_for_password[0]
							character = random.choice(equivalent_values[item])
							password.append(character)

						for i in range(round(int(password_length.get()) / 3)):
							item = values_for_password[1]
							character = random.choice(equivalent_values[item])
							password.append(character)
									
						while len(password) < int(password_length.get()):
							item = values_for_password[2]
							character = random.choice(equivalent_values[item])
							password.append(character)
						
					elif len(values_for_password) == 2:
						for i in range(round(int(password_length.get()) / 2)):
							item = values_for_password[0]
							character = random.choice(equivalent_values[item])
							password.append(character)
						
						while len(password) < int(password_length.get()):
							item = values_for_password[1]
							character = random.choice(equivalent_values[item])
							password.append(character)
					
					else:
						for key, value in equivalent_values.items():
							if key in values_for_password:
								while len(password) < int(password_length.get()):
									character = random.choice(value)
									password.append(character)
							else:
								continue
																		
		except ValueError:
			_msgBox()
		
		random.shuffle(password) 				# shuffle password.
		password = "".join(password) 			# Turn password into a string
		scr_pass.insert(tk.INSERT, password) 	# Insert the password into the scrolledtext.
		

	####################################################
	####### Creating the GUI for the password_generator
	####################################################			

	gen_window = tk.Toplevel()
	gen_window.title("Password Generator")
	gen_window.geometry("450x640")
	gen_window.resizable(False, False)
	gen_window.wm_iconbitmap("icons/lock.ico")


	pass_gen_header = tk.PhotoImage(file = 'icons/pass_gen_header.gif')
	pass_gen_header_gif = tk.Label(gen_window, image = pass_gen_header)
	pass_gen_header_gif.grid(column = 0, row = 0)


	#############################################################
	#######      Creating the Widgets for Password Generator
	#############################################

	advice_button = ttk.Button(gen_window, text = "Password Tips", command = show_tips)
	advice_button.grid(column = 0, row = 1, pady = 10)

	guide_button = ttk.Button(gen_window, text = "User guide", command = _open_PassGen_Guide)
	guide_button.grid(column = 0, row = 2, pady = 5)

	label_frame1 = ttk.LabelFrame(gen_window, text = "Your Password Generator Options:")
	label_frame1.grid(column = 0, row = 3, padx = 15, pady = 5)

	label_1 = ttk.Label(label_frame1, text = "Enter the number of characters (between 8 and 500) for your new password :")
	label_1.grid(column = 0, row = 0, pady = 20, padx = 5)

	password_length = tk.StringVar()
	password_length.set("20")   # I set an initial value!!
	entry_1 = ttk.Entry(label_frame1, width = "10", textvariable = password_length)
	entry_1.grid(column = 0, row = 1, padx = 20, pady = 5)
	entry_1.focus()

	chVarLetters = tk.IntVar()
	check_1 = tk.Checkbutton(label_frame1, text = "Password has letters?", variable = chVarLetters,
							state = 'active')
	check_1.select()
	check_1.grid(column = 0, row = 2, sticky = 'W')

	chVarNumbers = tk.IntVar()
	check_1 = tk.Checkbutton(label_frame1, text = "Password has numbers?", variable = chVarNumbers,
							state = 'active')
	check_1.select()
	check_1.grid(column = 0, row = 3, sticky = 'W')

	chVarSymbols = tk.IntVar()
	check_1 = tk.Checkbutton(label_frame1, text = "Password has symbols?", variable = chVarSymbols,
							state = 'active')
	check_1.select()
	check_1.grid(column = 0, row = 4, sticky = 'W')


	button_1 = ttk.Button(label_frame1, text = "Generate Password!", command = generate_password)
	button_1.grid(column = 0, row = 5, columnspan = 2, pady = 20)

	label_frame2 = ttk.LabelFrame(gen_window, text = "Your new password")
	label_frame2.grid(column = 0, row = 4, padx = 20, pady = 5)

	label_2 = ttk.Label(label_frame2, text = "Edit your new password if needed.  Try to keep as generated.")
	label_2.grid(column = 0, row = 0, pady = 10)

	scr_pass = scrolledtext.ScrolledText(label_frame2, width = 42, height = 5, wrap = tk.WORD)
	scr_pass.grid(column = 0, row = 1, columnspan = 3, padx = 12, pady = 10)

	button_2 = ttk.Button(label_frame2, text = "Generate Another Password!", command = generate_password)
	button_2.grid(column = 0, row = 2, pady = 15, sticky = "W")

	button_3 = ttk.Button(label_frame2, text = "Copy to Clipboard", command = _copyClipboard)
	button_3.grid(column = 0, row = 2, sticky = "E")

	gen_window.mainloop()

#ADD NEW ENTRY window
def new_entry():
	new_entry_window = tk.Toplevel()
	new_entry_window.title("New Entry")
	new_entry_window.geometry("550x550")
	new_entry_window.resizable(False, False)
	new_entry_window.wm_iconbitmap("icons/pass_man.ico")

	new_entry_header = tk.PhotoImage(file = 'icons/new_entry_header.gif')
	new_entry_header_gif = tk.Label(new_entry_window, image = new_entry_header)
	new_entry_header_gif.grid(column = 0, row = 0)

	labelFrame = ttk.Labelframe(new_entry_window, text = "Enter the information for your new entry :  ")
	labelFrame.grid(column = 0, row = 1, padx = 30, pady = 20, sticky = "N")

	#Spaces to enter the new password information:
	#Title of account:
	titleAccount_label = ttk.Label(labelFrame, text = "Title of Account:")
	titleAccount_label.grid(column = 0, row = 2, padx = 15, pady = 10)
	
	title_account = tk.StringVar()
	titleAccount_entry = ttk.Entry(labelFrame, width = 25, textvariable = title_account)
	titleAccount_entry.grid(column = 1, row = 2, padx = 15, pady = 10)

	#User account:
	userAccount_label = ttk.Label(labelFrame, text = "User Account:")
	userAccount_label.grid(column = 0, row = 3, padx = 10, pady = 10)

	user_account = tk.StringVar()
	userAccount_entry = ttk.Entry(labelFrame, width = 25, textvariable = user_account)
	userAccount_entry.grid(column = 1, row = 3, padx = 10, pady = 10)

	#Password:
	password_label = ttk.Label(labelFrame, text = "Enter your password:")
	password_label.grid(column = 0, row = 4, padx = 10, pady = 10)

	password = tk.StringVar()
	password_entry = ttk.Entry(labelFrame, width = 25, textvariable = password, show = "*" )
	password_entry.grid(column = 1, row = 4, padx = 10, pady = 10)

	def toogle_show_pass(event):
		"""To toogle show password on NEW ENTRY window"""
		global show
		show = True
		show_hide_pass.config(text = password.get())

	def toogle_hide_pass(event):
		"""To toogle hide password on NEW ENTRY window"""
		global show
		show = False
		show_hide_pass.config(text = " ")
		
	password_hide = ttk.Button(labelFrame, text = "Show/Hide:")
	password_hide.grid(column = 2, row = 4, padx = 5, pady = 5)

	password_hide.bind('<ButtonPress-1>', toogle_show_pass)
	password_hide.bind('<ButtonRelease-1>', toogle_hide_pass)

	password_gen = ttk.Button(labelFrame, text = "Open \nPassword \nGenerator", command = open_pass_gen)
	password_gen.grid(column = 3, row = 4, columnspan = 2)

	show_hide_pass = ttk.Label(labelFrame, text = " ", width = 60)
	show_hide_pass.grid(column = 0, row = 5, columnspan = 4)

	#Web Site
	website_label = ttk.Label(labelFrame, text = "Enter the website:")
	website_label.grid(column = 0, row =6, padx = 10, pady = 10)

	web_site = tk.StringVar()
	website_entry = ttk.Entry(labelFrame, width = 25, textvariable = web_site)
	website_entry.grid(column = 1, row = 6, padx = 10, pady = 10)

	#Notes
	note_label = ttk.Label(labelFrame, text = "Notes:")
	note_label.grid(column = 0, row =7, padx = 10, pady = 10)

	#notes = tk.StringVar()
	note_text = scrolledtext.ScrolledText(labelFrame, width = 19, height = 3, wrap = tk.WORD)
	note_text.grid(column = 1, row = 7, columnspan = 2, padx = 10, pady = 10, sticky = "W")

	def __confirm_save():
		reply = msg.askyesnocancel("Confirmation", "Are you sure you want to save the information in Database?")
		print(reply)
		
		if reply == True:
			
			#Commit changes to DB
			title_account1 = title_account.get()
			user_account1 = user_account.get()
			password1 = password.get()
			web_site1 = web_site.get()
			note_text1 = note_text.get(1.0,"end")
			
			# Save on SQLite DB!
			db_manager_sqlite.insert_data(title_account1, user_account1, password1, web_site1, note_text1)

			#open new window confirming user that the info was saved!
			msg.showinfo("", "Information saved!")
			entry_chosen.config(values = db_manager_sqlite.words)
				
			def _ok_quit():      # Function to close the new_entry window
				new_entry_window.quit()
				new_entry_window.destroy()
				
			_ok_quit()
		
	#Save button
	save_button = tk.Button(labelFrame, text = "SAVE INFORMATION", 
			height = 3, width = 20, foreground = "white", background = "red", command = __confirm_save)
	save_button.grid(column = 1, row = 8, padx = 10, pady = 20, columnspan = 2, sticky = "W")

	new_entry_window.mainloop()

def edit_entry():
	edit_entry_window = tk.Toplevel()
	edit_entry_window.title("Edit / Delete Entry")
	edit_entry_window.geometry("550x550")
	edit_entry_window.resizable(False, False)
	edit_entry_window.wm_iconbitmap("icons/pass_man.ico")

	edit_entry_header = tk.PhotoImage(file = 'icons/edit_entry_header.gif')
	edit_entry_header_gif = tk.Label(edit_entry_window, image = edit_entry_header)
	edit_entry_header_gif.grid(column = 0, row = 0)

	labelFrame_edit = ttk.Labelframe(edit_entry_window, text = "Select a user account to see password details :  ")
	labelFrame_edit.grid(column = 0, row = 1, padx = 30, pady = 20, sticky = "N")

	def __confirm_edit():
		reply = msg.askyesnocancel("Confirmation", "Are you sure you want to EDIT this entry?")
		print(reply)
		
		if reply == True:

			# Read values directly from GUI to read possible edits from user.
			user_title_info_edit = titleAccount_entry_edit.get()
			user_info_edit = userAccount_entry_edit.get()
			password_info_edit  = password_entry_edit.get()
			website_info_edit = website_entry_edit.get()
			note_info_edit = note_text_edit.get(1.0, 'end')

			#Commit changes to DB
			title_value_edit = entry_chosen_edit.get()
			db_manager_sqlite.update_data(title_value_edit, user_title_info_edit, user_info_edit,
							password_info_edit, website_info_edit, note_info_edit) 

			#open new window confirming user that the info was saved!
			msg.showinfo("", "Information edited successfully!")
			entry_chosen.config(values = db_manager_sqlite.words)
			
			edit_entry_window.quit()
			edit_entry_window.destroy()
			
	def __confirm_delete():
		reply = msg.askyesnocancel("Confirmation", "Are you sure you want to DELETE this entry?")
		print(reply)
		
		if reply == True:
			
			#Commit changes to DB
			title_value_delete = entry_chosen_edit.get()
			db_manager_sqlite.delete_data(title_value_delete)

			#open new window confirming user that the info was saved!
			msg.showinfo("", "Information deleted successfully!")
			entry_chosen.config(values = db_manager_sqlite.words)

			edit_entry_window.quit()
			edit_entry_window.destroy()

	def selection_changed_edit(self):
		
		# List of entries in GUI.  Delete info before injecting new info from DB
		list_entries_edit = [titleAccount_entry_edit, userAccount_entry_edit, 
							password_entry_edit, website_entry_edit, note_text_edit]
		
		for item in list_entries_edit:
			if item == note_text_edit:
				note_text_edit.delete(1.0,"end")		
			else:
				item.delete(0,"end")
		
		title_value_edit = entry_chosen_edit.get()

		all_results_clean = db_manager_sqlite.extract_db_info(title_value_edit)  # for SQLite DB
		
		#Assign values to list from DB
		user_title_info_edit = all_results_clean[0]
		user_info_edit = all_results_clean[1]
		password_info_edit  = all_results_clean[2]
		website_info_edit = all_results_clean[3]
		note_info_edit = all_results_clean[4]

		#change the values in the GUI.  Insert them into the ENTRY boxes
		titleAccount_entry_edit.insert(tk.INSERT, user_title_info_edit)
		userAccount_entry_edit.insert(tk.INSERT, user_info_edit)
		password_entry_edit.insert(tk.INSERT, password_info_edit)
		website_entry_edit.insert(tk.INSERT, website_info_edit)
		note_text_edit.insert(tk.INSERT, note_info_edit)

	password_entry = tk.StringVar()
	entry_chosen_edit = ttk.Combobox(labelFrame_edit, width = 40, textvariable = password_entry, state='readonly')
	entry_chosen_edit['values'] = db_manager_sqlite.words  # Shows titles from the DB
	entry_chosen_edit.grid(column=0, row=1,padx = 80, pady = 15, columnspan = 3)
	entry_chosen_edit.current(0)
	entry_chosen_edit.bind("<<ComboboxSelected>>", selection_changed_edit)
	

	#Spaces to enter the new password information to edit or delete:
	#Title of account:
	titleAccount_label_edit = ttk.Label(labelFrame_edit, text = "Title of Account:")
	titleAccount_label_edit.grid(column = 0, row = 2, padx = 15, pady = 10)
	
	title_account_edit = tk.StringVar()
	titleAccount_entry_edit = ttk.Entry(labelFrame_edit, width = 25, textvariable = title_account_edit)
	titleAccount_entry_edit.grid(column = 1, row = 2, padx = 15, pady = 10)

	#User account:
	userAccount_label_edit = ttk.Label(labelFrame_edit, text = "User Account:")
	userAccount_label_edit.grid(column = 0, row = 3, padx = 10, pady = 10)

	user_account_edit = tk.StringVar()
	userAccount_entry_edit = ttk.Entry(labelFrame_edit, width = 25, textvariable = user_account_edit)
	userAccount_entry_edit.grid(column = 1, row = 3, padx = 10, pady = 10)

	#Password:
	password_label_edit = ttk.Label(labelFrame_edit, text = "Enter your password:")
	password_label_edit.grid(column = 0, row = 4, padx = 10, pady = 10)

	password_edit = tk.StringVar()
	password_entry_edit = ttk.Entry(labelFrame_edit, width = 25, textvariable = password_edit, show = "*" )
	password_entry_edit.grid(column = 1, row = 4, padx = 10, pady = 10)

	password_hide = ttk.Button(labelFrame_edit, text = "Show/Hide")
	password_hide.grid(column = 2, row = 4, padx = 5, pady = 5)

	password_gen = ttk.Button(labelFrame_edit, text = "Open \nPassword \nGenerator", command = open_pass_gen)
	password_gen.grid(column = 3, row = 4, columnspan = 2)

	#Web Site
	website_label_edit = ttk.Label(labelFrame_edit, text = "Enter the website:")
	website_label_edit.grid(column = 0, row =6, padx = 10, pady = 10)

	web_site_edit = tk.StringVar()
	website_entry_edit = ttk.Entry(labelFrame_edit, width = 25, textvariable = web_site_edit)
	website_entry_edit.grid(column = 1, row = 6, padx = 10, pady = 10)

	#Notes
	note_label_edit = ttk.Label(labelFrame_edit, text = "Notes:")
	note_label_edit.grid(column = 0, row =7, padx = 10, pady = 10)

	note_text_edit = scrolledtext.ScrolledText(labelFrame_edit, width = 19, height = 3, wrap = tk.WORD)
	note_text_edit.grid(column = 1, row = 7, columnspan = 2, padx = 10, pady = 10, sticky = "W")
	
	# Save button
	save_button_edit = tk.Button(edit_entry_window, text = "SAVE INFORMATION", 
			height = 3, width = 20, foreground = "white", background = "red", command = __confirm_edit)
	save_button_edit.grid(column = 0, row = 2, padx = 50, pady = 10, columnspan = 2, sticky = "W")

	# Delete button
	delete_button_edit = tk.Button(edit_entry_window, text = "DELETE ENTRY!", 
			height = 3, width = 20, foreground = "white", background = "red", command = __confirm_delete)
	delete_button_edit.grid(column = 0, row = 2, padx = 50, pady = 10, columnspan = 2, sticky = "E")

	edit_entry_window.mainloop()


# Header
title = tk.PhotoImage(file = 'icons/manager_header.gif')
title_gif = tk.Label(window, image = title)
title_gif.grid(column = 0, row = 0, columnspan = 2)

# Left side Panel 
left_panel = ttk.LabelFrame(window, text = "Options:")
left_panel.grid(column = 0, row = 1, padx = 10, pady = 30, sticky = "N")

#Left side buttons
button_new = ttk.Button(left_panel, text = "Add New Entry", width = 15, command = new_entry)
button_new.grid(column = 0, row = 1, padx = 10, pady = 20)

button_edit = ttk.Button(left_panel, text = "Edit or Delete Entry", width = 20, command = edit_entry)
button_edit.grid(column = 0, row = 3, padx = 10, pady = 20)

#Right side LabelFrame to hold all the password manager
right_panel = ttk.LabelFrame(window, text = "Password Manager")
right_panel.grid(column = 1, row = 1, padx = 10, pady = 30, sticky = "NW")

def selection_changed(self):
	#db_manager.show_Title_account() # MySQL DB
	db_manager_sqlite.show_Title_account() # SQLite DB
	title_value = entry_chosen.get()

	all_results_clean = db_manager_sqlite.extract_db_info(title_value)
	
	#assign variables to results form db
	final_user_title = all_results_clean[0]
	final_user_info = all_results_clean[1]
	final_password = all_results_clean[2]
	final_website = all_results_clean[3]
	final_notes = all_results_clean[4]
	
	#change the values in the GUI
	user_title_info.configure(text = final_user_title)
	user_info.configure(text = final_user_info)
	password_info.configure(text = final_password)
	website_info.configure(text = final_website)
	note_info.configure(text = final_notes)

intro_text = ttk.Label(right_panel, text = "Select a user account to see password details:")
intro_text.grid(column = 0, row = 0, padx = 20, pady = 10, sticky = "W")

db_manager_sqlite.show_Title_account()

password_entry = tk.StringVar()
entry_chosen = ttk.Combobox(right_panel, width = 40, textvariable = password_entry, state='readonly')
entry_chosen['values'] = db_manager_sqlite.words  # Shows titles from the DB
entry_chosen.grid(column=0, row=1,padx = 60, pady = 20)
entry_chosen.current(0)
entry_chosen.bind("<<ComboboxSelected>>", selection_changed)


#Database info on the user page:  
#User options, spaces and button
user_title = ttk.Label(right_panel, text = "Title of Account: ")
user_title.grid(column = 0, row = 3, padx = 20, pady = 20, sticky = "W")

user_title_info = ttk.Label(right_panel, text = " ", background = "white", width = 40)
user_title_info.grid(column = 0, row = 3, padx = 20, pady = 20, sticky = "E")

#User options, spaces and button
user_title = ttk.Label(right_panel, text = "User Account: ")
user_title.grid(column = 0, row = 4, padx = 20, pady = 20, sticky = "W")

user_info = ttk.Label(right_panel, text = " ", background = "white", width = 40)
user_info.grid(column = 0, row = 4, padx = 20, pady = 20, sticky = "E")

def _copy_user_account_Clipboard():
	"""Function to copy the password to the clipboard"""
	pyperclip.copy(user_info.cget("text"))

copy_user_button = ttk.Button(right_panel, text = "Copy to Clipboard", command = _copy_user_account_Clipboard)
copy_user_button.grid(column = 1, row = 4, padx = 10, pady = 10, sticky = "W")

#Password options, spaces and button
password_title = ttk.Label(right_panel, text = "Password: ")
password_title.grid(column = 0, row = 6, padx = 20, pady = 20, sticky = "W")

password_info = ttk.Label(right_panel, text = " ", background = "white", width = 40)
password_info.grid(column = 0, row = 6, padx = 20, pady = 20, sticky = "E")

def _copy_password_Clipboard():
	"""Function to copy the password to the clipboard"""
	pyperclip.copy(password_info.cget("text"))

copy_password_button = ttk.Button(right_panel, text = "Copy to Clipboard", command = _copy_password_Clipboard)
copy_password_button.grid(column = 1, row = 6, padx = 10, pady = 10, sticky = "W")

#Website options, spaces and button
website_title = ttk.Label(right_panel, text = "Web Site: ")
website_title.grid(column = 0, row = 8, padx = 20, pady = 20, sticky = "W")

website_info = ttk.Label(right_panel, text = " ", background = "white", width = 40)
website_info.grid(column = 0, row = 8, padx = 20, pady = 20, sticky = "E")

def _open_web_page():
	"""Small function to open the website in the GUI"""
	import webbrowser
	url = website_info.cget("text")
	if url[:3] == 'www' or url[:3] == 'htt':
		url = website_info.cget("text")
	else: 
		url = 'www.' + website_info.cget("text")
	
	webbrowser.open(url, new = 0, autoraise = True)

copy_website_button= ttk.Button(right_panel, text = "Open Web Site", width = 16, command = _open_web_page)
copy_website_button.grid(column = 1, row = 8, padx = 10, pady = 10, sticky = "W")


##### ADD A WIDGET FOR THE NOTES INFO!!!!!!!
note_title = ttk.Label(right_panel, text = "Notes: ")
note_title.grid(column = 0, row = 9, padx = 20, pady = 20, sticky = "W")

note_info = ttk.Label(right_panel, text = " ", background = "white", width = 40)
note_info.grid(column = 0, row = 9, padx = 20, pady = 20, sticky = "E")


#############################################
####### Creating the menu bar ###############
menu_bar = Menu(window)
window.config(menu = menu_bar)

def _quit():      # Function to close the main.py program
	window.quit()
	window.destroy()
	exit()

def _versionBox():     #Function to show the version
	msg.showinfo("About", "Password Manager    \
	           \n\n  {} \n\nBy Nicolás Táutiva".format(version))

def _openGit():
	"""Small function to open my git web site"""
	import webbrowser
	url = 'www.github.com/NickATC'
	webbrowser.open(url, new = 0, autoraise = True)

def drop_db():
	"""To delete / drop database.  Use with caution!"""
	
	def __confirm_deleteDB():
		reply = msg.askyesnocancel("DELETE DATABASE!!", "Are you sure you want to delete all the database and the information it contains?")
		print(reply)
		
		if reply == True:
			#delete / drop DB
			db_manager_sqlite.drop_db()

			#open new window confirming user that the info was saved!
			msg.showinfo("", "Database deleted!")
	
	__confirm_deleteDB()
	
#Creating the menu and adding items
file_menu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Options", menu = file_menu)
file_menu.add_command(label = "Add entry", command = new_entry)
file_menu.add_command(label = "Edit or delete entry", command = edit_entry)
file_menu.add_command(label = "Open Password Generator", command = open_pass_gen)
file_menu.add_command(label = "Delete Database !", command = drop_db) 
file_menu.add_command(label = "Exit", command = _quit)


help_menu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "User guide")     ####    the USER GUIDE is pending!!!
help_menu.add_command(label = "Follow me on Git", command = _openGit)
help_menu.add_command(label = "About", command = _versionBox)

window.mainloop()
