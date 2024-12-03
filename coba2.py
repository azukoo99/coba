import csv
import pandas as pd
from tabulate import tabulate
import os


def login():
    os.system('cls')
    teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

    print(teks)
    print ("=================================[LOGIN]=================================")


    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    user = []
    with open('user.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            user.append({'username': row[0], 'password': row[1], 'role': row[2]})

    for i in user:
        if i['username'] == username and i['password'] == password:
            if i['role'] == 'owner': 
                print("Selamat datang, owner!")
                input("Klik Enter untuk melanjutkan...")
                menu_owner(username)
            else:
                print(f"Selamat datang, {i['username']}!")
                input("Klik Enter untuk melanjutkan...")
                menu_kasir(username)
            return username

    print("Username atau password salah!")    
    input("Klik Enter untuk melanjutkan...")
    return login()

def kelola_produk(role, username):
    os.system('cls')
    data_produk = pd.read_csv('produk.csv')
    data_produk.index += 1
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    print("Kelola Produk")
    print("1. Tambah Produk")
    print("2. Hapus Produk")
    print("3. Update Produk")
    print("4. Keluar")

    pilihan = input("Masukan jawaban Anda: ")
    if pilihan == "1":
        os.system('cls')
        tambah_produk(data_produk)
    elif pilihan == "2":
        os.system('cls')
        hapus_produk(data_produk)
    elif pilihan == "3":
        os.system('cls')
        update_produk(data_produk)
    elif pilihan == "4":
        os.system('cls')
        if role == "owner":
            menu_owner(username)
        else:
            menu_kasir(username)
    else:
        input("Masukan input yang benar, tekan Enter untuk lanjut")
        kelola_produk(role, username)

def tambah_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    nama_produk = input("Masukan nama produk: ")
    stok_produk = input("Masukan stok produk: ")
    harga_produk = input("Masukan harga produk: ")
    keuntungan_produk = input("Masukan keuntungan produk: ")
    menambahkan_produk = pd.DataFrame({"produk": [nama_produk], "stok(kg)": [stok_produk], "harga": [harga_produk], "keuntungan": [keuntungan_produk]})
    data_produk = data_produk._append(menambahkan_produk)
    data_produk.to_csv('produk.csv', index=False)
    print("Produk berhasil ditambahkan")
    input("Klik Enter untuk melanjutkan...")

def hapus_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    index_produk = int(input("Masukan index produk: ")) 
    if 0 <= index_produk < len(data_produk)+1:
        data_produk = data_produk.drop(index=index_produk)
        data_produk.to_csv('produk.csv', index=False)
        print("Produk berhasil dihapus")
    else:
        print("Index tidak valid!")
    input("Klik Enter untuk melanjutkan...")

def update_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    index_produk = int(input("Masukan index produk: ")) 
    if 0 <= index_produk < len(data_produk)+1:
        nama_produk = input("Masukan nama produk: ")
        stok_produk = input("Masukan stok produk: ")
        harga_produk = input("Masukan harga produk: ")
        keuntungan_produk = input("Masukan keuntungan produk: ")
        data_produk.at[index_produk, "produk"] = nama_produk
        data_produk.at[index_produk, "stok(kg)"] = float(stok_produk)
        data_produk.at[index_produk, "harga"] = float(harga_produk)
        data_produk.at[index_produk, "keuntungan"] = float(keuntungan_produk)

        data_produk.to_csv('produk.csv', index=False)
        print("Produk berhasil diubah")
    else:
        print("Index tidak valid!")
    input("Klik Enter untuk melanjutkan...")

def catatan_penjualan(username):
    os.system('cls')
    produk = pd.read_csv('produk.csv')
    penjualan = pd.read_csv('penjualan.csv')

    tampilkan_produk = produk.copy()
    tampilkan_produk.index += 1
    print("\nDaftar Produk Tersedia:")
    kolom_tertentu = tampilkan_produk[['produk', 'stok(kg)', 'harga']]
    print(tabulate(kolom_tertentu, headers='keys', tablefmt='fancy_grid'))


    while True:
        try:
            jumlah_jenis = int(input("\nBerapa jenis produk yang ingin dibeli: "))
            if jumlah_jenis <= 0:
                print("Masukkan angka lebih besar dari 0!")
            elif len(produk)+1 <= jumlah_jenis:
                print("Jumlah jenis barang yang ingin dibeli melebihi jumlah produk kami")
                continue
            break
        except ValueError:
            print("Input tidak valid! Masukkan angka.")
    
    keranjang = []
    total_belanja = 0
    total_keuntungan = 0
    
    for i in range(jumlah_jenis):
        print(f"\nPembelian ke-{i+1}")

        while True:
            try:
                nomor_produk = int(input("Masukkan nomor produk: ")) -1
                if nomor_produk < 0 or nomor_produk >= len(produk):
                    print("Nomor produk tidak valid!")
                    continue
                
                jumlah = float(input("Masukkan jumlah (kg): "))
                if jumlah <= 0:
                    print("Jumlah harus lebih besar dari 0!")
                    continue
                
                stok = float(produk.iloc[nomor_produk]['stok(kg)'])
                if jumlah > stok:
                    print(f"Stok tidak cukup! Stok tersedia: {stok} kg")
                    continue
                
                nama = produk.iloc[nomor_produk]['produk']
                harga = float(produk.iloc[nomor_produk]['harga'])
                keuntungan_per_kg = float(produk.iloc[nomor_produk]['keuntungan'])
                subtotal = jumlah * harga
                subtotal_keuntungan = jumlah * keuntungan_per_kg

                keranjang.append({
                    'produk': nama, 
                    'jumlah': jumlah, 
                    'harga': harga, 
                    'subtotal': subtotal,
                    'keuntungan': subtotal_keuntungan
                })
                total_belanja += subtotal
                total_keuntungan += subtotal_keuntungan

                produk.at[nomor_produk, 'stok(kg)'] = stok - jumlah
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka.")
    
    print("\n=== STRUK PEMBELIAN ===")
    print(f"Kasir: {username}")  
    for i in keranjang:
        print(f"\nProduk: {i['produk']}")
        print(f"Jumlah: {i['jumlah']} kg")
        print(f"Harga: Rp {i['harga']:,.0f}/kg")
        print(f"Subtotal: Rp {i['subtotal']:,.0f}")
    print(f"\nTotal Pembelian: Rp {total_belanja:,.0f}")
    
    for i in keranjang:
        new_row = pd.DataFrame({
            'tanggal': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")],
            'produk': [i['produk']],
            'jumlah': [i['jumlah']],
            'harga': [i['harga']], 
            'total': [i['subtotal']],
            'keuntungan': [i['keuntungan']]
        })
        penjualan = pd.concat([penjualan, new_row], ignore_index=True)

    penjualan.to_csv('penjualan.csv', index=False)
    produk.to_csv('produk.csv', index=False)
    
    input("\nTekan Enter untuk kembali ke menu utama...")

def laporan_keseluruhan():
    os.system('cls')
    penjualan = pd.read_csv('penjualan.csv')
    total_keuntungan = penjualan['keuntungan'].sum()
    print("\n=== Laporan Keseluruhan ===")
    print(f"Total Keuntungan: Rp {total_keuntungan:,.0f}")
    input("\nTekan Enter untuk kembali...")


def kelola_akun_kasir():
    os.system('cls')
    print("=== Kelola Akun Kasir ===")
    print("1. Tambah Akun Kasir")
    print("2. Hapus Akun Kasir")
    print("3. Kembali")

    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == '1':
        os.system('cls')
        tambah_akun_kasir()
    elif pilihan == '2':
        os.system('cls')
        hapus_akun_kasir()
    elif pilihan == '3':
        os.system('cls')
        return
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter untuk melanjutkan...")
        kelola_akun_kasir()

def tambah_akun_kasir():
    os.system('cls')
    print("=== Tambah Akun Kasir ===")
    username = input("Masukkan Username Kasir: ")
    password = input("Masukkan Password Kasir: ")
    role = 'kasir'
    akun_kasir = pd.read_csv('user.csv')

    if username in akun_kasir['username'].values:
        print("Username sudah ada!") 
    else:
        menambahkan_akun = pd.DataFrame({"username": [username], "password": [password], "role": [role]})
        akun_kasir = akun_kasir._append(menambahkan_akun)
        akun_kasir.to_csv('user.csv', index=False)
        print("Akun berhasil ditambahkan")
        input("Klik Enter untuk melanjutkan...")

def hapus_akun_kasir():
    os.system('cls')
    akun_kasir = pd.read_csv('user.csv')
    akun_kasir.index += 1
    print(tabulate(akun_kasir, headers='keys', tablefmt='fancy_grid'))
    
    while True:
        try:
            index_hapus = int(input("Masukkan index akun yang akan dihapus: "))
            if 0 <= index_hapus < len(akun_kasir)+1:
                akun_kasir = akun_kasir.drop(index=index_hapus).reset_index(drop=True)
                akun_kasir.to_csv('user.csv', index=False)
                print("Akun kasir berhasil dihapus!")
                break
            else:
                print("Index tidak valid!")
    
        except ValueError:
            print("Input tidak valid! Masukkan angka.")

            

            
    input("Tekan Enter untuk melanjutkan...")


def laporan_keuntungan():
    while True:
        os.system('cls')
        print("=== LAPORAN KEUNTUNGAN ===")
        print("1. Laporan Per Produk")
        print("2. Laporan Per Periode")
        print("3. Laporan Keseluruhan")
        print("4. Kembali")
        
        pilihan = input("Pilih menu (1/2/3/4): ")
        
        if pilihan == '1':
            os.system('cls')
            penjualan = pd.read_csv('penjualan.csv')
            laporan = penjualan.groupby('produk').agg({
                'jumlah': 'sum',
                'keuntungan': 'sum'
            }).reset_index()
            print("\nLaporan Keuntungan Per Produk:")
            laporan.index += 1
            print(tabulate(laporan, headers='keys', tablefmt='fancy_grid'))
            
            
        elif pilihan == '2':
            os.system('cls')
            penjualan = pd.read_csv('penjualan.csv')
            penjualan['tanggal'] = pd.to_datetime(penjualan['tanggal'])
            
# Custom Periode
            while True:
                try:
                    print("\nMasukkan tanggal dalam format DD-MM-YYYY")
                    start_str = input("Tanggal Awal: ")
                    end_str = input("Tanggal Akhir: ")
                        
                    start_date = pd.to_datetime(start_str, format='%d-%m-%Y')
                    end_date = pd.to_datetime(end_str, format='%d-%m-%Y') + pd.Timedelta(days=1)
                        
                    if start_date > end_date:
                        print("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
                        continue
                        
                    period_name = f"Periode {start_str} s/d {end_str}"
                    break
                except ValueError:
                    print("Format tanggal salah! Gunakan format DD-MM-YYYY")
            
            # Filter data berdasarkan periode
            filtered = penjualan[
                (penjualan['tanggal'] >= start_date) & 
                (penjualan['tanggal'] < end_date)
            ]
            
            # Grouping per hari
            laporan = filtered.groupby(filtered['tanggal'].dt.date).agg({
                'keuntungan': 'sum'
            }).reset_index()
            laporan.index += 1
            
            print(f"\nLaporan Keuntungan {period_name}:")
            if len(laporan) > 0:
                print(tabulate(laporan, headers='keys', tablefmt='fancy_grid'))
                print(f"Total Keuntungan: Rp {laporan['keuntungan'].sum():,.0f}")
            else:
                print("Tidak ada transaksi pada periode tersebut")
            
        elif pilihan == '3':
            os.system('cls')
            penjualan = pd.read_csv('penjualan.csv')
            total_keuntungan = penjualan['keuntungan'].sum()
            total_transaksi = len(penjualan)
            
            print("\nRekapitulasi Keseluruhan:")
            print(f"Total Transaksi: {total_transaksi}")
            print(f"Total Keuntungan: Rp {total_keuntungan:,.0f}")
            
        elif pilihan == '4':
            break
            
        input("\nTekan Enter untuk melanjutkan...")
        os.system('cls')
def logout():
    os.system('cls')
    input ("Anda telah logout. Sampai jumpa!")
    os.system('cls')
    exit()

def menu_kasir(username):
    while True:
        os.system('cls')
        teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

        print(teks)

        print(f"===================== MENU UTAMA (Kasir: {username}) =====================")
        print("1. Kelola Produk")
        print("2. Catat Penjualan")
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            os.system('cls')
            kelola_produk("kasir", username)
        elif pilihan == '2':
            os.system('cls')
            catatan_penjualan(username)
        elif pilihan == '3':
            os.system('cls')
            logout()
        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")

def menu_owner(username):
    while True:
        os.system('cls')
        teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

        print(teks)

        print(f"===================== MENU UTAMA (Owner: {username}) =====================")
        print("1. Kelola Produk")
        print("2. Catat Penjualan")
        print("3. Laporan Keuntungan")
        print("4. Kelola Akun Kasir")
        print("5. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5): ")

        if pilihan == '1':
            os.system('cls')
            kelola_produk("owner", username)
        elif pilihan == '2':
            os.system('cls')
            catatan_penjualan(username)
        elif pilihan == '3':
            os.system('cls')
            laporan_keuntungan()
        elif pilihan == '4':
            os.system('cls')
            kelola_akun_kasir()
        elif pilihan == '5':
            os.system('cls')
            logout()
        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")

login()
