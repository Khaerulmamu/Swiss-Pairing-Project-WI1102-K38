# Program SwissPairing_v2
# Sistem Swiss pairing untuk N tim (N = 2, 4, 8, 16, ...). Banyak ronde R
# dihitung otomatis dari N: R = log basis 2 dari N (2 tim -> 1 ronde,
# 4 -> 2, 8 -> 3, 16 -> 4, 32 -> 5, ...).
# Aturan/fitur bebas lah mau dipanggil apa sudah sesuai kesepakatan:
#   - Hasil pertandingan hanya menang atau kalah (tidak ada seri)
#   - Setiap tim punya kekuatan rahasia (50 s.d. 100). Peluang tim A menang
#     melawan tim B = kekuatanA / (kekuatanA + kekuatanB), sehingga tim yang
#     lebih kuat lebih berpeluang menang, tetapi upset tetap mungkin terjadi
#   - Kekuatan tim dan hasil pertandingan ditentukan secara acak dengan
#     fungsi random (library random)
#   - Peringkat: jumlah kemenangan terbanyak; jika sama, dilihat nilai Buchholz
#     (jumlah kemenangan seluruh lawan yang pernah dihadapi); jika masih sama,
#     urutan pendaftaran yang lebih awal didahulukan
#   - Pairing tiap ronde: tim peringkat teratas yang belum dapat lawan
#     dipasangkan dengan tim di bawahnya yang belum dapat lawan dan belum
#     pernah bertemu. Jika tidak ada, dipasangkan dengan tim berikutnya yang
#     belum dapat lawan
#   - Setelah semua ronde, setengah dari total tim (peringkat teratas) lolos
# Catatan: pairing bersifat greedy (tanpa backtracking), sehingga pertemuan ulang
# masih mungkin terjadi, tetapi jarang karena R jauh lebih kecil daripada N-1.

import random

# KAMUS
# N, R, lolos : int                       : banyak tim, banyak ronde (hasil hitung_ronde), banyak tim lolos
# nama : array [0..N-1] of string         : nama tim
# kekuatan : array [0..N-1] of int        : kekuatan rahasia tim
# skor : array [0..N-1] of int            : jumlah kemenangan tim
# bh : array [0..N-1] of int              : nilai Buchholz tim
# urutan : array [0..N-1] of int          : nomor tim, terurut berdasarkan peringkat
# dipasang : array [0..N-1] of int        : 1 jika tim sudah dapat lawan di ronde ini
# sudah_main : array [0..N*N-1] of int    : sudah_main[a*N+b] = 1 jika a pernah melawan b
# match1, match2 : array [0..N-1] of int  : pasangan tim tiap match di ronde ini
# banyak_match : int                      : banyak match di ronde ini
# r, i, p, q, m, a, b : int

# Definisi Fungsi pangkat_dua
def pangkat_dua(N):
    # Menghasilkan True jika N adalah 2, 4, 8, 16, ... (pangkat dua, N >= 2)

    # KAMUS LOKAL
    # x : int

    # ALGORITMA
    x = 1
    while (x < N):
        x = x * 2
    # x >= N
    if (x == N and N >= 2):
        return True
    else:
        return False

# Definisi Fungsi hitung_ronde
def hitung_ronde(N):
    # Menghasilkan banyak ronde Swiss untuk N tim (N pangkat dua),
    # yaitu pangkat dua yang menghasilkan N: 2 -> 1, 4 -> 2, 8 -> 3, 16 -> 4, ...
    # (log basis 2 dari N)

    # KAMUS LOKAL
    # x, ronde : int

    # ALGORITMA
    x = 1
    ronde = 0
    while (x < N):
        x = x * 2
        ronde = ronde + 1
    # x >= N
    return ronde

# Definisi Fungsi TimAMenang
def TimAMenang(kA, kB):
    # Menghasilkan True jika tim A (kekuatan kA) menang melawan tim B
    # (kekuatan kB). Peluang A menang = kA / (kA + kB)

    # KAMUS LOKAL
    # titik : int

    # ALGORITMA
    titik = random.randint(1, kA + kB)    # bilangan acak 1 s.d. kA+kB
    if (titik <= kA):
        return True
    else:
        return False

