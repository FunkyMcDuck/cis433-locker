from tkinter import *
from PIL import ImageTk,Image
import redis
import sys
import os

sys.path.append("../encryption")
#from encryption import database
#from encryption import encryption
'''
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
'''

root = Tk()
root.title('Encryption App')
root.iconbitmap('images/iconsmall.ico')
root.geometry("400x600")

# Databases
r = redis.Redis(host='localhost', port=6379, db=1)
n = 0

# TODO: Multiple entries
#		File ID selection

# Create Update function to update a record
def update():
	record_id = delete_box.get()

	'''
	c.execute("""UPDATE createdes SET
		file_name = :first,
		file_type = :last,
		created = :created,
		modified = :modified,
		accessed = :accessed,
		saved = :saved 

		WHERE oid = :oid""",
		{
		'file_name': f_name_editor.get(),
		'file_type': f_type_editor.get(),
		'created': created_editor.get(),
		'modified': modified_editor.get(),
		'accessed': accessed_editor.get(),
		'saved': saved_editor.get(),
		'oid': record_id
		})
		'''

	r.hset(n, 'file_name', f_name_editor.get())
	r.hset(n, 'file_type', f_name_editor.get())
	r.hset(n, 'created', f_name_editor.get())
	r.hset(n, 'modified', f_name_editor.get())
	r.hset(n, 'accessed', f_name_editor.get())
	r.hset(n, 'saved', f_name_editor.get())

	editor.destroy()
	root.deiconify()

# Create Edit function to update a record
'''
def edit():
	root.withdraw()
	global editor
	editor = Tk()
	editor.title('Update A Record')
	editor.iconbitmap('images/iconsmall.ico')
	editor.geometry("400x300")
	# Create a database or connect to one
	#conn = sqlite3.connect('file_directory.db')
	# Create cursor
	#c = conn.cursor()

	record_id = delete_box.get()
	# Query the database
	c.execute("SELECT * FROM createdes WHERE oid = " + record_id)
	records = c.fetchall()
	
	#Create Global Variables for text box names
	global f_name_editor
	global f_type_editor
	global created_editor
	global modified_editor
	global accessed_editor
	global saved_editor

	# Create Text Boxes
	f_name_editor = Entry(editor, width=30)
	f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
	f_type_editor = Entry(editor, width=30)
	f_type_editor.grid(row=1, column=1)
	created_editor = Entry(editor, width=30)
	created_editor.grid(row=2, column=1)
	modified_editor = Entry(editor, width=30)
	modified_editor.grid(row=3, column=1)
	accessed_editor = Entry(editor, width=30)
	accessed_editor.grid(row=4, column=1)
	saved_editor = Entry(editor, width=30)
	saved_editor.grid(row=5, column=1)
	
	# Create Text Box Labels
	f_name_label = Label(editor, text="File Name")
	f_name_label.grid(row=0, column=0, pady=(10, 0))
	f_type_label = Label(editor, text="File Type")
	f_type_label.grid(row=1, column=0)
	created_label = Label(editor, text="Created")
	created_label.grid(row=2, column=0)
	modified_label = Label(editor, text="Modified")
	modified_label.grid(row=3, column=0)
	accessed_label = Label(editor, text="Accessed")
	accessed_label.grid(row=4, column=0)
	saved_label = Label(editor, text="Save Date")
	saved_label.grid(row=5, column=0)

	# Loop thru results
	for record in records:
		f_name_editor.insert(0, record[0])
		f_type_editor.insert(0, record[1])
		created_editor.insert(0, record[2])
		modified_editor.insert(0, record[3])
		accessed_editor.insert(0, record[4])
		saved_editor.insert(0, record[5])

	
	# Create a Save Button To Save edited record
	edit_btn = Button(editor, text="Save File", command=update)
	edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

'''


# Create Function to Delete A Record
def delete():
	# TODO: Formatting
	# Delete a record
	#c.execute("DELETE from createdes WHERE oid = " + delete_box.get())

	r.hdel("entry", "file_name")
	r.hdel("entry", "file_type")
	r.hdel("entry", "created")
	r.hdel("entry", "modified")
	r.hdel("entry", "accessed")
	r.hdel("entry", "saved")

	delete_box.delete(0, END)


# Create Submit Function For database
def submit():
	# Create a database or connect to one
	# conn = sqlite3.connect('file_directory.db')
	# Create cursor
	# c = conn.cursor()

	# Insert Into Table
	'''
	c.execute("INSERT INTO createdes VALUES (:f_name, :f_type, :created, :modified, :accessed, :saved)",
			{
				'f_name': f_name.get(),
				'f_type': f_type.get(),
				'created': created.get(),
				'modified': modified.get(),
				'accessed': accessed.get(),
				'saved': saved.get()
			})
			'''

	r.hset("entry", "f_name", f_name.get())
	r.hset("entry", "f_type", f_type.get())
	r.hset("entry", "created", created.get())
	r.hset("entry", "modified", modified.get())
	r.hset("entry", "accessed", accessed.get())
	r.hset("entry", "saved", saved.get())

	# Clear The Text Boxes
	f_name.delete(0, END)
	f_type.delete(0, END)
	created.delete(0, END)
	modified.delete(0, END)
	accessed.delete(0, END)
	saved.delete(0, END)

# Create Query Function
def query():

	# Query the addresses
	records = r.hgetall("entry")
	print(records)

	# Loop Thru Results
	print_records = ''
	for record in records:
		print_records += str(record) + "\n"

	query_label = Label(root, text=records)
	query_label.grid(row=12, column=0, columnspan=2)

	# TODO: Format query


# Create Text Boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
f_type = Entry(root, width=30)
f_type.grid(row=1, column=1)
created = Entry(root, width=30)
created.grid(row=2, column=1)
modified = Entry(root, width=30)
modified.grid(row=3, column=1)
accessed = Entry(root, width=30)
accessed.grid(row=4, column=1)
saved = Entry(root, width=30)
saved.grid(row=5, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)


# Create Text Box Labels
f_name_label = Label(root, text="File Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))
f_type_label = Label(root, text="File Type")
f_type_label.grid(row=1, column=0)
created_label = Label(root, text="Created")
created_label.grid(row=2, column=0)
modified_label = Label(root, text="Modified")
modified_label.grid(row=3, column=0)
accessed_label = Label(root, text="Accessed")
accessed_label.grid(row=4, column=0)
saved_label = Label(root, text="Saved Date")
saved_label.grid(row=5, column=0)
delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=9, column=0, pady=5)

# Create Submit Button
submit_btn = Button(root, text="Add File to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a Query Button
query_btn = Button(root, text="Show Files", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Create A Delete Button
delete_btn = Button(root, text="Delete Files", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Create an Update Button
edit_btn = Button(root, text="Edit Files", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

root.mainloop()