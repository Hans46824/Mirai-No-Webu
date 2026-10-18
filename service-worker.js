/**
 * Service Worker: service-worker.js
 * Website: MIRAI NO HANA (Mirai no Webu)
 * Dihasilkan otomatis oleh: skrip/arsip/build_precache_list.py
 * Versi Cache: mirai-app-shell-c3528335ef64
 */

const CACHE_NAME = "mirai-app-shell-c3528335ef64";
const DATA_CACHE_NAME = "mirai-data-cache-v1";
const OFFLINE_URL = "offline.html";

// Berkas precache app shell (dihasilkan otomatis dari pohon berkas)
const PRECACHE_ASSETS = [
  "index.html",
  "404.html",
  "offline.html",
  "divisi/index.html",
  "divisi/bahasa.html",
  "divisi/cosplay.html",
  "divisi/desain.html",
  "divisi/kewirausahaan.html",
  "kamus/index.html",
  "kamus/kanji.html",
  "kegiatan/index.html",
  "kegiatan/kimi-to-nippon.html",
  "kegiatan/konbini.html",
  "kegiatan/nihon-go-rajio.html",
  "kegiatan/ramadhan.html",
  "kegiatan/tomodachi.html",
  "kelas/index.html",
  "kelas/latihan.html",
  "kelas/motivasi.html",
  "lomba/index.html",
  "materi/dasar/index.html",
  "materi/dasar/hiragana.html",
  "materi/dasar/katakana.html",
  "materi/dasar/kosakata.html",
  "materi/dasar/jikoshokai.html",
  "materi/lanjutan/index.html",
  "materi/lanjutan/grammar.html",
  "materi/lanjutan/kanji.html",
  "materi/lanjutan/kalimat.html",
  "peringkat/index.html",
  "rekomendasi/index.html",
  "sora/index.html",
  "tentang/index.html",
  "toko/index.html",
  "css/style.css",
  "css/pages/global.css",
  "css/pages/navbar-hero-footer.css",
  "css/pages/beranda.css",
  "css/pages/kelas-materi.css",
  "css/pages/kamus.css",
  "css/pages/kegiatan-divisi.css",
  "css/pages/tentang.css",
  "css/pages/rekomendasi-motivasi.css",
  "css/pages/peringkat.css",
  "css/pages/lomba.css",
  "css/pages/toko.css",
  "js/main.js",
  "js/script.js",
  "js/progress.js",
  "js/kana.js",
  "js/kanji.js",
  "js/stroke.js",
  "js/sora.js",
  "js/api.js",
  "js/translator.js",
  "js/quiz-divisi.js",
  "js/carousel.js",
  "js/proker-slider.js",
  "manifest.webmanifest",
  "images/mirai/logo/MNH1-nav.png",
  "images/mirai/logo/MNH1.png",
  "images/mirai/logo/icon-192.png",
  "images/mirai/logo/icon-512.png"
];

// 1. Install: Simpan seluruh app shell ke dalam cache
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      try {
        await cache.addAll(PRECACHE_ASSETS);
      } catch (err) {
        console.warn("[SW] Bulk cache.addAll gagal, melakukan caching modular per-berkas:", err);
        await Promise.allSettled(PRECACHE_ASSETS.map((asset) => cache.add(asset)));
      }
    }).then(() => self.skipWaiting())
  );
});

// 2. Activate: Hapus cache usang dan ambil alih klien aktif
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME && name !== DATA_CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch: Strategi Cache-First untuk data/fonts dan Stale-While-Revalidate untuk halaman/aset
self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Abaikan non-GET requests
  if (req.method !== "GET") return;

  // STRATEGI A: Cache-First untuk data JSON lokal, goresan kanji, & Google Fonts
  const isDataRequest = url.pathname.includes("/data/") && url.pathname.endsWith(".json");
  const isFontRequest = url.hostname.includes("fonts.gstatic.com") || url.hostname.includes("fonts.googleapis.com");

  if (isDataRequest || isFontRequest) {
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then((cache) => {
        return cache.match(req).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(req).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              cache.put(req, networkResponse.clone());
            }
            return networkResponse;
          });
        });
      })
    );
    return;
  }

  // STRATEGI B: Stale-While-Revalidate untuk halaman web & app shell, fallback ke offline.html
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(req).then((cachedResponse) => {
        const fetchPromise = fetch(req).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            cache.put(req, networkResponse.clone());
          }
          return networkResponse;
        }).catch(async () => {
          // Jika offline dan navigasi halaman gagal, tampilkan offline.html
          if (req.mode === "navigate") {
            const fallback = await cache.match(OFFLINE_URL);
            if (fallback) return fallback;
            const anyOffline = await caches.match("offline.html");
            if (anyOffline) return anyOffline;
          }
          return cachedResponse;
        });

        return cachedResponse || fetchPromise;
      });
    })
  );
});