# Definisi Prosedur hitung_buccholz
def hitung_buccholz(skor, sudah_main, bh, N):
    # Mengisi bh[a] dengan jumlah kemenangan semua lawan yang pernah dihadapi tim a

    # KAMUS LOKAL
    # a, b : int

    # ALGORITMA
    for a in range(0, N):
        bh[a] = 0
        for b in range(0, N):
            if (sudah_main[a*N+b] == 1):
                bh[a] = bh[a] + skor[b]
    return

# Definisi Prosedur urutan_peringkat
def urutan_peringkat(skor, bh, urutan, N):
    # Mengisi array urutan dengan nomor tim terurut dari peringkat terbaik
    # (kemenangan terbanyak, lalu Buchholz terbesar, lalu pendaftaran terawal)

    # KAMUS LOKAL
    # i, j, temp : int

    # ALGORITMA
    for i in range(0, N):
        urutan[i] = i
    for i in range(0, N-1):
        for j in range(0, N-1-i):
            if (skor[urutan[j]] < skor[urutan[j+1]] or (skor[urutan[j]] == skor[urutan[j+1]] and bh[urutan[j]] < bh[urutan[j+1]])):
                temp = urutan[j]
                urutan[j] = urutan[j+1]
                urutan[j+1] = temp
    return

# Definisi Fungsi CariLawan
def CariLawan(urutan, dipasang, sudah_main, N, p, lawan_cocok):
    # Menghasilkan posisi (di array urutan) lawan untuk tim di posisi p,
    # yaitu tim di bawah posisi p yang belum dapat lawan.
    # Jika lawan_cocok = False, lawan juga harus belum pernah bertemu.
    # Menghasilkan -1 jika tidak ada lawan yang cocok.

    # KAMUS LOKAL
    # a, b, q : int
    # found : bool

    # ALGORITMA
    a = urutan[p]
    q = p + 1
    found = False
    while (q < N and found == False):
        b = urutan[q]
        if (dipasang[b] == 0 and (lawan_cocok == True or sudah_main[a*N+b] == 0)):
            found = True
        else:
            q = q + 1
    # q = N atau found = True
    if (found == True):
        return q
    else:
        return -1

# Definisi Prosedur klasemen
def klasemen(nama, skor, bh, urutan, N, ronde):
    # Mencetak peringkat, nama, rekor menang-kalah, dan Buchholz semua tim

    # KAMUS LOKAL
    # i, a : int

    # ALGORITMA
    for i in range(0, N):
        a = urutan[i]
        print(str(i+1) + ". " + nama[a] + "  " + str(skor[a]) + "-" + str(ronde - skor[a]) + "  (Buchholz " + str(bh[a]) + ")")
    return

# Definisi Prosedur CetakHasilAkhir
def CetakHasilAkhir(nama, skor, bh, urutan, N, ronde, lolos):
    # Mencetak klasemen akhir beserta status lolos / tersisih tiap tim

    # KAMUS LOKAL
    # i, a : int
    # status : string

    # ALGORITMA
    for i in range(0, N):
        a = urutan[i]
        if (i < lolos):
            status = "LOLOS"
        else:
            status = "TERSISIH"
        print(str(i+1) + ". " + nama[a] + "  " + str(skor[a]) + "-" + str(ronde - skor[a]) + "  (Buchholz " + str(bh[a]) + ")  " + status)
    return

# Definisi Fungsi NamaSudahAda
def NamaSudahAda(nama, n, kandidat):
    # Menghasilkan True jika kandidat sama dengan salah satu nama
    # pada nama[0..n-1]

    # KAMUS LOKAL
    # i : int
    # found : bool

    # ALGORITMA
    i = 0
    found = False
    while (i < n and found == False):
        if (nama[i] == kandidat):
            found = True
        else:
            i = i + 1
    # i = n atau found = True
    return found

