import tkinter as tk
from tkinter import filedialog, messagebox
import smtplib
import pandas as pd
import ssl

def send_emails():
    try:
        email_address = email_entry.get()
        email_password = password_entry.get()
        subject = subject_entry.get()

        # Read recipients
        df = pd.read_csv(recipients_file_path.get())
        with open(template_file_path.get(), 'r') as f:
            template = f.read()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_address, email_password)

            for index, row in df.iterrows():
                personalized_msg = template.replace("{name}", row['Name'])
                message = f"Subject: {subject}\n\n{personalized_msg}"
                server.sendmail(email_address, row['Email'], message)

        messagebox.showinfo("Success", "✅ Emails sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to send emails:\n{e}")

def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    recipients_file_path.set(filename)

def browse_template():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    template_file_path.set(filename)

# GUI setup
root = tk.Tk()
root.title("📧 Python Email Sender")
root.geometry("400x300")

email_entry = tk.Entry(root, width=40)
password_entry = tk.Entry(root, show='*', width=40)
subject_entry = tk.Entry(root, width=40)

recipients_file_path = tk.StringVar()
template_file_path = tk.StringVar()

tk.Label(root, text="Your Gmail Address").pack()
email_entry.pack()

tk.Label(root, text="Gmail App Password").pack()
password_entry.pack()

tk.Label(root, text="Email Subject").pack()
subject_entry.pack()

tk.Button(root, text="📂 Select CSV File", command=browse_csv).pack(pady=5)
tk.Button(root, text="📂 Select Template File", command=browse_template).pack(pady=5)
tk.Button(root, text="✉️ Send Emails", command=send_emails, bg="green", fg="white").pack(pady=10)

root.mainloop()
