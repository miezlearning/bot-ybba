# Introduction

Seperti biasa, saya akan memperkenalkan program ini tentang apa untuk memastikan kalian paham alur dari programnya. 

**Forum Announcer Bot**

Forum Announcer Bot adalah sebuah bot Discord yang secara otomatis memberikan pengumuman di channel tertentu ketika ada thread baru yang dibuat atau dihapus di kategori tertentu. Bot ini juga memiliki fitur untuk memberikan tanggapan acak ketika disebutkan/mention di channel.


# Fitur Unggulan

Seperti yang disebutkan sebelumnya kami memiliki beberapa fitur; *pengumuman post baru, post dihapus, respon acak*.

- **Pengumuman Post Baru** 🆕

Fitur ini akan mengirim pesan di channel yang kalian tentukan dengan embed message yang sangat informatif.

[Letak_SS]

- **Pengumuman Post Dihapus** ⛔

Jadi, ketika ada salah satu post yang dihapus. Embed sebelumnya akan di edit atau di ubah, bagian yang menariknya adalah deskripsi postnya akan di enkripsi dengan tipe AES 25 dengan 32 Bit. 

Nah, kalau kalian ingin dekripsi atau membuka kunci enkripsinya pakai saja file `dekripsi.py`.

[Letak_SS]

- **Respon Bot Acak** 😊

Ketika kamu mention/sebut nama botnya, maka akan ada tanggapan random dari botnya 😅.

[Letak_SS]

# Cara Pakai

**Perlu disimak dengan baik**! karena akan ada sedikit bagian yang membuat bingung bagi orang awam.

1. Kalian harus membuat application-nya terlebih dahulu [*disini*](https://discord.com/developers/applications)
2. Klik Tombol **New Application** dikanan pojok atas.
3. Masukkan *Nama Application*, dan *klik tombol kotak*.
4. Klik Tombol **Create**
5. Selanjutnya, kalian ke bagian **Bot** (beri nama bot jika perlu dan avatarnya)
6. Simpan tokennya terlebih dahulu dengan cara tekan tombol **Reset Token**.
7. Nyalakan, beberapa ketentuannya seperti di screenshot bawah

[Letak SS]

8. Invite Bot, Copy link dan sesuaikan dengan ID bot yang kalian punya (lihatnya di **General Information**).

`https://discord.com/oauth2/authorize?client_id=ID_BOTNYA_DISINI&scope=bot&permissions=8`

9. Buka **Visual Studio Code** , dan bukan terminal baru ketikkan ini `pip install -r requirements.txt`
    
10. jalankan filenya menggunakan python([cara run file python](https://jagongoding.com/python/vscode-untuk-python/)).

Jika sudah seharusnya seperti ini :

[Letak_SS]