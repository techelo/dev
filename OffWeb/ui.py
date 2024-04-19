from logging import root
import os
import re
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests

def download_website():
    url = url_entry.get()
    download_path = os.path.join("/workspaces/dev", os.path.basename(url))
    file_types = file_types_entry.get().split() if file_types_var.get() else None
    keywords = keywords_entry.get().split() if keywords_var.get() else None
    follow_links = follow_links_var.get()

    try:
        download_website_impl(url, download_path, file_types, keywords, follow_links)
        messagebox.showinfo("Success", "Download completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_website_impl(url, download_path, file_types=None, keywords=None, follow_links=False):
    # Same as before

 root = tk.Tk()
 root.title("Website Downloader")

tk.Label(root, text="URL:").pack() # type: ignore
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="File types (separated by spaces):").pack()
file_types_entry = tk.Entry(root, width=50)
file_types_entry.pack()
file_types_var = tk.BooleanVar()
tk.Checkbutton(root, text="Download file types", variable=file_types_var).pack() # type: ignore

tk.Label(root, text="Keywords (separated by spaces):").pack() # type: ignore
keywords_entry = tk.Entry(root, width=50)
keywords_entry.pack()
keywords_var = tk.BooleanVar()
tk.Checkbutton(root, text="Search keywords", variable=keywords_var).pack()

follow_links_var = tk.BooleanVar()
tk.Checkbutton(root, text="Follow links", variable=follow_links_var).pack()

tk.Button(root, text="Download", command=download_website).pack()

root.mainloop()