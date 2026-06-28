import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# --- FONKSİYONLAR ---

def dosya_sec():
    dosya = filedialog.askopenfilename(
        title="Anka - Kalıp Seç", 
        filetypes=[("ISO/IMG Dosyaları", "*.iso *.img"), ("Tüm Dosyalar", "*.*")]
    )
    if dosya:
        dosya_adi = os.path.basename(dosya)
        etiket_dosya.config(text=f"🗂 {dosya_adi}", fg="#ffffff")
        etiket_tam_yol.config(text=dosya)

def suruculeri_tara():
    try:
        # Sessizce sadece USB'leri (çıkarılabilir diskleri) bulur
        komut = "lsblk -dno NAME,SIZE,MODEL,RM | grep ' 1$'"
        usb_listesi = os.popen(komut).read().splitlines()
        
        temiz_liste = []
        for cihaz in usb_listesi:
            temiz_liste.append(f"🖴 {cihaz[:-2].strip()}")
            
        usb_menu['values'] = temiz_liste
        if temiz_liste:
            usb_menu.current(0)
        else:
            usb_menu.set("Uygun USB bulunamadı")
    except:
        usb_menu.set("Tarama hatası!")

def yazdirma_baslat():
    iso_yolu = etiket_tam_yol.cget("text")
    secili_usb = usb_menu.get()
    
    if iso_yolu == "" or "🖴" not in secili_usb:
        messagebox.showwarning("Anka Flasher", "Dosya ve USB seçimi yapmalısın!")
        return

    emin_misin = messagebox.askyesno("KRİTİK UYARI", "USB'deki tüm veriler silinecek! Devam edilsin mi?")
    
    if emin_misin:
        usb_device = "/dev/" + secili_usb.replace("🖴 ", "").split()[0]
        mod = mod_menu.get()
        
        # Seçilen moda göre teknik parametreleri ayarla
        if "DD Modu" in mod:
            parametre = "bs=4M status=progress conv=fdatasync"
        elif "GNU/Linux" in mod:
            parametre = "bs=1M status=progress conv=fsync"
        else:
            parametre = "bs=4M status=progress"

        messagebox.showinfo("AnkaOS", "Yazdırma başlıyor. Terminale şifreni gir.")
        os.system(f"sudo dd if='{iso_yolu}' of={usb_device} {parametre}")
        messagebox.showinfo("Başarılı", "Yazma işlemi tamamlandı!")

# --- TASARIM (v1.0 ASİL TEMA) ---

bg_koyu = "#0d0d0d"    
panel_koyu = "#161616" 
asil_kirmizi = "#9a0000" 
beyaz = "#ffffff"

pencere = tk.Tk()
pencere.title("Anka Flasher v1.0")
pencere.geometry("480x650")
pencere.configure(bg=bg_koyu)

# Combobox Stil Ayarı
style = ttk.Style()
style.theme_use('default')
style.configure("TCombobox", fieldbackground=panel_koyu, background="#333333", foreground=beyaz, arrowcolor=asil_kirmizi)

# Üst Şerit
tk.Frame(pencere, bg=asil_kirmizi, height=5).pack(fill="x")

# Başlık
tk.Label(pencere, text="ANKA FLASHER v1.0", font=("Helvetica", 24, "bold"), bg=bg_koyu, fg=asil_kirmizi).pack(pady=30)

# Ana Panel
ana_panel = tk.Frame(pencere, bg=panel_koyu, padx=25, pady=20, highlightbackground=asil_kirmizi, highlightthickness=1)
ana_panel.pack(padx=20, pady=10, fill="both", expand=True)

# 1. DOSYA SEÇİMİ
tk.Label(ana_panel, text="1. KAYNAK KALIP", font=("Arial", 10, "bold"), bg=panel_koyu, fg=asil_kirmizi).pack(anchor="w")
etiket_dosya = tk.Label(ana_panel, text="Dosya seçilmedi", bg=panel_koyu, fg="#888888", font=("Arial", 9))
etiket_dosya.pack(pady=10, anchor="w")
etiket_tam_yol = tk.Label(pencere, text="") 
tk.Button(ana_panel, text="KALIP DOSYASI SEÇ", command=dosya_sec, bg="#333333", fg=beyaz, relief="flat", width=22).pack(anchor="w")

tk.Frame(ana_panel, height=1, bg="#222222").pack(fill="x", pady=20)

# 2. USB SEÇİMİ
tk.Label(ana_panel, text="2. HEDEF SÜRÜCÜ", font=("Arial", 10, "bold"), bg=panel_koyu, fg=asil_kirmizi).pack(anchor="w")
usb_menu = ttk.Combobox(ana_panel, state="readonly", width=35)
usb_menu.pack(pady=10, anchor="w")
tk.Button(ana_panel, text="SÜRÜCÜLERİ TARA", command=suruculeri_tara, bg="#333333", fg=beyaz, relief="flat", width=22).pack(anchor="w")

tk.Frame(ana_panel, height=1, bg="#222222").pack(fill="x", pady=20)

# 3. YAZMA MODLARI
tk.Label(ana_panel, text="3. YAZMA SEÇENEKLERİ", font=("Arial", 10, "bold"), bg=panel_koyu, fg=asil_kirmizi).pack(anchor="w")
mod_menu = ttk.Combobox(ana_panel, state="readonly", width=35)
mod_menu['values'] = ("DD Modu [Önerilen]", "ISO Modu (GNU/Linux)", "ISO Modu (Windows)")
mod_menu.current(0)
mod_menu.pack(pady=10, anchor="w")

# BAŞLAT BUTONU
btn_baslat = tk.Button(pencere, text="YAZDIRMAYI BAŞLAT", command=yazdirma_baslat, bg=asil_kirmizi, fg=beyaz, font=("Arial", 13, "bold"), relief="flat", height=2, width=32)
btn_baslat.pack(pady=35)

suruculeri_tara()
pencere.mainloop()
