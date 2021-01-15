from tkinter import * #mengimport semua class tkinter
from tkinter import messagebox #mengimport class messgebox dari tkinter
from tkinter.filedialog   import asksaveasfilename #mengimport ‘askopenfilename’ dari class ‘filedialog’ tkinter
from tkinter import filedialog #mengimport class file dialog dari library tkinter
import os, webbrowser #mengimport class python yaitu os
from tkinter.messagebox import askokcancel #mengimport messegebox sebagi ‘askokcancel’
from tkinter import messagebox as mbox #mengimport massage box

class SimpleEditor(Frame): #membuat class ‘SImpleEditor’ dengan inheritence class ‘Frame’ (di tkinter)
    def __init__(self, parent=None, file=None):
        Frame.__init__(self, parent)
        self.frm = Frame(parent) #membuat frame untuk toolbar
        self.frm.pack(fill=X) #memasukkan frame ke window
        self.buatJudul() #menjalankan metode ‘buatJudul’
        self.parent = parent
        self.parent.title('Text editor')
        self.buatTombol() #menjalankan metode buatTombol
        self.kolomTeksUtama() #menjalankan metode ‘kolomTeksUtama’
        self.settext(text='',file=file) #memasukkan teks (kosongan)
        self.kolomTeks.config(font=('DejaVu Sans Mono', 10)) #mengatur jenis dan ukuran teks
        self.path = ''
        self.indeks = '0.9' #inisialisasi variabel ‘indeks’ sebagai penentu lokasi pencarian
        self.buatCari() #menjalankan metode ‘buatCari’
        self.buatMenuBar() # menjalankan metode 'buat Cari'

    def buatTombol(self): #metode ‘buatTombol’
        Button(self.frm, text='Open',relief='flat',  command=self.bukaFile).pack(side=LEFT)
        Button(self.frm, text='Save',relief='flat',  command=self.perintahSimpan).pack(side=LEFT)
        Button(self.frm, text='Copy', relief='flat', command=self.perintahCopy).pack(side=LEFT)
        Button(self.frm, text='Cut', relief='flat',   command=self.perintahCut).pack(side=LEFT)
        Button(self.frm, text='Paste', relief='flat', command=self.perintahPaste).pack(side=LEFT)
        Button(self.frm, text='Undo', relief='flat',   command=self.perintahUndo).pack(side=LEFT)
        Button(self.frm, text='Redo', relief='flat', command=self.perintahRedo).pack(side=LEFT)
        Button(self.frm, text='Keluar', relief='flat', command=self.perintahKeluar).pack(side=LEFT)

    def kolomTeksUtama(self): #metode ‘kolomTeksUtama’
        scroll = Scrollbar(self)
        kolomTeks = Text(self, relief=SUNKEN, undo=True)
        scroll.config(command=kolomTeks.yview)
        kolomTeks.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        kolomTeks.pack(side=LEFT, expand=YES, fill=BOTH)
        self.kolomTeks = kolomTeks
        self.pack(expand=YES, fill=BOTH)

    def buatMenuBar(self): #metode ‘menu bar’
        self.menubar = Menu(self.parent,bd=0)
        self.fileMenu = Menu(self.parent, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.bukaFile)
        self.fileMenu.add_command(label="Save", command=self.perintahSimpan)
        self.fileMenu.add_command(label="Exit", command=self.perintahKeluar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        self.menuEdit = Menu(self.parent, tearoff=0)
        self.menuEdit.add_command(label="Undo", command=self.perintahUndo)
        self.menuEdit.add_command(label="Redo", command=self.perintahRedo)
        self.menuEdit.add_separator()
        self.menuEdit.add_command(label="Copy", command=self.perintahCopy)
        self.menuEdit.add_command(label="Cut", command=self.perintahCut)
        self.menuEdit.add_command(label="Paste", command=self.perintahPaste)
        self.menubar.add_cascade(label="Edit", menu=self.menuEdit)

        self.menuWeb = Menu(self.parent, tearoff=0)
        self.menuWeb.add_command(label="Go to Website", command=self.pergiKeWeb)
        self.menubar.add_cascade(label="Web", menu=self.menuWeb)

        self.menuAbout = Menu(self.parent, tearoff=0)
        self.menuAbout.add_command(label="Tentang aplikasi", command=self.about)
        self.menubar.add_cascade(label="About", menu=self.menuAbout)

        self.parent.config(menu=self.menubar)
        self.pack()

    def perintahSimpan(self): #metode ‘perintahSImpan'
        print(self.path) #perulangan agar path tidak kosong
        if self.path:
            alltext = self.gettext()
            open(self.path, 'w').write(alltext)
            messagebox.showinfo('Berhasil', 'Selamat File telah tersimpan ! ')
        else:
            tipeFile = [('Text file', '*.txt'), ('Python file', '*asdf.py'), ('All files', '.*')] #membuka tipe yang di cari  di file dialog untuk menyimpan file
            filename = asksaveasfilename(filetypes=(tipeFile), initialfile=self.kolomJudul.get())
            if filename: 
                alltext = self.gettext()
                open(filename, 'w').write(alltext)
                self.path = filename

    def perintahCopy(self): #metode ‘perintahCopy’
        try:
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST) #mendapatkan teks yang di select atau di blok
            self.clipboard_clear()#membersihkan clip board
            self.clipboard_append(text) #memasukkan teks ke klip board
            self.kolomTeks.selection_clear() #membersihkan pemilihan teks
        except:
            pass

    def perintahCut(self): #metode ‘perintahCut’
        try :
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.kolomTeks.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except:
            pass

    def perintahPaste(self): #metode ‘perintahPaste’
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.kolomTeks.insert(INSERT, text)
        except TclError:
            pass

    def perintahFind(self): #metode ‘perintahFind’
        target = self.kolomCari.get() #mendapatkan teks dari kolom cari (teks yang akan di cari)
        if target:
            self.indeks = self.kolomTeks.search(target, str(float(self.indeks)+0.1), stopindex=END) #mencari file
            if self.indeks:
                pastit = self.indeks + ('+%dc' % len(target)) #mendapatkan jumlah karakter
                self.kolomTeks.tag_remove(SEL, '1.0', END)
                self.kolomTeks.tag_add(SEL, self.indeks, pastit)
                self.kolomTeks.mark_set(INSERT, pastit)
                self.kolomTeks.see(INSERT)
                self.kolomTeks.focus()
            else: #jika ‘self.indeks’ kosong
                self.indeks = '0.9'

    def perintahKeluar(self): #metode perintah keluar
        ans = askokcancel('Keluar', "anda yakin ingin keluar?") #menampilkan kotak konfirmasi
        if ans: Frame.quit(self) #menutup window jika user klik ok

    def settext(self, text='', file=None): #metode settext
        if file:
            text = open(file, 'r').read()
        self.kolomTeks.delete('1.0', END)
        self.kolomTeks.insert('1.0', text)
        self.kolomTeks.mark_set(INSERT, '1.0')
        self.kolomTeks.focus()

    def gettext(self):
        return self.kolomTeks.get('1.0', END+'-1c')

    def buatJudul(self): #metode buatJudul
        top = Frame(root)
        top.pack(fill=BOTH, padx=17, pady=5)
        judul = Label(top, text="Judul : ")
        judul.pack(side="left")
        self.kolomJudul = Entry(top)
        self.kolomJudul.pack(side="left")

    def buatCari(self): #metode ‘buatCari’
        Button(self.frm, text='Cari', command=self.perintahFind).pack(side="right")
        self.kolomCari = Entry(self.frm)
        self.kolomCari.pack(side="right")

    def bukaFile(self): #metode bukaFile
        extensiFile = [ ('All files', '*'), ('Text files', '*.txt'),('Python files', '*.py')]
        buka = filedialog.askopenfilename(filetypes = extensiFile)
        if buka != '':
            text = self.readFile(buka)
            if text:
                self.path = buka
                nama = os.path.basename(buka)
                self.kolomJudul.delete(0, END)
                self.kolomJudul.insert(END, nama)
                self.kolomTeks.delete('0.1',END)
                self.kolomTeks.insert(END, text)

    def readFile(self, filename): #metode ‘readFile’
        try:
            f = open(filename, "r")
            text = f.read()
            return text
        except:
            messagebox.showerror("Error!!","Maaf file tidak dapat dibuka ! :) \nsabar ya..")
            return None

    def about(self): #metode ‘about’
        mbox.showinfo("Tentang Aplikasi", "Aplikasi ini merupakan contoh aplikasi text editor.\n"
                                          "namun, lebih dari itu, aplikasi sederhana ini bisa\n"
                                          "kalian gunakan untuk membuat file teks dan juga file python\n"
                                          "\ngimana ? menarikkan ?\n"
                                          "\nya semoga aplikasoi sederhana ini dapat bermanfaat bagi kalian.")
    def pergiKeWeb(self):
        webbrowser.open_new(r"http://mn-belajarpython.blogspot.co.id")

    def perintahUndo(self): #metode ‘perintahUndo’
        try:
            self.kolomTeks.edit_undo()
        except:
            pass
    def perintahRedo(self): #/metode ‘perintahRedo’
        try:
            self.kolomTeks.edit_redo()
        except:
            pass
root = Tk() #menampilkan window Tkinter
SimpleEditor(root) #menjalankan metode ‘SimpleEditor’
mainloop() #agar window tidak langsung close saat di jalankan
