/**
 * MIRAI NO WEBU — Data Terpusat Papan Peringkat (Leaderboard Master Data)
 * Sumber data tunggal untuk Papan Peringkat (peringkat.html) dan Statistik Prestasi (tentang.html).
 */

(function() {
    window.leaderboardData = {
            rajio: {
                badge: "PAPAN PERINGKAT · NIHON GO RAJIO",
                title: "Papan Peringkat <span>Nihon Go Rajio</span>",
                desc: "Dihitung berdasarkan jumlah keikutsertaan menyimak siaran rutin mingguan Nihon Go Rajio dan keaktifan menjawab kuis interaktif bahasa Jepang.",
                top3: [
                    {
                        rank: 1,
                        name: "Sakura Yuna",
                        class: "Kelas XI-Bahasa · Divisi Bahasa <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "28 Kali",
                        unit: "Siaran & Kuis Rajio",
                        quote: "Tidak pernah absen menjawab kuis kosakata kanji di setiap sesi rajio!",
                        avatar: "images/mirai/stiker/dik.jpeg",
                        activityLog: [
                            { tgl: "20 Feb 2026", nama: "Nihon Go Rajio #28: Tanya Jawab Budaya Jepang & Kosakata Populer", rekan: ["Kenzou Arata", "Arya Mitsuki"] },
                            { tgl: "13 Feb 2026", nama: "Nihon Go Rajio #27: Bedah Lirik Lagu YOASOBI & Partikel Bahasa", rekan: ["Siti Hanabi"] },
                            { tgl: "06 Feb 2026", nama: "Nihon Go Rajio #26: Kosakata Sehari-hari & Dialek Kansai", rekan: ["Haikal Daichi", "Aoi Minami"] },
                            { tgl: "30 Jan 2026", nama: "Nihon Go Rajio #25: Bedah Ungkapan Gaul Anime (Wakamono Kotoba)", rekan: ["Kenzou Arata"] },
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Tips Menghafal Pola Kalimat N5 Cepat & Menyenangkan", rekan: ["Arya Mitsuki", "Siti Hanabi"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Kuis Interaktif Kanji Dasar & Hadiah Menarik", rekan: ["Haikal Daichi"] }
                        ]
                    },
                    {
                        rank: 2,
                        name: "Kenzou Arata",
                        class: "Kelas XI-MIPA 2 · Divisi Bahasa <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "24 Kali",
                        unit: "Siaran & Kuis Rajio",
                        quote: "Selalu sedia mendengarkan siaran rajio sepulang sekolah!",
                        avatar: "images/mirai/stiker/be.jpeg",
                        activityLog: [
                            { tgl: "20 Feb 2026", nama: "Nihon Go Rajio #28: Tanya Jawab Budaya Jepang & Kosakata Populer", rekan: ["Sakura Yuna", "Arya Mitsuki"] },
                            { tgl: "13 Feb 2026", nama: "Nihon Go Rajio #27: Diskusi Perbedaan Aisatsu Formal dan Kasual", rekan: ["Haikal Daichi"] },
                            { tgl: "30 Jan 2026", nama: "Nihon Go Rajio #25: Bedah Ungkapan Gaul Anime (Wakamono Kotoba)", rekan: ["Sakura Yuna"] },
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Pengucapan Intonasi (Pitch Accent) Bahasa Jepang", rekan: ["Aoi Minami", "Rizky Ren"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Kuis Interaktif Kanji Dasar & Kosakata Musim Dingin", rekan: ["Nadia Hinata"] }
                        ]
                    },
                    {
                        rank: 3,
                        name: "Haikal Daichi",
                        class: "Kelas X-7 · Divisi Desain <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "21 Kali",
                        unit: "Siaran & Kuis Rajio",
                        quote: "Rajin bertanya makna ungkapan gaul di sesi tanya jawab radio.",
                        avatar: "images/mirai/stiker/ala.jpeg",
                        activityLog: [
                            { tgl: "13 Feb 2026", nama: "Nihon Go Rajio #27: Diskusi Perbedaan Aisatsu Formal dan Kasual", rekan: ["Kenzou Arata"] },
                            { tgl: "06 Feb 2026", nama: "Nihon Go Rajio #26: Kosakata Sehari-hari & Dialek Kansai", rekan: ["Sakura Yuna", "Aoi Minami"] },
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Filosofi Desain Poster Tradisional Jepang", rekan: ["Arya Mitsuki"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Kuis Interaktif Kanji Dasar & Hadiah Menarik", rekan: ["Sakura Yuna"] },
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Kosakata Seni Ilustrasi & Manga", rekan: ["Mei Chiyo", "Bima Ryouta"] }
                        ]
                    }
                ],
                ranks4to10: [
                    {
                        rank: 4,
                        name: "Aoi Minami",
                        class: "Kelas XI-IPS 1",
                        divisi: "Divisi Bahasa",
                        score: "18 Kali",
                        streak: "18 Sesi Rajio",
                        avatar: "images/mirai/stiker/ada.jpeg",
                        activityLog: [
                            { tgl: "06 Feb 2026", nama: "Nihon Go Rajio #26: Kosakata Sehari-hari & Dialek Kansai", rekan: ["Sakura Yuna", "Haikal Daichi"] },
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Pengucapan Intonasi (Pitch Accent) Bahasa Jepang", rekan: ["Kenzou Arata", "Rizky Ren"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Pembahasan Soal Bunpou JLPT N5", rekan: ["Sakura Yuna"] },
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Dialog Kasual dalam Anime Seinen", rekan: ["Fathir Souta"] }
                        ]
                    },
                    {
                        rank: 5,
                        name: "Rizky Ren",
                        class: "Kelas X-3",
                        divisi: "Divisi Cosplay",
                        score: "16 Kali",
                        streak: "16 Sesi Rajio",
                        avatar: "images/mirai/stiker/aku.jpeg",
                        activityLog: [
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Kosakata Khusus Dunia Cosplay & Panggung", rekan: ["Zahra Ayumi", "Aoi Minami"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Panduan Istilah Properti & Kostum Anime", rekan: ["Zahra Ayumi"] },
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Kuis Kosakata Ekspresi Karakter Anime", rekan: ["Sakura Yuna", "Fathir Souta"] },
                            { tgl: "19 Des 2025", nama: "Nihon Go Rajio #20: Sesi Cerita Komunitas Cosplay Jepang", rekan: ["Zahra Ayumi"] }
                        ]
                    },
                    {
                        rank: 6,
                        name: "Nadia Hinata",
                        class: "Kelas XI-MIPA 4",
                        divisi: "Divisi Kewirausahaan",
                        score: "15 Kali",
                        streak: "15 Sesi Rajio",
                        avatar: "images/mirai/stiker/bel.jpeg",
                        activityLog: [
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Kuis Interaktif Kanji & Kosakata Kuliner Jepang", rekan: ["Kenzou Arata"] },
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Istilah Jual-Beli & Budaya Matsuri", rekan: ["Mei Chiyo", "Bima Ryouta"] },
                            { tgl: "19 Des 2025", nama: "Nihon Go Rajio #20: Pengenalan Makanan Tradisional Festival Jepang", rekan: ["Sakura Yuna"] },
                            { tgl: "12 Des 2025", nama: "Nihon Go Rajio #19: Kosakata Pelayanan Toko (Omotenashi)", rekan: ["Siti Hanabi"] }
                        ]
                    },
                    {
                        rank: 7,
                        name: "Fathir Souta",
                        class: "Kelas X-1",
                        divisi: "Divisi Bahasa",
                        score: "13 Kali",
                        streak: "13 Sesi Rajio",
                        avatar: "images/mirai/stiker/beli.jpeg",
                        activityLog: [
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Kuis Kosakata Ekspresi Karakter Anime", rekan: ["Rizky Ren", "Aoi Minami"] },
                            { tgl: "19 Des 2025", nama: "Nihon Go Rajio #20: Tata Bahasa Bentuk Sopan (Teinei-go)", rekan: ["Sakura Yuna", "Kenzou Arata"] },
                            { tgl: "12 Des 2025", nama: "Nihon Go Rajio #19: Latihan Mendengarkan (Choukai) Pemula", rekan: ["Bima Ryouta"] },
                            { tgl: "05 Des 2025", nama: "Nihon Go Rajio #18: Kosakata Sekolah & Percakapan Siswa", rekan: ["Aoi Minami"] }
                        ]
                    },
                    {
                        rank: 8,
                        name: "Mei Chiyo",
                        class: "Kelas XII-Bahasa",
                        divisi: "Divisi Desain",
                        score: "12 Kali",
                        streak: "12 Sesi Rajio",
                        avatar: "images/mirai/stiker/ber.jpeg",
                        activityLog: [
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Istilah Jual-Beli & Budaya Matsuri", rekan: ["Nadia Hinata", "Bima Ryouta"] },
                            { tgl: "19 Des 2025", nama: "Nihon Go Rajio #20: Tips Sketsa Visual Karakter Chibi", rekan: ["Haikal Daichi"] },
                            { tgl: "05 Des 2025", nama: "Nihon Go Rajio #18: Mengenal Warna & Simbol Tradisional Jepang", rekan: ["Arya Mitsuki", "Haikal Daichi"] },
                            { tgl: "28 Nov 2025", nama: "Nihon Go Rajio #17: Istilah Alat Gambar Digital & Manga", rekan: ["Tania Riko"] }
                        ]
                    },
                    {
                        rank: 9,
                        name: "Bima Ryouta",
                        class: "Kelas X-5",
                        divisi: "Divisi Bahasa",
                        score: "11 Kali",
                        streak: "11 Sesi Rajio",
                        avatar: "images/mirai/stiker/cer.jpeg",
                        activityLog: [
                            { tgl: "09 Jan 2026", nama: "Nihon Go Rajio #22: Kosakata Seni Ilustrasi & Manga", rekan: ["Mei Chiyo", "Haikal Daichi"] },
                            { tgl: "12 Des 2025", nama: "Nihon Go Rajio #19: Latihan Mendengarkan (Choukai) Pemula", rekan: ["Fathir Souta"] },
                            { tgl: "05 Des 2025", nama: "Nihon Go Rajio #18: Dialog Percakapan Bahasa Jepang Santai", rekan: ["Sakura Yuna"] },
                            { tgl: "21 Nov 2025", nama: "Nihon Go Rajio #16: Kuis Tebak Kanji Nama Hewan & Tumbuhan", rekan: ["Kenzou Arata", "Fathir Souta"] }
                        ]
                    },
                    {
                        rank: 10,
                        name: "Zahra Ayumi",
                        class: "Kelas XI-IPS 3",
                        divisi: "Divisi Cosplay",
                        score: "10 Kali",
                        streak: "10 Sesi Rajio",
                        avatar: "images/mirai/stiker/dip.jpeg",
                        activityLog: [
                            { tgl: "23 Jan 2026", nama: "Nihon Go Rajio #24: Kosakata Khusus Dunia Cosplay & Panggung", rekan: ["Rizky Ren", "Aoi Minami"] },
                            { tgl: "16 Jan 2026", nama: "Nihon Go Rajio #23: Panduan Istilah Properti & Kostum Anime", rekan: ["Rizky Ren"] },
                            { tgl: "19 Des 2025", nama: "Nihon Go Rajio #20: Sesi Cerita Komunitas Cosplay Jepang", rekan: ["Rizky Ren"] },
                            { tgl: "21 Nov 2025", nama: "Nihon Go Rajio #16: Istilah Make-up & Karakterisasi Jepang", rekan: ["Vino Taiga", "Reza Shin"] }
                        ]
                    }
                ]
            },
            kehadiran: {
                badge: "PAPAN PERINGKAT · KEHADIRAN",
                title: "Papan Peringkat <span>Kehadiran</span>",
                desc: "Dihitung berdasarkan jumlah kehadiran anggota dalam sesi perkumpulan mingguan, workshop kebudayaan, serta agenda resmi klub.",
                top3: [
                    {
                        rank: 1,
                        name: "Dewi Megumi",
                        class: "Kelas XI-MIPA 1 · Divisi Bahasa <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "24 Kali Hadir",
                        unit: "Dari 24 Pertemuan (100%)",
                        quote: "Selalu datang paling awal dan membantu persiapan ruangan!",
                        avatar: "images/mirai/stiker/eet.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" }
                        ]
                    },
                    {
                        rank: 2,
                        name: "Farhan Kazuki",
                        class: "Kelas X-4 · Divisi Desain <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "23 Kali Hadir",
                        unit: "Dari 24 Pertemuan (96%)",
                        quote: "Sangat antusias dalam setiap sesi latihan kanji bersama.",
                        avatar: "images/mirai/stiker/cer.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Forum Diskusi Divisi Desain & Proyek Banner Klub" }
                        ]
                    },
                    {
                        rank: 3,
                        name: "Laras Sayaka",
                        class: "Kelas XI-Bahasa · Divisi Kewirausahaan <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "22 Kali Hadir",
                        unit: "Dari 24 Pertemuan (92%)",
                        quote: "Aktif mengoordinasi presensi teman-teman satu angkatan.",
                        avatar: "images/mirai/stiker/bel.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Rapat Koordinasi Stan Kewirausahaan Festival Jepang" }
                        ]
                    }
                ],
                ranks4to10: [
                    {
                        rank: 4,
                        name: "Ilham Haruto",
                        class: "Kelas X-2",
                        divisi: "Divisi Cosplay",
                        score: "21 Kali Hadir",
                        streak: "Presensi 88%",
                        avatar: "images/mirai/stiker/don.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" }
                        ]
                    },
                    {
                        rank: 5,
                        name: "Rania Koharu",
                        class: "Kelas XI-IPS 2",
                        divisi: "Divisi Bahasa",
                        score: "20 Kali Hadir",
                        streak: "Presensi 83%",
                        avatar: "images/mirai/stiker/gom.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Pelatihan Presentasi Berbahasa Jepang Sederhana" }
                        ]
                    },
                    {
                        rank: 6,
                        name: "Dimas Hayate",
                        class: "Kelas X-6",
                        divisi: "Divisi Desain",
                        score: "20 Kali Hadir",
                        streak: "Presensi 83%",
                        avatar: "images/mirai/stiker/ita.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Pelatihan Desain Grafis Flyer Promosi Klub" }
                        ]
                    },
                    {
                        rank: 7,
                        name: "Alya Kasumi",
                        class: "Kelas XI-MIPA 3",
                        divisi: "Divisi Bahasa",
                        score: "19 Kali Hadir",
                        streak: "Presensi 79%",
                        avatar: "images/mirai/stiker/jaw.jpeg",
                        activityLog: [
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Sesi Latihan Membaca Paragraf Bahasa Jepang N5" }
                        ]
                    },
                    {
                        rank: 8,
                        name: "Bagus Tatsuya",
                        class: "Kelas X-8",
                        divisi: "Divisi Kewirausahaan",
                        score: "18 Kali Hadir",
                        streak: "Presensi 75%",
                        avatar: "images/mirai/stiker/kar.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Pengadaan Merchandise & Sticker Klub" }
                        ]
                    },
                    {
                        rank: 9,
                        name: "Celine Hina",
                        class: "Kelas XI-IPS 4",
                        divisi: "Divisi Cosplay",
                        score: "18 Kali Hadir",
                        streak: "Presensi 75%",
                        avatar: "images/mirai/stiker/kok.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "14 Feb 2026", nama: "Pertemuan Rutin #23: Bedah Pola Kalimat Bentuk Lampau & Percakapan Berpasangan" },
                            { tgl: "24 Jan 2026", nama: "Pertemuan Rutin #20: Bedah Tata Bahasa Pola ~Te Form dan Penggunaannya" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Latihan Gerak dan Koreografi Budaya Jepang" }
                        ]
                    },
                    {
                        rank: 10,
                        name: "Raka Jin",
                        class: "Kelas X-3",
                        divisi: "Divisi Bahasa",
                        score: "17 Kali Hadir",
                        streak: "Presensi 71%",
                        avatar: "images/mirai/stiker/log.jpeg",
                        activityLog: [
                            { tgl: "21 Feb 2026", nama: "Pertemuan Rutin #24: Evaluasi Program Kerja Tengah Semester & Pemantapan Kanji" },
                            { tgl: "07 Feb 2026", nama: "Pertemuan Rutin #22: Workshop Budaya Origami & Pembuatan Mading Klub" },
                            { tgl: "31 Jan 2026", nama: "Pertemuan Rutin #21: Latihan Menulis Huruf Katakana & Istilah Serapan Asing" },
                            { tgl: "17 Jan 2026", nama: "Pertemuan Rutin #19: Pembekalan Peserta Delegasi Lomba Bunkasai 2026" },
                            { tgl: "10 Jan 2026", nama: "Pertemuan Rutin #18: Diskusi Interaktif Pengenalan Kanzen N5" }
                        ]
                    }
                ]
            },
            prestasi: {
                badge: "PAPAN PERINGKAT · PRESTASI",
                title: "Papan Peringkat <span>Prestasi</span>",
                desc: "Dihitung berdasarkan pencapaian prestasi lomba bahasa Jepang (Bunkasai), sertifikat kejuaraan, serta dedikasi karya desain dan artikel klub.",
                top3: [
                    {
                        rank: 1,
                        name: "Arya Mitsuki",
                        class: "Kelas XII-Bahasa · Divisi Desain <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "18 Prestasi & Karya",
                        unit: "Kejuaraan & Desain Resmi",
                        quote: "Juara 1 Desain Karakter Bunkasai & ilustrator maskot klub!",
                        avatar: "images/mirai/stiker/hua.jpeg",
                        activityLog: [
                            { tgl: "18 Jan 2026", nama: "Juara 1 Digital Fanart & Desain Karakter Bunkasai SMA Jawa Timur", kategori: "Kejuaraan Tingkat Provinsi Jatim" },
                            { tgl: "12 Des 2025", nama: "Ilustrator Utama Maskot Resmi Mirai No Hana Kabinet Sora 2025/2026", kategori: "Karya Desain Resmi Klub" },
                            { tgl: "22 Nov 2025", nama: "Juara 2 Lomba Poster Kebudayaan Jepang Bunkasai Wilayah Surabaya", kategori: "Kejuaraan Antar-SMA" },
                            { tgl: "15 Okt 2025", nama: "Desainer Grafis Booklet Modul Pembelajaran Kanji Klub", kategori: "Karya Desain Edukasi Klub" },
                            { tgl: "28 Sep 2025", nama: "Juara Harapan 1 Desain Komik Strip Mini Manga Fest", kategori: "Kompetisi Kreatif Pelajar" },
                            { tgl: "14 Agu 2025", nama: "Perancang Identitas Visual & Merchandise Resmi Dies Natalis Klub", kategori: "Dedikasi Proyek Klub" }
                        ]
                    },
                    {
                        rank: 2,
                        name: "Siti Hanabi",
                        class: "Kelas XI-IPS 1 · Divisi Bahasa <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "14 Prestasi & Karya",
                        unit: "Kejuaraan & Artikel Edukasi",
                        quote: "Juara 2 Lomba Rodoku & penulis materi mading kebudayaan.",
                        avatar: "images/mirai/stiker/iki.jpeg",
                        activityLog: [
                            { tgl: "25 Jan 2026", nama: "Juara 2 Lomba Rodoku (Membaca Teks Bahasa Jepang) Bunkasai Universitas", kategori: "Kejuaraan Tingkat Jawa Timur" },
                            { tgl: "19 Des 2025", nama: "Penulis Utama Seri Artikel Kebudayaan Jepang Mading Klub", kategori: "Karya Literasi Budaya" },
                            { tgl: "14 Nov 2025", nama: "Juara 3 Cerdas Cermat Bahasa Jepang (Nihongo Quiz) Tingkat SMA", kategori: "Kompetisi Akademik Jepang" },
                            { tgl: "10 Okt 2025", nama: "Lulus Ujian Kemampuan Bahasa Jepang JLPT Sertifikasi Level N4", kategori: "Sertifikasi Resmi Internasional" },
                            { tgl: "05 Sep 2025", nama: "Juara Harapan 1 Lomba Pidato Bahasa Jepang (Ben弁论大会)", kategori: "Lomba Pidato Pelajar" },
                            { tgl: "18 Agu 2025", nama: "Kontributor Esai Edukasi Budaya Matsuri Terpilih", kategori: "Karya Artikel Terpilih" }
                        ]
                    },
                    {
                        rank: 3,
                        name: "Vino Taiga",
                        class: "Kelas XI-MIPA 5 · Divisi Cosplay <span class=\"podium-period-pill\">Periode 2025/2026</span>",
                        score: "11 Prestasi & Karya",
                        unit: "Kejuaraan & Properti Kreatif",
                        quote: "Juara Harapan Cosplay Showcase & perancang properti festival.",
                        avatar: "images/mirai/stiker/iwa.jpeg",
                        activityLog: [
                            { tgl: "20 Jan 2026", nama: "Juara Harapan 1 Cosplay Walk & Armor Showcase Fest SMA Se-Derajat", kategori: "Kejuaraan Seni Panggung" },
                            { tgl: "15 Des 2025", nama: "Koordinator Perancang Properti Panggung & Booth Budaya Matsuri", kategori: "Dedikasi Properti Klub" },
                            { tgl: "10 Nov 2025", nama: "Juara 2 Kostum Kreatif Budaya Populer Bunkasai Pelajar", kategori: "Festival Kreatif Pelajar" },
                            { tgl: "18 Okt 2025", nama: "Peraih Apresiasi Properti Armor Terbaik Karya Mandiri Siswa", kategori: "Karya Mandiri Siswa" },
                            { tgl: "12 Sep 2025", nama: "Koreografer Pertunjukan Kabaret Drama Jepang Sekolah", kategori: "Pertunjukan Seni Kebudayaan" }
                        ]
                    }
                ],
                ranks4to10: [
                    {
                        rank: 4,
                        name: "Clara Yuki",
                        class: "Kelas X-2",
                        divisi: "Divisi Desain",
                        score: "9 Prestasi",
                        streak: "Juara Fanart",
                        avatar: "images/mirai/stiker/mas.jpeg",
                        activityLog: [
                            { tgl: "14 Jan 2026", nama: "Juara 2 Lomba Ilustrasi Tradisional Bunkasai Se-Jawa Timur", kategori: "Kejuaraan Seni Ilustrasi" },
                            { tgl: "20 Des 2025", nama: "Kontributor Desain Cover Buku Tahunan Klub Mirai No Hana", kategori: "Karya Desain Klub" },
                            { tgl: "18 Nov 2025", nama: "Juara Harapan 2 Desain Karakter Orisinil Festival Seni", kategori: "Kompetisi Karakter Desain" },
                            { tgl: "22 Okt 2025", nama: "Kreator Set Sticker Chat Maskot Klub 2025", kategori: "Aset Digital Kreatif" }
                        ]
                    },
                    {
                        rank: 5,
                        name: "Fandi Kaito",
                        class: "Kelas XI-Bahasa",
                        divisi: "Divisi Bahasa",
                        score: "8 Prestasi",
                        streak: "Finalis Cerdas Cermat",
                        avatar: "images/mirai/stiker/peg.jpeg",
                        activityLog: [
                            { tgl: "12 Jan 2026", nama: "Finalis 5 Besar Cerdas Cermat Pengetahuan Umum Jepang", kategori: "Kompetisi Cerdas Cermat" },
                            { tgl: "10 Des 2025", nama: "Juara 3 Lomba Menulis Esai Bahasa Jepang Pemula", kategori: "Kompetisi Menulis Esai" },
                            { tgl: "15 Nov 2025", nama: "Lulus Ujian Kemampuan Bahasa Jepang JLPT Sertifikasi Level N4", kategori: "Sertifikasi Resmi Internasional" },
                            { tgl: "08 Okt 2025", nama: "Delegasi Terbaik Simulasi Wawancara Beasiswa Jepang", kategori: "Simulasi Studi Akademik" }
                        ]
                    },
                    {
                        rank: 6,
                        name: "Nabila Sakura",
                        class: "Kelas X-7",
                        divisi: "Divisi Kewirausahaan",
                        score: "7 Prestasi",
                        streak: "Stan Terbaik Festival",
                        avatar: "images/mirai/stiker/sor.jpeg",
                        activityLog: [
                            { tgl: "18 Jan 2026", nama: "Peraih Predikat Stan Kewirausahaan Terbaik Festival Budaya Sekolah", kategori: "Penghargaan Stan Festival" },
                            { tgl: "05 Des 2025", nama: "Kreator Produk Kuliner Dorayaki & Onigiri Terlaris Klub", kategori: "Proyek Kewirausahaan" },
                            { tgl: "12 Nov 2025", nama: "Juara 3 Manajemen Usaha Mandiri Kreatif Siswa", kategori: "Kompetisi Usaha Kreatif" },
                            { tgl: "20 Sep 2025", nama: "Apresiasi Dedikasi Penggalangan Dana Kegiatan Bunkasai", kategori: "Penghargaan Dedikasi Klub" }
                        ]
                    },
                    {
                        rank: 7,
                        name: "Reza Shin",
                        class: "Kelas XI-IPS 3",
                        divisi: "Divisi Cosplay",
                        score: "6 Prestasi",
                        streak: "Kostum Terfavorit",
                        avatar: "images/mirai/stiker/sul.jpeg",
                        activityLog: [
                            { tgl: "15 Jan 2026", nama: "Juara Kostum Cosplay Terfavorit Pilihan Penonton Bunkasai", kategori: "Piala Favorit Festival" },
                            { tgl: "28 Nov 2025", nama: "Perancang Kostum Haori & Aksesori Budaya Festival Pelajar", kategori: "Karya Desain Kostum" },
                            { tgl: "16 Okt 2025", nama: "Juara Harapan 1 Cosplay Performance Kategori Individu", kategori: "Kompetisi Panggung" },
                            { tgl: "05 Sep 2025", nama: "Pemberi Materi Workshop Dasar Pembuatan Kostum Cosplay", kategori: "Pemateri Workshop Klub" }
                        ]
                    },
                    {
                        rank: 8,
                        name: "Tania Riko",
                        class: "Kelas X-4",
                        divisi: "Divisi Desain",
                        score: "5 Prestasi",
                        streak: "Karya Grafis Digital",
                        avatar: "images/mirai/stiker/woy.jpeg",
                        activityLog: [
                            { tgl: "10 Jan 2026", nama: "Juara 3 Kompetisi Desain Logo & Tipografi Kebudayaan", kategori: "Kompetisi Desain Grafis" },
                            { tgl: "14 Des 2025", nama: "Desainer Grafis Konten Media Sosial Instagram Klub", kategori: "Media & Publikasi Klub" },
                            { tgl: "02 Nov 2025", nama: "Kontributor Visual Infografis Kanji Mingguan", kategori: "Konten Edukasi Digital" },
                            { tgl: "19 Sep 2025", nama: "Peraih Karya Grafis Digital Terpilih Pameran Sekolah", kategori: "Pameran Karya Sekolah" }
                        ]
                    },
                    {
                        rank: 9,
                        name: "Yoga Daiki",
                        class: "Kelas XII-MIPA 1",
                        divisi: "Divisi Bahasa",
                        score: "5 Prestasi",
                        streak: "Lulus JLPT N3",
                        avatar: "images/mirai/stiker/yan.jpeg",
                        activityLog: [
                            { tgl: "08 Jan 2026", nama: "Lulus Ujian Kemampuan Bahasa Jepang JLPT Resmi Level N3", kategori: "Sertifikasi Resmi Internasional" },
                            { tgl: "20 Nov 2025", nama: "Tutor Sebaya Bimbingan Belajar Kanji Kelas X & XI", kategori: "Program Tutor Sebaya" },
                            { tgl: "25 Okt 2025", nama: "Juara Harapan 2 Lomba Terjemahan Teks Bahasa Jepang", kategori: "Kompetisi Penerjemahan" },
                            { tgl: "14 Agu 2025", nama: "Penyusun Bank Soal Latihan Kanji Persiapan JLPT Klub", kategori: "Pengembangan Materi Klub" }
                        ]
                    },
                    {
                        rank: 10,
                        name: "Amelia Nonoka",
                        class: "Kelas X-1",
                        divisi: "Divisi Bahasa",
                        score: "4 Prestasi",
                        streak: "Finalis Shodou",
                        avatar: "images/mirai/stiker/yat.jpeg",
                        activityLog: [
                            { tgl: "16 Jan 2026", nama: "Finalis Lomba Kaligrafi Jepang (Shodou 书道) Bunkasai SMA", kategori: "Kompetisi Seni Tradisional" },
                            { tgl: "02 Des 2025", nama: "Karya Kaligrafi Kanji Terbaik Terpajang di Pameran Klub", kategori: "Pameran Seni Budaya" },
                            { tgl: "18 Okt 2025", nama: "Peserta Terbaik Workshop Seni Menulis Kanji Tradisional", kategori: "Apresiasi Workshop" },
                            { tgl: "12 Agu 2025", nama: "Kontributor Karya Seni Mading Edisi Spesial Kemerdekaan", kategori: "Karya Mading Sekolah" }
                        ]
                    }
                ]
            }
        };

    // Konfigurasi & sinkronisasi data prestasi kejuaraan
    if (window.leaderboardData && window.leaderboardData.prestasi) {
        const p = window.leaderboardData.prestasi;

        // Delegasi historis & partisipasi ajang eksternal klub
        p.delegasiTambahan = [
            // Prestasi kejuaraan historis klub (Maskot & Alumni)
            { nama: "Juara Umum Bunkasai Jawa Timur (Maskot Asora Aokita)", tgl: "2025", kategori: "Kejuaraan Provinsi", tipe: "prestasi" },
            { nama: "Juara 1 Desain Maskot Resmi Asora Aokita", tgl: "2025", kategori: "Kompetisi Desain", tipe: "prestasi" },
            { nama: "Piala Bergilir Kebudayaan Jepang Jawa Timur", tgl: "2024", kategori: "Piala Bergilir", tipe: "prestasi" },
            { nama: "Juara 1 Cerdas Cermat Bahasa Jepang Tingkat Provinsi", tgl: "2024", kategori: "Kompetisi Akademik", tipe: "prestasi" },

            // Keikutsertaan delegasi klub dalam ajang lomba (Menang/kalah tercatat terbuka)
            { nama: "Delegasi Lomba Bunkasai Wilayah Gerbangkertosusila", tgl: "2025", kategori: "Delegasi Kompetisi", tipe: "partisipasi" },
            { nama: "Delegasi Festival Kebudayaan Jepang Surabaya", tgl: "2025", kategori: "Delegasi Festival", tipe: "partisipasi" },
            { nama: "Delegasi Olimpiade Bahasa Jepang SMA Se-Jatim", tgl: "2024", kategori: "Delegasi Olimpiade", tipe: "partisipasi" },
            { nama: "Delegasi Seleksi Nasional Pertukaran Pelajar Jepang", tgl: "2024", kategori: "Seleksi Delegasi", tipe: "partisipasi" }
        ];

        // Pemetaan eksplisit untuk 17 kejuaraan podium aktif dan 2 delegasi finalis aktif
        const prestasiNames = [
            'Juara 1 Digital Fanart & Desain Karakter Bunkasai SMA Jawa Timur',
            'Juara 2 Lomba Poster Kebudayaan Jepang Bunkasai Wilayah Surabaya',
            'Juara Harapan 1 Desain Komik Strip Mini Manga Fest',
            'Juara 2 Lomba Rodoku (Membaca Teks Bahasa Jepang) Bunkasai Universitas',
            'Juara 3 Cerdas Cermat Bahasa Jepang (Nihongo Quiz) Tingkat SMA',
            'Lulus Ujian Kemampuan Bahasa Jepang JLPT Sertifikasi Level N4', // Siti Hanabi
            'Juara Harapan 1 Cosplay Walk & Armor Showcase Fest SMA Se-Derajat',
            'Juara 2 Kostum Kreatif Budaya Populer Bunkasai Pelajar',
            'Juara 2 Lomba Ilustrasi Tradisional Bunkasai Se-Jawa Timur',
            'Juara Harapan 2 Desain Karakter Orisinil Festival Seni',
            'Juara 3 Lomba Menulis Esai Bahasa Jepang Pemula',
            'Peraih Predikat Stan Kewirausahaan Terbaik Festival Budaya Sekolah',
            'Juara 3 Manajemen Usaha Mandiri Kreatif Siswa',
            'Juara Kostum Cosplay Terfavorit Pilihan Penonton Bunkasai',
            'Juara Harapan 1 Cosplay Performance Kategori Individu',
            'Juara 3 Kompetisi Desain Logo & Tipografi Kebudayaan',
            'Juara Harapan 2 Lomba Terjemahan Teks Bahasa Jepang'
        ];

        const partisipasiNames = [
            'Finalis 5 Besar Cerdas Cermat Pengetahuan Umum Jepang',
            'Finalis Lomba Kaligrafi Jepang (Shodou 书道) Bunkasai SMA'
        ];

        const allMembers = [...(p.top3 || []), ...(p.ranks4to10 || [])];
        allMembers.forEach(m => {
            if (Array.isArray(m.activityLog)) {
                m.activityLog.forEach(item => {
                    const nm = item.nama || '';
                    if (m.name === 'Fandi Kaito' && nm.includes('JLPT')) {
                        item.tipe = 'karya';
                    } else if (prestasiNames.includes(nm)) {
                        item.tipe = 'prestasi';
                    } else if (partisipasiNames.includes(nm)) {
                        item.tipe = 'partisipasi';
                    } else {
                        item.tipe = 'karya'; // Karya/kontribusi internal klub
                    }
                });
            }
        });
    }

    /**
     * Menghitung total prestasi & partisipasi secara dinamis dari papan peringkat prestasi.
     * Jika ada data prestasi baru ditambahkan ke papan peringkat, angka pada halaman Tentang
     * akan otomatis bertambah secara real-time.
     */
    window.getLeaderboardPrestasiStats = function() {
        const cat = window.leaderboardData && window.leaderboardData.prestasi;
        if (!cat) return { prestasi: 21, partisipasi: 27 };

        let totalPrestasi = 0;
        let totalPartisipasi = 0;

        const allMembers = [...(cat.top3 || []), ...(cat.ranks4to10 || [])];

        allMembers.forEach(member => {
            if (Array.isArray(member.activityLog)) {
                member.activityLog.forEach(item => {
                    if (item.tipe === 'prestasi') {
                        totalPrestasi++;
                        totalPartisipasi++;
                    } else if (item.tipe === 'partisipasi') {
                        totalPartisipasi++;
                    } else if (item.tipe !== 'karya') {
                        // Untuk entri baru yang ditambahkan di masa depan tanpa menentukan tipe:
                        const text = ((item.nama || '') + ' ' + (item.kategori || '')).toLowerCase();
                        if (/juara|podium|pemenang|piala|lulus\s*ujian|sertifikasi|1st|2nd|3rd/.test(text)) {
                            totalPrestasi++;
                            totalPartisipasi++;
                        } else if (/finalis|delegasi|peserta|lomba|kompetisi|festival|bunkasai/.test(text)) {
                            totalPartisipasi++;
                        }
                    }
                });
            }
        });

        if (Array.isArray(cat.delegasiTambahan)) {
            cat.delegasiTambahan.forEach(item => {
                if (item.tipe === 'prestasi') {
                    totalPrestasi++;
                    totalPartisipasi++;
                } else if (item.tipe === 'partisipasi') {
                    totalPartisipasi++;
                }
            });
        }

        return {
            prestasi: totalPrestasi,
            partisipasi: totalPartisipasi
        };
    };
})();
