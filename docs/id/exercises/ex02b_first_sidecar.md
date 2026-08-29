# Latihan 2B: Sidecar Pertama Anda

> **Durasi:** 20 menit | **Modul:** 2 — Ekosistem Plugin

---

## Tujuan

Buat **sidecar standup harian** terjadwal yang berjalan pada pukul 9 pagi Senin–Jumat, membuat percakapan AGY baru, dan memintanya untuk merangkum commit git kemarin di seluruh repositori Anda.

---

## Latar Belakang

Sidecar adalah proses latar belakang persisten yang dikelola oleh AGY untuk Anda — mereka diluncurkan secara otomatis saat AGY dimulai, dimulai ulang saat terjadi crash, dan berjalan secara independen dari percakapan aktif Anda. Fungsi bawaan `schedule` menerima ekspresi cron dan perintah untuk dijalankan pada jadwal tersebut.

---

## Bagian 1: Membuat Konfigurasi Sidecar (5 menit)

Buat direktori sidecar dan berkas konfigurasi:

```bash
mkdir -p ~/.gemini/config/sidecars/standup
```

Buat `~/.gemini/config/sidecars/standup/sidecar.json`:

```json
{
  "description": "Daily standup — summarises yesterday's git commits",
  "builtin": "schedule",
  "args": [
    "0 9 * * 1-5",
    "agentapi",
    "new-conversation",
    "Summarise all git commits from yesterday across my repos. Group by repo, list the most impactful changes first, and flag any commits that touch security-sensitive files."
  ]
}
```

**Keputusan utama:**

- `builtin: "schedule"` — menggunakan penjadwal cron bawaan AGY alih-alih perintah mentah
- `0 9 * * 1-5` — berjalan pada pukul 09:00 Senin hingga Jumat
- `agentapi new-conversation` — secara terprogram membuka percakapan AGY baru dengan prompt standup Anda

---

## Bagian 2: Mengaktifkan Sidecar (5 menit)

Sidecar **dinonaktifkan secara default**. Aktifkan di `~/.gemini/config/config.json`:

```bash
# View current config (create if it doesn't exist)
cat ~/.gemini/config/config.json 2>/dev/null || echo '{}'
```

Edit `~/.gemini/config/config.json` untuk menyertakan entri sidecar:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    }
  }
}
```

> **Catatan:** Jika Anda sudah memiliki konten di `config.json`, gabungkan blok `sidecars` ke dalam JSON Anda yang sudah ada — jangan ganti file tersebut.

---

## Bagian 3: Verifikasi Sidecar (5 menit)

Mulai AGY dan periksa apakah sidecar telah ditemukan:

```bash
agy
```

Di dalam sesi, tanyakan:

```text
> What sidecars are currently configured? Is the standup sidecar active?
```

Periksa direktori data runtime sidecar:

```bash
ls -la ~/.gemini/antigravity-cli/sidecar_data/standup/logs/
```

Jika direktori tersebut ada, sidecar telah terdaftar. Berkas log akan muncul di sini dengan keluaran stdout/stderr yang diberi stempel waktu setelah setiap eksekusi yang dijadwalkan.

> **Kiat:** Sidecar tidak akan berjalan hingga pukul 9 pagi pada hari kerja. Untuk mengujinya segera, ubah sementara cron menjadi `* * * * *` (setiap menit), tunggu 60 detik, lalu periksa log. **Ingatlah untuk mengubahnya kembali.**

---

## Bagian 4: Memeriksa Tata Letak Runtime (5 menit)

Periksa struktur data sidecar secara lengkap:

```bash
# The sidecar runtime directory layout
find ~/.gemini/antigravity-cli/sidecar_data/standup/ -type f 2>/dev/null
```

Struktur yang diharapkan:

```text
~/.gemini/antigravity-cli/sidecar_data/standup/
├── data/     ← persistent storage (ANTIGRAVITY_EXECUTABLE_DATA_DIR env var)
├── logs/     ← timestamped stdout/stderr logs
└── events/   ← JSON records of agentapi calls
```

---

## Tujuan Tambahan: Sidecar Pengamat File

Tambahkan sidecar kedua yang menggunakan `command: python3` alih-alih bawaan `schedule`. Sidecar ini mengamati file lokal untuk mencari perubahan dan mengirimkan pesan ke percakapan yang ada ketika mendeteksi adanya perbedaan (diff).

Buat `~/.gemini/config/sidecars/file-watcher/sidecar.json`:

```json
{
  "description": "Watches a target file and alerts on changes",
  "command": "python3",
  "args": ["watch.py"],
  "restart_policy": "on-failure",
  "env": {
    "WATCH_FILE": "/path/to/your/important-file.yaml"
  }
}
```

Buat `~/.gemini/config/sidecars/file-watcher/watch.py`:

```python
import os
import time
import hashlib
import subprocess

WATCH_FILE = os.environ.get("WATCH_FILE", "")
POLL_INTERVAL = 5  # seconds

def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    if not os.path.exists(WATCH_FILE):
        print(f"File not found: {WATCH_FILE}")
        return

    last_hash = file_hash(WATCH_FILE)
    print(f"Watching {WATCH_FILE} (initial hash: {last_hash[:12]}...)")

    while True:
        time.sleep(POLL_INTERVAL)
        current_hash = file_hash(WATCH_FILE)
        if current_hash != last_hash:
            print(f"Change detected! {last_hash[:12]} -> {current_hash[:12]}")
            subprocess.run([
                "agentapi", "new-conversation",
                f"The file {WATCH_FILE} was modified. Please review the changes."
            ])
            last_hash = current_hash

if __name__ == "__main__":
    main()
```

Aktifkan di `~/.gemini/config/config.json`:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    },
    "file-watcher": {
      "enabled": true
    }
  }
}
```

---

## Kriteria Penyelesaian

- [ ] `~/.gemini/config/sidecars/standup/sidecar.json` ada dengan bawaan `schedule` dan cron `0 9 * * 1-5`
- [ ] `~/.gemini/config/config.json` memiliki `sidecars.standup.enabled: true`
- [ ] AGY mengenali sidecar tersebut (dikonfirmasi melalui kueri sesi atau keberadaan direktori log)
- [ ] Direktori runtime sidecar ada di `~/.gemini/antigravity-cli/sidecar_data/standup/`
- [ ] *(Tantangan)* Sidecar pengamat berkas dibuat dengan `command: python3` dan `watch.py` yang berfungsi
