from tkinter import *
from tkinter.messagebox import showinfo,showerror,askokcancel
from tkinter.ttk import Frame,Button,Label,Entry,Style
from tkinter import filedialog
import tkinter.font as font
import pandas as pd
import numpy as np
import sys
import os
import datetime
import ctypes

pd.options.mode.chained_assignment = None  # default='warn'
#Supaya kolomnya tampil semua
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_rows', None)

#Pergerakan rata2 terbobot/weighted moving average 3-hari
#Bobot masing=masing
w1=0.2
w2=0.3
w3=0.5
#Penjumlahan bobot total (dengan total bobot=1)
weights1=np.array([w1,w2,w3])
sum_weights1=np.sum(weights1)


#Pergerakan rata2 terbobot/weighted moving average 5-hari
#Bobot masing=masing
w4=0.1
w5=0.15
w6=0.2
w7=0.25
w8=0.3  
weights2=np.array([w4,w5,w6,w7,w8])
sum_weights2=np.sum(weights2)


class FormUtama(Frame):#Form Utama
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.InitUI()

    def InitUI(self):
        #=======Konfigurasi font untuk form========#
        font_style=Style()
        font_style.configure('my.TButton',font=('Arial',11))
        
        #=======Label Nama File========#
        self.frame1=Frame()
        self.frame1.pack(fill=X)
        
        self.lbl=Label(self.frame1,text="Nama File",font="Arial 12 bold")
        self.lbl.pack(side=LEFT,padx=5,pady=5)
       
        #=======Textbox Nama File========#
        self.frame2=Frame()
        self.frame2.pack(fill=BOTH,expand=True)
        
        self.text1_Text=StringVar()
        self.text1=Entry(self.frame2,font="Arial 14",state=DISABLED,textvariable=self.text1_Text)
        self.text1.pack(side=LEFT,anchor=NW,fill=X,expand=True,padx=5,pady=5)
        
        #=======Kumpulan tombol untuk membuka dan menjalankan file CSV========#
        
        self.frame3=Frame()
        self.frame3.pack(fill=BOTH,expand=True)
           
        self.actBtn1=Button(self.frame3,text="Pilih File CSV",style='my.TButton',command=self.open_dialog,image=ikon_buka_file,compound=LEFT)
        self.actBtn1.pack(side=LEFT,padx=5,pady=5)
        
        
        self.actBtn2=Button(self.frame3,text="Jalankan Program",state=DISABLED,style='my.TButton',command=self.tes_dataframe,image=ikon_buka_program,compound=LEFT)
        self.actBtn2.pack(side=RIGHT,padx=5,pady=5)
        
        
        #========Label informasi dan tombol informasi program=======#
        self.frame4=Frame()
        self.frame4.pack(side=LEFT,anchor=N)
        
        self.lbl2=Label(self.frame4,text="Informasi:",font="Arial 12 bold")
        self.lbl2.pack(side=LEFT,padx=5,pady=5)     
        
        self.helpBtn=Button(self.frame4,text="Panduan Penggunan Program",style='my.TButton',command=self.form_guide,image=ikon_guide,compound=LEFT)
        self.helpBtn.pack(side=LEFT,padx=5,pady=5,anchor=N)
        
        self.aboutBtn=Button(self.frame4,text="Tentang Program",style='my.TButton',command=self.form_about,image=ikon_info,compound=LEFT)
        self.aboutBtn.pack(side=RIGHT,padx=5,pady=5,anchor=N)
        #===============#
    
    def form_about(self):#Untuk membuka form tentang program
        self.newWindow=Toplevel(self.parent)
        self.newWindow.title("Tentang Program")
        self.newWindow.geometry("500x150")
        self.newWindow.resizable(False,False)
        self.app=FormAbout(self.newWindow)    
        
    def form_guide(self):#Untuk membuka form tentang penggunaan program
        self.newWindow=Toplevel(self.parent)
        self.newWindow.title("Panduan Penggunaan Program")
        self.newWindow.geometry("500x400")
        self.newWindow.resizable(False,False)
        self.app=FormGuide(self.newWindow)
        
    def open_dialog(self):#Memilih file CSV
        try:
            self.fileName=filedialog.askopenfilename(initialdir="/",filetypes=(("Comma-separated values","*.csv"),))
            if len(self.fileName)==0:
                raise FileNotFoundError
            else:
                self.text1_Text.set(self.fileName)
                self.actBtn2['state']=NORMAL                
        except FileNotFoundError:
            showerror("Peringatan","File belum dipilih!")

    def tes_dataframe(self):#Untuk membuka file CSV
        try:
            global df,fileName
            fileName=self.fileName
            data=pd.read_csv(self.text1.get(),sep=",")
            df=pd.DataFrame(data)  
            
            if not any(df.columns==['Date','Close']):
                raise ValueError
            else: 
                showinfo(title="Pemberitahuan",message="Kolom yang dibutuhkan telah ditemukan.") 
                root.destroy() 
        except ValueError:
            showerror(title="Peringatan",message="Kolom yang dibutuhkan tidak ditemukan!. \n\nKolom yang dibutuhkan adalah kolom 'Date' dan 'Close' ")  
                