# Definisi Prosedur IsiNamaTim
def IsiNamaTim(nama, N):
    # Membaca nama N tim dari keyboard dan menyimpannya di array nama.
    # Nama tidak boleh kosong dan tidak boleh sama dengan nama tim lain;
    # jika tidak valid, masukan diulang.

    # KAMUS LOKAL
    # i : int
    # kandidat : string

    # ALGORITMA
    for i in range(0, N):
        valid = False
        while not valid:
            kandidat = input("Nama tim ke-" + str(i+1) + ": ")
            if kandidat == '':
                print("Nama tim tidak boleh kosong, coba lagi!")
            elif NamaSudahAda(nama, i, kandidat):
                print("Nama tim sudah dipakai tim lain, coba lagi!")
            else:
                valid = True
        nama[i] = kandidat

# ALGORITMA PROGRAM UTAMA

# Membaca banyak tim (pangkat dua: 2, 4, 8, 16, ...)
N = int(input("Jumlah tim (2, 4, 8, 16, ...): "))
while not pangkat_dua(N):
    print("Jumlah tim harus pangkat dua (2, 4, 8, 16, ...), coba lagi!")
    N = int(input("Jumlah tim (2, 4, 8, 16, ...): "))

# Banyak ronde dihitung otomatis dari banyak tim
R = hitung_ronde(N)
print("Jumlah ronde : " + str(R))

# Deklarasi array
nama = ['' for i in range(N)]
kekuatan = [0 for i in range(N)]
skor = [0 for i in range(N)]
bh = [0 for i in range(N)]
urutan = [0 for i in range(N)]
dipasang = [0 for i in range(N)]
sudah_main = [0 for i in range(N*N)]
match1 = [0 for i in range(N)]
match2 = [0 for i in range(N)]

# Mengisi nama tim (dengan validasi), lalu menentukan kekuatan rahasia (50 s.d. 100)
IsiNamaTim(nama, N)
for i in range(0, N):
    kekuatan[i] = random.randint(50, 100)

# Pemrosesan tiap ronde
for r in range(1, R+1):
    print("")
    print("=== RONDE " + str(r) + " ===")

    # Mengurutkan tim berdasarkan peringkat
    hitung_buccholz(skor, sudah_main, bh, N)
    urutan_peringkat(skor, bh, urutan, N)

    # Mengosongkan penanda tim yang sudah dapat lawan
    for i in range(0, N):
        dipasang[i] = 0
    banyak_match = 0

    # Pairing: dari peringkat teratas ke bawah
    for p in range(0, N):
        a = urutan[p]
        if (dipasang[a] == 0):
            q = CariLawan(urutan, dipasang, sudah_main, N, p, False)
            if (q == -1):
                q = CariLawan(urutan, dipasang, sudah_main, N, p, True)
            b = urutan[q]
            dipasang[a] = 1
            dipasang[b] = 1
            sudah_main[a*N+b] = 1
            sudah_main[b*N+a] = 1
            match1[banyak_match] = a
            match2[banyak_match] = b
            banyak_match = banyak_match + 1

    # Mensimulasikan tiap pertandingan
    for m in range(0, banyak_match):
        a = match1[m]
        b = match2[m]
        if (TimAMenang(kekuatan[a], kekuatan[b]) == True):
            skor[a] = skor[a] + 1
            print("Match " + str(m+1) + ": " + nama[a] + " vs " + nama[b] + "  -> pemenang: " + nama[a])
        else:
            skor[b] = skor[b] + 1
            print("Match " + str(m+1) + ": " + nama[a] + " vs " + nama[b] + "  -> pemenang: " + nama[b])

    # Klasemen sementara
    print("")
    print("Klasemen setelah ronde " + str(r) + ":")
    hitung_buccholz(skor, sudah_main, bh, N)
    urutan_peringkat(skor, bh, urutan, N)
    klasemen(nama, skor, bh, urutan, N, r)

# Hasil akhir: setengah dari total tim lolos
lolos = int(N/2)
print("")
print("HASIL AKHIR (" + str(lolos) + " dari " + str(N) + " tim lolos)")
CetakHasilAkhir(nama, skor, bh, urutan, N, R, lolos)
