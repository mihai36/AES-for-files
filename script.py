from Cryptodome.Cipher import AES
import hashlib
import string
import random
import os
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

class AESfiles:
    def pad_IV(msg):
        padding=""
        if len(msg) < 16:
            while len(msg) % 16 != 0:
                char = random.choice(string.ascii_letters)
                msg = msg  + char.encode()
                padding += char
        else:
            msg = msg[0:16]
        return msg, padding
    def pad_file(msg):
        while len(msg) % 16 != 0:
            msg = msg + ' '.encode()
        return msg
    def encrypt(path, key, iv, mode):
        ivX, pad = AESfiles.pad_IV(iv)
        cipher = AES.new(key, mode, ivX) 
        with open(path, 'rb') as f:
            content = f.read()
        pcontent = AESfiles.pad_file(content)
        print("IV: " + iv.decode() + pad)
        ct = cipher.encrypt(pcontent)
        with open(path, 'wb') as e:
            e.write(ct)
        return pad, ct
    def decrypt(path, key, iv, mode):
        cipher = AES.new(key, mode, iv)
        with open(path, 'rb') as f:
            content = f.read()
        print("IV: " + iv.decode())
        pcontent = AESfiles.pad_file(content)
        pt = cipher.decrypt(pcontent)
        with open(path, 'wb') as e:
            e.write(pt)
        return pt
    def walk(path):
        files = list()
        for (p, d, f) in os.walk(path):
            files += [os.path.join(p, filex) for filex in f]
        return files

if __name__ == '__main__':
    window = Tk()
    window.title("Symetric Encryption")
    window.configure(background="black")
    def popUp(message):
        messagebox.showinfo("Status", message)
    def enc():
        if ivX.get() == "" or keyX.get() == "":
            popUp("Input key and iv")
        else:
            try:
                print("\t\t\t---Encryption---")
                window.filename = fd.askopenfilename(title="Encrypt File", filetypes=(("all files", "*.*"),("jpg files", "*.jpg")))
                password = keyX.get().encode()
                key = hashlib.sha3_256(password).digest()
                iv = ivX.get().encode()
                mode = AES.MODE_CBC
                print(window.filename)
                print("Key: " + password.decode())
                pad, ct = AESfiles.encrypt(window.filename, key, iv, mode)
                ivX.insert(END, pad)
                ivX.delete(16, END)
                popUp("The file has been encrypted!")
            except:
                popUp("Select file")
    def dec():
        if ivX.get() == "" or keyX.get() == "":
            popUp("Input key and iv")
        else:
            try:
                print("\t\t\t---Decryption---")
                window.filename = fd.askopenfilename(initialdir='/', title="Decrypt File", filetypes=(("all files", "*.*"),("jpg files", "*.jpg")))
                password = keyX.get().encode()
                key = hashlib.sha3_256(password).digest()
                iv = ivX.get().encode()
                mode = AES.MODE_CBC
                print(window.filename)
                print("Key: " + password.decode()) 
                AESfiles.decrypt(window.filename, key, iv, mode)
                keyX.delete(0, END)
                ivX.delete(0, END)
                popUp("The file has been decrypted!")
            except:
                popUp("Select file ")
    def encD():
        if ivX.get() == "" or keyX.get() == "":
            popUp("Input key and iv")
        else:
            try:
                print("\t\t\t---Encryption---")
                path = fd.askdirectory()
                password = keyX.get().encode()
                key = hashlib.sha3_256(password).digest()
                iv = ivX.get().encode()
                mode = AES.MODE_CBC
                files = AESfiles.walk(path)
                pad=""  
                for filex in files:
                    print(filex)
                    print("Key: " + password.decode())
                    pad, ct = AESfiles.encrypt(filex, key, iv, mode)
                ivX.insert(END, pad)
                ivX.delete(16, END)
                popUp("The files has been encrypted!")
            except:
                popUp("Select directory")
    def decD():
        if ivX.get() == "" or keyX.get() == "":
            popUp("Input key and iv")
        else:
            try:
                print("\t\t\t---Decryption---")
                path = fd.askdirectory()
                password = keyX.get().encode()
                key = hashlib.sha3_256(password).digest()
                iv = ivX.get().encode()
                mode = AES.MODE_CBC
                files = AESfiles.walk(path)
                pad=""
                for filex in files:
                    AESfiles.decrypt(filex, key, iv, mode)
                keyX.delete(0, END)
                ivX.delete(0, END)
                popUp("The files has been decrypted!")
            except:
                popUp("Select directory")
    def save():
        try:
            path = fd.askopenfilename(initialdir='/', title="Save to file" )
            with open(path, "a") as f:
                f.write(path + "\nKey: " + keyX.get() + "\t\t\t ----> IV: " + ivX.get() + "\n\n")
            popUp("Keys were saved")
        except:
            popUp("Select File ")

    Label (window, text="Encrypt files with AES", bg="black", fg="royalblue", font="none 18 bold").grid(row=0, column=0, sticky=W, pady=(6, 21))
    keyX = Entry(window, width=41, bg="black", fg="white")
    keyX.grid(row=3, column=0, columnspan=2, sticky=W)
    ivX = Entry(window, width=32, bg="black", fg="white")
    ivX.grid(row=5, column=0, sticky=W)
    Label (window, text="Key", bg="black", fg="cyan3", font="none 11 bold").grid(row=2, column=0, sticky=W, padx=(3,0))
    Label (window, text="IV", bg="black", fg="cyan3", font="none 11 bold").grid(row=4, column=0, sticky=W, pady=(30,0), padx=(3,0))
    Button(window, text="Encrypt File", width=9, bg="dodgerblue", command=enc).grid(row=3, column=2, sticky=W, padx=(70,0))
    Button(window, text="Decrypt File", width=9, bg="dodgerblue", command=dec).grid(row=4, column=2, sticky=W, pady=(9, 18), padx=(70,0))
    Button(window, text="Encrypt Directory", width=12, bg="dodgerblue", command=encD).grid(row=6, column=2, sticky=W, padx=(50,0), pady=(30,0))
    Button(window, text="Decrypt Directory", width=12, bg="dodgerblue", command=decD).grid(row=7, column=2, sticky=W, padx=(50,0), pady=(9,0))
    Button(window, text="Save keys", width=9, bg="cyan4", command=save).grid(row=7, column=0, sticky=W, padx=(0, 10))
    window.mainloop()