class FormAbout(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.InitUI()
        
    def InitUI(self):
        self.frame1=Frame(self.parent)
        self.lbl1=Label(self.frame1,text="Dibuat oleh:")
        self.frame2=Frame(self.parent)
        self.lbl2=Label(self.frame2,text="5150411282 - Jagaddewa Vitagi")
        self.frame3=Frame(self.parent)
        self.lbl3=Label(self.frame3,text="Mahasiswa Informatika 2015 Universitas Teknologi Yogyakarta ")        
        self.frame4=Frame(self.parent)
        self.lbl4=Label(self.frame4,text="\n\nIkon yang digunakan pada aplikasi buatan dari Yusuke Kamiyamane \n(https://p.yusukekamiyamane.com/)")
        self.lbl1.pack(side=LEFT,padx=5,pady=5)  
        self.lbl2.pack(side=LEFT,padx=5)  
        self.lbl3.pack(side=LEFT,padx=5)  
        self.lbl4.pack(side=LEFT,padx=5)  
        self.frame1.pack(fill=X)
        self.frame2.pack(fill=X)
        self.frame3.pack(fill=X)
        self.frame4.pack(fill=X)
        
class FormGuide(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.InitUI()
        
    def InitUI(self):
        self.frame1=Frame(self.parent)
        self.lbl1=Label(self.frame1,text="Panduan Penggunaan")
        self.frame2=Frame(self.parent)
        self.lbl2=Label(self.frame2,text="1. Klik 'Pilih File CSV' untuk memilih file CSV")
        self.frame3=Frame(self.parent)
        self.lbl3=Label(self.frame3,text="2. Tekan tombol 'Jalankan Program'. Bila pada proses membuka file CSV tidak ada kolom")        
        self.frame4=Frame(self.parent)
        self.lbl4=Label(self.frame4,text="yang dibutuhkan maka muncul pesan error, silakan pilih kembali file CSV dengan")        
        self.frame5=Frame(self.parent)
        self.lbl5=Label(self.frame5,text="kolom yang dibutuhkan. Dan tekan kembali tombol 'Jalankan Program'.")
        self.frame6=Frame(self.parent)
        self.lbl6=Label(self.frame6,text="3. Pada program terdapat 7 menu:")
        self.frame7=Frame(self.parent)
        self.lbl7=Label(self.frame7,text="a. Menu no.1 untuk menampilkan data dari file CSV.")
        self.frame8=Frame(self.parent)
        self.lbl8=Label(self.frame8,text="b. Menu no.2 untuk menambahkan data ke file CSV.")
        self.frame9=Frame(self.parent)
        self.lbl9=Label(self.frame9,text="c. Menu no.3 untuk meng-edit data dari file CSV.")
        self.frame10=Frame(self.parent)
        self.lbl10=Label(self.frame10,text="d. Menu no.4 untuk mencari data dari file CSV.")
        self.frame11=Frame(self.parent)
        self.lbl11=Label(self.frame11,text="e. Menu no.5 untuk menghapus data pada file CSV.")
        self.frame12=Frame(self.parent)
        self.lbl12=Label(self.frame12,text="f. Menu no.6 untuk masuk ke sub-menu metode WMA.")
        self.frame13=Frame(self.parent)
        self.lbl13=Label(self.frame13,text="g. Menu no.7 untuk keluar dari program.")
        self.frame14=Frame(self.parent)
        self.lbl14=Label(self.frame14,text="\n\nNB: Pada menu no.6 terdapat 2 sub-menu untuk menjalankan proses metode WMA \n(Weighted Moving Average)")
        self.frame15=Frame(self.parent)
        self.lbl15=Label(self.frame15,text="a. Pilih 1 untuk menjalankan metode WMA-3.")
        self.frame16=Frame(self.parent)
        self.lbl16=Label(self.frame16,text="b. Pilih 2 untuk menjalankan metode WMA-5.")
        self.lbl1.pack(side=LEFT,padx=5,pady=5)  
        self.lbl2.pack(side=LEFT,padx=5)  
        self.lbl3.pack(side=LEFT,padx=5)  
        self.lbl4.pack(side=LEFT,padx=5)  
        self.lbl5.pack(side=LEFT,padx=5)  
        self.lbl6.pack(side=LEFT,padx=5)  
        self.lbl7.pack(side=LEFT,padx=30)  
        self.lbl8.pack(side=LEFT,padx=30)  
        self.lbl9.pack(side=LEFT,padx=30)  
        self.lbl10.pack(side=LEFT,padx=30)  
        self.lbl11.pack(side=LEFT,padx=30)  
        self.lbl12.pack(side=LEFT,padx=30)  
        self.lbl13.pack(side=LEFT,padx=30)  
        self.lbl14.pack(side=LEFT,padx=5)  
        self.lbl15.pack(side=LEFT,padx=30)  
        self.lbl16.pack(side=LEFT,padx=30)  
        self.frame1.pack(fill=X)
        self.frame2.pack(fill=X)
        self.frame3.pack(fill=X)
        self.frame4.pack(fill=X)
        self.frame5.pack(fill=X)
        self.frame6.pack(fill=X)
        self.frame7.pack(fill=X)
        self.frame8.pack(fill=X)
        self.frame9.pack(fill=X)
        self.frame10.pack(fill=X)
        self.frame11.pack(fill=X)
        self.frame12.pack(fill=X)
        self.frame13.pack(fill=X)
        self.frame14.pack(fill=X)
        self.frame15.pack(fill=X)
        self.frame16.pack(fill=X)
                     
        
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear') 

def print_menu():
    clear_screen()
    print("-"*15,"Menu","-"*15)
    print("1. Tampil Data")
    print("2. Tambah Data")
    print("3. Ubah Data")
    print("4. Cari Data")
    print("5. Hapus Data")
    print("6. Proses/Olah Data")
    print("7. Keluar")
    print("-"*36)

def print_menu_olahdata():
    clear_screen()
    print("-"*15,"Menu","-"*15)
    print("1. Hitung jumlah dan rata2")
    print("2. Proses dengan metode WMA-3")
    print("3. Proses dengan metode WMA-5")
    print("4. Keluar")
    print("-"*36)

def back_to_menu():
    print()
    input("Tekan Enter untuk kembali") 
    
def on_close():
    close = askokcancel("Close", "Yakin mau keluar program?")
    if close:
        root.destroy()
        sys.exit(1)
    
def tambah_data():
    try:
        tgl=input("Masukkan tanggal: ")
        datetime.datetime.strptime(tgl,'%Y-%m-%d')
        if any(df['Date']==tgl):
            print("Tanggal yang sama telah ada di tabel")
            return tambah_data()
        else:
            try:
                hrg=int(input("Masukkan harga: "))
            except ValueError:
                print("Yang dimasukkan bukan angka.")
                return tambah_data()
            if hrg<0:
                print("Angka yang dimasukkan negatif")
                return tambah_data()
            else:    
                df.loc[len(df)]=[tgl,hrg]
                df.sort_values(by=['Date'],inplace=True)
                df.to_csv(fileName,index=False)
                print("Data sukses ditambahkan")
    except ValueError:
        print("Formatnya harus Tahun-bulan-tanggal")
        return tambah_data()        

def ubah_data():
    try:
        tgl=input("Masukkan tanggal: ")
        datetime.datetime.strptime(tgl,'%Y-%m-%d')
        
        inputan=df[df['Date'].str.contains(tgl)]
        
        if inputan.empty:
            print("Tidak boleh kosong")
            return ubah_data()
        else:
            print(inputan)
            try:
                harga=int(input("Masukkan harga: "))
            except ValueError:
                print("Bukan angka gan!")  
                return tgl_dan_harga()
            
            if harga<0:
                print("Negatif gan!")
                return ubah_data()
            else:
                df.loc[df['Date']==tgl,'Close']=harga
                df.to_csv(fileName,index=False)
                print("Data sukses diupdate.")   
    except ValueError:
        print("Formatnya harus Tahun-bulan-tanggal")
        return ubah_data()

def cari_data():
    cari=input("Masukkan kata kunci: ")
    
    hasil=df[df['Date'].str.contains(cari)]   
    
    if hasil.empty or cari=="":
        print("Data tidak ditemukan")
        return cari_data()
    else:            
        print(hasil)  
            

def hapus_data():
    try:
        input_tanggal=input("Masukkan tanggal yang akan dihapus: ")
        ########
        tanggal_pilihan=df['Date']==input_tanggal
        pilihan=df[tanggal_pilihan]
        if pilihan.empty or input_tanggal=="":
            print("Kosong gan!")
            return hapus_data()
        else:
            print("Tanggal pilihan:")
            print(pilihan)
            ########
            pilihan_hapus=input("Yakin mau dihapus?[y/n]: ")
            if pilihan_hapus=="Y" or pilihan_hapus=="y" :
                df.drop(df.index[tanggal_pilihan],inplace=True)
                df.reset_index(drop=True,inplace=True)
                df.index=range(len(df.index))
                df.to_csv(fileName,index=False)
                print("Data sukses dihapus.")                    
            elif pilihan_hapus=="N" or pilihan_hapus=="n":
                print()
                print("Data tidak dihapus!")
                print()
    except ValueError:
        return hapus_data()
    
def menus():
    loop1=True
    while loop1:
        print_menu()
        pilihan=input("Masukkan pilihan Anda[1-7]: ")
        
        if pilihan=="1":#Menampilkan data CSV
            clear_screen()
            print("="*30) 
            print("Data")
            print("="*30)  
            df.reset_index(drop=True,inplace=True)
            print(df)
            print("="*30)
            print()
            back_to_menu()
        elif pilihan=="2":#Menambah data baru
            clear_screen()
            print()
            print("=======================")
            print("Menambah data")
            print("=======================")
            print()       
            tambah_data()            
            back_to_menu()
        elif pilihan=="3":#Mengedit data
            clear_screen()
            print()
            print("=======================")
            print("Mengubah data")
            print("=======================")
            print()
            ubah_data()
            back_to_menu()                
        elif pilihan=="4":#Mencari data
            clear_screen()
            print()
            print("=======================")
            print("Mencari data")
            print("=======================")
            print()
            cari_data()         
            back_to_menu()        
        elif pilihan=="5":#Menghapus data
            clear_screen()
            print()
            print("=======================")
            print("Menghapus data")
            print("=======================")
            print()  
            hapus_data()            
            back_to_menu()        
        elif pilihan=="6":#Menu pengolahan data
            clear_screen()
            print("Menu olah data")
            loop2=True
            while loop2:
                print_menu_olahdata()
                data_yg_ada="Data yang ada: "
                pilihan2=input("Masukkan pilihan[1-4]: ")
                if pilihan2=="1": #Hitung rata-rata
                    clear_screen()
                    df_4=df.copy(deep=False)
                    print("{}{}\n".format(data_yg_ada,len(df_4)))
                    df_4_close=df_4[['Close']]
                    df_4_date=df_4[['Date']]
                    
                    jumlah_data=np.sum(df_4_close)
                    rata_rata=np.mean(df_4_close)
                    
                    rata_rata_desimal=np.around(rata_rata,decimals=6)
                    
                    print()
                    print(df_4)
                    print()
                    print("{}: {}".format("Jumlah Data",len(df_4)))
                    print("{}: {}{} ".format("Jumlah Harga","Rp.",jumlah_data))
                    print("{}: {}".format("Rata-rata",rata_rata_desimal))
                    
                    back_to_menu()
                    
                elif pilihan2=="2":#Metode WMA-3
                    clear_screen()
                    df_2=df.copy(deep=False)
                    print("{}{}\n".format(data_yg_ada,len(df_2)))
                    df_2_close=df_2[['Close']]
                    df_2_date=df_2[['Date']]
                    
                    input_data=int(input("Masukkan jumlah data tes: "))
                    if input_data>len(df_2):
                        print("Di luar jangkauan")
                        back_to_menu()
                        continue
                    elif input_data<=3:
                        print("Tidak memenuhi data uji minimum. Data latih harus lebih dari 3")
                        back_to_menu()
                        continue
                    else:    
                        proses_hitung=[]                    
                        wma3_train=df_2_close[0:input_data]
                        wma3_test=df_2_close[input_data:]
                        tanggal_train=df_2_date[0:input_data]
                        tanggal_test=df_2_date[input_data:]
                        ########                 
                        wma3_train['WMA3'] = wma3_train['Close'].rolling(window=3, center=False).apply(lambda x: np.sum(weights1*x)/sum_weights1, raw=True).shift(periods=1)
                        wma3_train['proses_hitung']= wma3_train['Close'].rolling(window=3, center=False).apply(lambda x: proses_hitung.append("(({}*{})+({}*{})+({}*{}))".format(x.iloc[0],w1,x.iloc[1],w2,x.iloc[2],w3)) or 0)
                        wma3_test['WMA3 Prediksi']=wma3_train['Close'].rolling(window=3, center=False).apply(lambda x: np.sum(weights1*x)/sum_weights1, raw=True).shift(periods=1).iloc[input_data-1]
                        ########
                        wma3_train.loc[2:, 'proses_hitung'] = proses_hitung
                        wma3=wma3_train['WMA3']
                        proses=wma3_train['proses_hitung'].shift(periods=1)
                        ########
                        wma3_train_table=pd.concat([tanggal_train,wma3_train['Close'],wma3,proses],axis=1)
                        ########
                        prediksi=wma3_test['WMA3 Prediksi']
                        ########
                        wma3_error=abs(prediksi-wma3_test['Close'])
                        wma3_error_kuadrat=abs(prediksi-wma3_test['Close'])**2
                        wma3_error_percentage=abs(((prediksi-wma3_test['Close'])/wma3_test['Close'])*100)
                        
                        mse=np.square(np.subtract(wma3_test['Close'],prediksi)).mean()
                        mae=np.mean(abs(prediksi-wma3_test['Close']))
                        mape=np.mean((abs(prediksi-wma3_test['Close'])/abs(wma3_test['Close']))*100)
                        
                        mse_desimal=np.around(mse,decimals=6)
                        mae_desimal=np.around(mae,decimals=6)
                        mape_desimal=np.around(mape,decimals=6)
                        
                        
                        wma3_test['persenan']="| (" + "(" + wma3_test['Close'].astype(str) + "-" + np.around(prediksi,decimals=2).astype(str) + ")/" + wma3_test['Close'].astype(str) +") | *100"
                        proses_persenan=wma3_test['persenan']
                        ########
                        wma3_test_table=pd.concat([tanggal_test,wma3_test['Close'],prediksi,wma3_error,wma3_error_kuadrat,proses_persenan,wma3_error_percentage],axis=1)
                        ########
                        judul_tabel_wma3_train=['Tanggal','Harga Faktual','Prediksi WMA-3','Proses Perhitungan Prediksi WMA-3']                       
                        judul_tabel_wma3_test=['Tanggal','Harga Faktual','Prediksi WMA-3','Error','Error^2','Proses Perhitungan Persentase Error','Persentase Error']                   
                        ########
                        wma3_train_table.columns=judul_tabel_wma3_train
                        wma3_test_table.columns=judul_tabel_wma3_test
                        ########
                        print()
                        print("==============================")
                        print("Data Training/Data Latih")
                        print("==============================")
                        print()
                        print(wma3_train_table)
                        print()
                        print("==============================")
                        print("Data Test/Data Uji")
                        print("==============================")
                        print()
                        print(wma3_test_table)
                        print()
                        print("Mean Squared Error (MSE): ", mse_desimal)
                        print("Mean Average Error (MAE): ", mae_desimal)
                        print("Mean Average Percentage Error (MAPE): ", mape_desimal ,"%")                          
                        df_2.reset_index()
                        back_to_menu()
                        
                elif pilihan2=="3":#Metode WMA-5
                    clear_screen()
                    df_3=df.copy(deep=False)
                    print("{}{}\n".format(data_yg_ada,len(df_3)))
                    df_3_close=df_3[['Close']]
                    df_3_date=df_3[['Date']]
                    input_data_2=int(input("Masukkan jumlah data tes: "))
                    
                    if input_data_2>len(df_3):
                        print("Di luar jangkauan")
                        back_to_menu()
                        continue                    
                    elif input_data_2<=5:
                        print("Tidak memenuhi data uji minimum. Data latih harus lebih dari 5")
                        back_to_menu()
                        continue                    
                    else:
                        proses_hitung_2=[]                    
                        wma5_train=df_3_close[0:input_data_2]
                        wma5_test=df_3_close[input_data_2:]
                        tanggal_train=df_3_date[0:input_data_2]
                        tanggal_test=df_3_date[input_data_2:]
                        
                        ########                 
                        wma5_train['WMA5'] = wma5_train['Close'].rolling(window=5, center=False).apply(lambda x: np.sum(weights2*x)/sum_weights2, raw=True).shift(periods=1)
                        wma5_train['proses_hitung']= wma5_train['Close'].rolling(window=5, center=False).apply(lambda x: proses_hitung_2.append("(({}*{})+({}*{})+({}*{})+({}*{})+({}*{}))".format(x.iloc[0],w4,x.iloc[1],w5,x.iloc[2],w6,x.iloc[3],w7,x.iloc[4],w8)) or 0)
                        wma5_test['WMA5 Prediksi']=wma5_train['Close'].rolling(window=5, center=False).apply(lambda x: np.sum(weights2*x)/sum_weights2, raw=True).shift(periods=1).iloc[input_data_2-1]
                        ########
                        wma5_train.loc[4:, 'proses_hitung_2'] = proses_hitung_2
                        wma5=wma5_train['WMA5']
                        proses=wma5_train['proses_hitung_2'].shift(periods=1)
                        ########
                        wma5_train_table=pd.concat([tanggal_train,wma5_train['Close'],wma5,proses],axis=1)
                        ########
                        prediksi=wma5_test['WMA5 Prediksi']
                        ########
                        wma5_error=abs(prediksi-wma5_test['Close'])
                        wma5_error_kuadrat=abs(prediksi-wma5_test['Close'])**2
                        wma5_error_percentage=abs(((prediksi-wma5_test['Close'])/wma5_test['Close'])*100)
                        
                        mse_2=np.square(np.subtract(wma5_test['Close'],prediksi)).mean()
                        mae_2=np.mean(abs(prediksi-wma5_test['Close']))
                        mape_2=np.mean((abs(prediksi-wma5_test['Close'])/abs(wma5_test['Close']))*100)
                        
                        mse_2_desimal=np.around(mse_2,decimals=6)
                        mae_2_desimal=np.around(mae_2,decimals=6)
                        mape_2_desimal=np.around(mape_2,decimals=6)
                        
                        wma5_test['persenan']="| (" + "(" + wma5_test['Close'].astype(str) + "-" + np.around(prediksi,decimals=2).astype(str) + ")/" + wma5_test['Close'].astype(str) +") | *100"
                        proses_persenan_2=wma5_test['persenan']
                        ########
                        wma5_test_table=pd.concat([tanggal_test,wma5_test['Close'],prediksi,wma5_error,wma5_error_kuadrat,proses_persenan_2,wma5_error_percentage],axis=1)
                        ########
                        judul_tabel_wma5_train=['Tanggal','Harga Faktual','Prediksi WMA-5','Proses Perhitungan Prediksi WMA-5']                       
                        judul_tabel_wma5_test=['Tanggal','Harga Faktual','Prediksi WMA-5','Error','Error^2','Proses Perhitungan Persentase Error','Persentase Error']                   
                        ########
                        wma5_train_table.columns=judul_tabel_wma5_train
                        wma5_test_table.columns=judul_tabel_wma5_test
                        ########
                        print()
                        print("==============================")
                        print("Data Training/Data Latih")
                        print("==============================")
                        print()                        
                        print(wma5_train_table)
                        print()
                        print("==============================")
                        print("Data Test/Data Uji")
                        print("==============================")
                        print()                        
                        print(wma5_test_table)
                        print()
                        print("Mean Squared Error (MSE): ", mse_2_desimal)
                        print("Mean Average Error (MAE): ", mae_2_desimal)
                        print("Mean Average Percentage Error (MAPE): ", mape_2_desimal ,"%")                          
                        df_3.reset_index()
                        back_to_menu()                                   
                elif pilihan2=="4":   
                    clear_screen()
                    print("Terima kasih sudah menjalankan proses.")
                    loop2=False               
                    back_to_menu()
                else:
                    print("Anda tidak memilih")      
                    back_to_menu()                
        elif pilihan=="7":
            print("Anda keluar dari program")
            loop1=False
            sys.exit(1)
            break
        else:
            print("Anda tidak memilih")      
            back_to_menu()          

if __name__=='__main__':
    root=Tk()
    ikon_buka_file=PhotoImage(file=r"folder-open-document-text.png")
    ikon_info=PhotoImage(file=r"information-button.png")
    ikon_guide=PhotoImage(file=r"book-question.png")
    ikon_buka_program=PhotoImage(file=r"notebook--arrow.png")
    app=FormUtama(root)
    ##Supaya command linenya langsung maximize begitu dibuka##
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMISE = 3
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMISE)
    ##Supaya formnya di tengah##
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws/2) - (w/2))
    y = int((hs/3) - (h/2))
    ####
    root.geometry("480x160+{}+{}".format(x,y))
    root.title("Prediksi Harga Saham Menggunakan Metode WMA")
    root.resizable(False,False)
    root.protocol("WM_DELETE_WINDOW",  on_close)
    root.mainloop()
    menus()    
