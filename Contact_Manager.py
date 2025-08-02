from tkinter import *
import tkinter.messagebox as tmsg
import pymysql

# connecting to db
def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="your_password", # Enter your mysql password here--
        port=3306,
        database="contact_db"
    )

def save_to_db(name,phone,email,address):
    try:
        conn=connect_db()
        cursor=conn.cursor()
        insert_sql="insert into contacts(name,phone,email,address) values (%s,%s,%s,%s)"
        cursor.execute(insert_sql,(name,phone,email,address))
        conn.commit()

        tmsg.showinfo("Successfully Added to List","Contact has been saved")
    except pymysql.err.IntegrityError:
        tmsg.showerror("Error","Contact already exists")

    except Exception as e:
        tmsg.showerror("Databae Error",str(e))



# Add Contact Function (placeholder)
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:
        save_to_db(name,phone,email,address)
    else:
        tmsg.showwarning("Missing Info","Name and Phone are required!")

# Clear all field after 1 entry-
def clear_fields():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)
    address_entry.delete(0, END)
    name_entry.focus_set()


# Fetching details from db
def show_contacts():
    try:
        conn =connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, email, address FROM contacts")
        rows = cursor.fetchall()
        conn.close()

        # Show in new popup
        win = Toplevel()
        win.title("All Contacts")
        win.geometry("500x300")
        win.iconbitmap("contact_book.ico")
        win.configure(bg="#fff")



        scrollbar = Scrollbar(win)
        scrollbar.pack(side="right", fill="y")
        text_area = Text(win, font=("Calibri", 11),yscrollcommand=scrollbar.set)
        text_area.pack(fill="both", expand=True)
        scrollbar.config(command=text_area.yview)

        for row in rows:
            name, phone, email, address = row
            text_area.insert(END, f"👤 {name}\n📞 {phone}\n📧 {email}\n🏠 {address}\n{'-'*40}\n")


    except Exception as e:
        tmsg.showerror("Error",f"MySql Workbench must in running state\n{str(e)}")

# Edit contact details-
current_id=None
def load_for_edit(name):
    global current_id

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id,name, phone, email, address FROM contacts WHERE name = %s", (name,))
        contact = cursor.fetchone()
        conn.close()

        if contact:
            current_id = contact[0]
            name_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            address_entry.delete(0, END)

            name_entry.insert(0, contact[1])
            phone_entry.insert(0, contact[2])
            email_entry.insert(0, contact[3])
            address_entry.insert(0, contact[4])

        else:
            tmsg.showerror("Not Found", f"No contact found with name '{name}'")

    except Exception as e:
        tmsg.showerror("Database Error", str(e))

# Updating-Edited contact
def update_contact():
    global current_id

    if current_id is None:
        tmsg.showwarning("Select Contact", "Please use Edit first to load a contact!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s"
        cursor.execute(query, (
            name_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            address_entry.get(),
            current_id
        ))
        conn.commit()
        conn.close()

        tmsg.showinfo("Updated", "Contact updated successfully!")
        clear_fields()

    except Exception as e:
        tmsg.showerror("Database Error", str(e))

# Deleting a contact
def delete_contact():
    name = name_entry.get()
    phone = phone_entry.get()

    if phone == "" and name == "":
        tmsg.showwarning("Input Error", "Please enter the Name or Phone number to delete!")
        return

    confirm = tmsg.askyesno("Confirm Delete", f"Are you sure you want to delete this contact?\n{name} {phone}")

    if confirm:
        try:
            conn =connect_db()
            cursor = conn.cursor()
            if phone !="":
                query = "DELETE FROM contacts WHERE phone = %s"
                cursor.execute(query, (phone,))     # (phone)- str, (phone,)- tuple.
            else:
                query = "DELETE FROM contacts WHERE name = %s"
                cursor.execute(query, (name,))    # Syntax for making tuple with 1 argument (name,).

            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                tmsg.showinfo("Not Found", "No contact found with given input.")
            else:
                tmsg.showinfo("Deleted", f"Successfully Deleted this contact!")
                clear_fields()

        except Exception as e:
            tmsg.showerror("Database Error", str(e))
# GUI Setup
root = Tk()
root.title("My Contact Manager")
root.geometry("520x450")
root.iconbitmap("contact_book.ico")
root.configure(bg="#e8f0fe")  # Light blue background
root.resizable(False, False)

# Heading
heading = Label(root, text="📒 Contact Book", font="Helvetica 18 bold", fg="#333", bg="#e8f0fe")
heading.grid(row=0, column=0, columnspan=2, pady=20)

# Labels and Entry Fields
Label(root, text="Name:", font="Calibri 12 bold", bg="#f0f8ff").grid(row=1, column=0, padx=20, pady=10, sticky=W)
name_entry = Entry(root, width=35, font="Calibri 12")
name_entry.grid(row=1, column=1, padx=10)

Label(root, text="Phone:", font="Calibri 12 bold", bg="#f0f8ff").grid(row=2, column=0, padx=20, pady=10, sticky=W)
phone_entry = Entry(root, width=35, font="Calibri 12")
phone_entry.grid(row=2, column=1, padx=10)

Label(root, text="Email:", font="Calibri 12 bold", bg="#f0f8ff").grid(row=3, column=0, padx=20, pady=10, sticky=W)
email_entry = Entry(root, width=35, font="Calibri 12")
email_entry.grid(row=3, column=1, padx=10)

Label(root, text="Address:", font="Calibri 12 bold", bg="#f0f8ff").grid(row=4, column=0, padx=20, pady=10, sticky=W)
address_entry = Entry(root, width=35, font="Calibri 12")
address_entry.grid(row=4, column=1, padx=10)

# Buttons
Button(root, text="  ➕ Add Contact  ", bg="#28a745", fg="white", font=("Segoe UI",10,"bold"),
       width=15, command=add_contact).grid(row=5, column=0, pady=15, padx=20)

Button(root, text="🧹 Clear    ", bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold"),
       width=15, command=clear_fields).grid(row=5, column=1,pady=15, padx=20)

Button(root, text="🧨 Delete Contact", bg="#6c3483", fg="white",font=("Segoe UI", 10, "bold"),
       width=20, command=delete_contact).grid(row=6, column=0, columnspan=2, pady=10,padx=20,sticky=W)

Button(root, text="📋 Show All Contacts", bg="#007bff", fg="white", font=("Segoe UI", 10, "bold"),
       width=20, command=show_contacts).grid(row=6, column=1, columnspan=2, pady=10,padx=20)

Button(root, text="✏ Edit (by Name)", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"),
       width=20, command=lambda: load_for_edit(name_entry.get())).grid(row=7, column=0, pady=10, padx=20)

Button(root, text="🔁 Update Contact", bg="#17a2b8", fg="white", font=("Segoe UI", 10, "bold"),
       width=20, command=update_contact).grid(row=7, column=1, pady=10, padx=20)

# Start the App
root.mainloop()