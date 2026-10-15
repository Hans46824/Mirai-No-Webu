#!/usr/bin/env python3
"""
File: skrip/arsip/sync_datasets.py
Fungsi: Pipeline audit, kurasi, sinkronisasi dataset Kanji & Kana antara
        canonical source (data/kanji.json, data/kana.json) dan
        embedded fallback (js/kanji.js KANJI_FULL_DATA, data/kanji-meta.json).
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 79 Karakter JLPT N5 yang telah diverifikasi secara manual & komprehensif
VERIFIED_N5_KANJI = {
    "一": {
        "meaning": "satu",
        "meaningEn": "One",
        "onyomi": ["イチ", "イツ"],
        "kunyomi": ["ひと", "ひと.つ"],
        "words": [
            {"word": "一つ", "reading": "ひとつ", "meaning": "satu buah"},
            {"word": "一人", "reading": "ひとり", "meaning": "satu orang / sendiri"},
            {"word": "一日", "reading": "ついたち", "meaning": "tanggal satu / satu hari"}
        ],
        "sentence": {
            "japanese": "りんごを一つください。",
            "reading": "りんごを ひとつ ください。",
            "meaning": "Tolong beri saya satu buah apel."
        }
    },
    "七": {
        "meaning": "tujuh",
        "meaningEn": "Seven",
        "onyomi": ["シチ"],
        "kunyomi": ["なな", "なな.つ", "なの"],
        "words": [
            {"word": "七つ", "reading": "ななつ", "meaning": "tujuh buah"},
            {"word": "七時", "reading": "しちじ", "meaning": "jam 7"},
            {"word": "七日", "reading": "なのか", "meaning": "tanggal 7 / tujuh hari"}
        ],
        "sentence": {
            "japanese": "毎朝七時に起きます。",
            "reading": "まいあさ しちじに おきます。",
            "meaning": "Saya bangun setiap pagi jam tujuh."
        }
    },
    "九": {
        "meaning": "sembilan",
        "meaningEn": "Nine",
        "onyomi": ["キュウ", "ク"],
        "kunyomi": ["ここの", "ここの.つ"],
        "words": [
            {"word": "九つ", "reading": "ここのつ", "meaning": "sembilan buah"},
            {"word": "九時", "reading": "くじ", "meaning": "jam 9"},
            {"word": "九月", "reading": "くがつ", "meaning": "bulan September"}
        ],
        "sentence": {
            "japanese": "授業は九時から始まります。",
            "reading": "じゅぎょうは くじから はじまります。",
            "meaning": "Pelajaran dimulai dari jam sembilan."
        }
    },
    "二": {
        "meaning": "dua",
        "meaningEn": "Two",
        "onyomi": ["ニ"],
        "kunyomi": ["ふた", "ふた.つ"],
        "words": [
            {"word": "二つ", "reading": "ふたつ", "meaning": "dua buah"},
            {"word": "二人", "reading": "ふたり", "meaning": "dua orang"},
            {"word": "二月", "reading": "にがつ", "meaning": "bulan Februari"}
        ],
        "sentence": {
            "japanese": "ペンが二本あります。",
            "reading": "ペンが にほん あります。",
            "meaning": "Ada dua buah pulpen."
        }
    },
    "人": {
        "meaning": "orang",
        "meaningEn": "Person",
        "onyomi": ["ジン", "ニン"],
        "kunyomi": ["ひと"],
        "words": [
            {"word": "日本人", "reading": "にほんじん", "meaning": "orang Jepang"},
            {"word": "一人", "reading": "ひとり", "meaning": "satu orang"},
            {"word": "人", "reading": "ひと", "meaning": "orang"}
        ],
        "sentence": {
            "japanese": "あの人は日本語の先生です。",
            "reading": "あの ひとは にほんごの せんせいです。",
            "meaning": "Orang itu adalah guru bahasa Jepang."
        }
    },
    "入": {
        "meaning": "masuk",
        "meaningEn": "Enter, Insert",
        "onyomi": ["ニュウ"],
        "kunyomi": ["はい.る", "い.れる"],
        "words": [
            {"word": "入る", "reading": "はいる", "meaning": "masuk"},
            {"word": "入口", "reading": "いりぐち", "meaning": "pintu masuk"},
            {"word": "入れる", "reading": "いれる", "meaning": "memasukkan"}
        ],
        "sentence": {
            "japanese": "部屋に入ってください。",
            "reading": "へやに はいってください。",
            "meaning": "Silakan masuk ke dalam kamar."
        }
    },
    "八": {
        "meaning": "delapan",
        "meaningEn": "Eight",
        "onyomi": ["ハチ"],
        "kunyomi": ["や", "や.つ", "やっ.つ", "よう"],
        "words": [
            {"word": "八つ", "reading": "やっつ", "meaning": "delapan buah"},
            {"word": "八時", "reading": "はちじ", "meaning": "jam 8"},
            {"word": "八日", "reading": "ようか", "meaning": "tanggal 8 / delapan hari"}
        ],
        "sentence": {
            "japanese": "夜八時に晩ご飯を食べます。",
            "reading": "よる はちじに ばんごはんを たべます。",
            "meaning": "Saya makan malam pada jam delapan malam."
        }
    },
    "十": {
        "meaning": "sepuluh",
        "meaningEn": "Ten",
        "onyomi": ["ジュウ"],
        "kunyomi": ["とお"],
        "words": [
            {"word": "十", "reading": "じゅう", "meaning": "sepuluh"},
            {"word": "十分", "reading": "じゅっぷん", "meaning": "sepuluh menit"},
            {"word": "十日", "reading": "とおか", "meaning": "tanggal 10 / sepuluh hari"}
        ],
        "sentence": {
            "japanese": "あと十分で着きます。",
            "reading": "あと じゅっぷんで つきます。",
            "meaning": "Sepuluh menit lagi akan sampai."
        }
    },
    "三": {
        "meaning": "tiga",
        "meaningEn": "Three",
        "onyomi": ["サン"],
        "kunyomi": ["み", "み.つ", "みっ.つ"],
        "words": [
            {"word": "三つ", "reading": "みっつ", "meaning": "tiga buah"},
            {"word": "三人", "reading": "さんにん", "meaning": "tiga orang"},
            {"word": "三月", "reading": "さんがつ", "meaning": "bulan Maret"}
        ],
        "sentence": {
            "japanese": "教室に学生が三人います。",
            "reading": "きょうしつに がくせいが さんにん います。",
            "meaning": "Ada tiga orang siswa di ruang kelas."
        }
    },
    "上": {
        "meaning": "atas",
        "meaningEn": "Above, Up",
        "onyomi": ["ジョウ"],
        "kunyomi": ["うえ", "あ.がる"],
        "words": [
            {"word": "上", "reading": "うえ", "meaning": "atas"},
            {"word": "上手", "reading": "じょうず", "meaning": "mahir / pandai"}
        ],
        "sentence": {
            "japanese": "机の上に本があります。",
            "reading": "つくえの うえに ほんが あります。",
            "meaning": "Ada buku di atas meja."
        }
    },
    "下": {
        "meaning": "bawah",
        "meaningEn": "Below, Down",
        "onyomi": ["カ", "ゲ"],
        "kunyomi": ["した", "さ.がる"],
        "words": [
            {"word": "下", "reading": "した", "meaning": "bawah"},
            {"word": "地下鉄", "reading": "ちかてつ", "meaning": "kereta bawah tanah"},
            {"word": "下手", "reading": "へた", "meaning": "kurang mahir"}
        ],
        "sentence": {
            "japanese": "猫が椅子の下にいます。",
            "reading": "ねこが いすの したに います。",
            "meaning": "Kucing ada di bawah kursi."
        }
    },
    "千": {
        "meaning": "seribu",
        "meaningEn": "Thousand",
        "onyomi": ["セン"],
        "kunyomi": ["ち"],
        "words": [
            {"word": "千", "reading": "せん", "meaning": "seribu"},
            {"word": "千円", "reading": "せんえん", "meaning": "seribu yen"},
            {"word": "三千", "reading": "さんぜん", "meaning": "tiga ribu"}
        ],
        "sentence": {
            "japanese": "このノートは千円です。",
            "reading": "この ノートは せんえんです。",
            "meaning": "Buku catatan ini harganya seribu yen."
        }
    },
    "土": {
        "meaning": "tanah, hari Sabtu",
        "meaningEn": "Soil, Earth, Saturday",
        "onyomi": ["ド", "ト"],
        "kunyomi": ["つち"],
        "words": [
            {"word": "土曜日", "reading": "どようび", "meaning": "hari Sabtu"},
            {"word": "土地", "reading": "とち", "meaning": "tanah / lahan"}
        ],
        "sentence": {
            "japanese": "土曜日に友達と遊びます。",
            "reading": "どようびに ともだちと あそびます。",
            "meaning": "Saya bermain dengan teman pada hari Sabtu."
        }
    },
    "大": {
        "meaning": "besar",
        "meaningEn": "Large, Big",
        "onyomi": ["ダイ", "タイ"],
        "kunyomi": ["おお.きい"],
        "words": [
            {"word": "大きい", "reading": "おおきい", "meaning": "besar"},
            {"word": "大学", "reading": "だいがく", "meaning": "universitas"},
            {"word": "大学生", "reading": "だいがくせい", "meaning": "mahasiswa"}
        ],
        "sentence": {
            "japanese": "公園に大きい木があります。",
            "reading": "こうえんに おおきい きが あります。",
            "meaning": "Ada pohon besar di taman."
        }
    },
    "女": {
        "meaning": "perempuan, wanita",
        "meaningEn": "Woman, Female",
        "onyomi": ["ジョ"],
        "kunyomi": ["おんな"],
        "words": [
            {"word": "女の子", "reading": "おんなのこ", "meaning": "anak perempuan"},
            {"word": "女の人", "reading": "おんなのひと", "meaning": "wanita / perempuan"},
            {"word": "女性", "reading": "じょせい", "meaning": "wanita"}
        ],
        "sentence": {
            "japanese": "あそこに女の人が立っています。",
            "reading": "あそこに おんなのひとが たっています。",
            "meaning": "Di sana ada seorang wanita yang sedang berdiri."
        }
    },
    "子": {
        "meaning": "anak",
        "meaningEn": "Child",
        "onyomi": ["シ"],
        "kunyomi": ["こ"],
        "words": [
            {"word": "子ども", "reading": "こども", "meaning": "anak-anak"},
            {"word": "女の子", "reading": "おんなのこ", "meaning": "anak perempuan"},
            {"word": "男の子", "reading": "おとこのこ", "meaning": "anak laki-laki"}
        ],
        "sentence": {
            "japanese": "公園で子どもたちが遊んでいます。",
            "reading": "こうえんで こどもたちが あそんでいます。",
            "meaning": "Anak-anak sedang bermain di taman."
        }
    },
    "小": {
        "meaning": "kecil",
        "meaningEn": "Little, Small",
        "onyomi": ["ショウ"],
        "kunyomi": ["ちい.さい"],
        "words": [
            {"word": "小さい", "reading": "ちいさい", "meaning": "kecil"},
            {"word": "小学校", "reading": "しょうがっこう", "meaning": "sekolah dasar"},
            {"word": "小川", "reading": "おがわ", "meaning": "anak sungai"}
        ],
        "sentence": {
            "japanese": "庭に小さい花が咲いています。",
            "reading": "にわに ちいさい はなが さいています。",
            "meaning": "Bunga kecil sedang mekar di halaman."
        }
    },
    "山": {
        "meaning": "gunung",
        "meaningEn": "Mountain",
        "onyomi": ["サン"],
        "kunyomi": ["やま"],
        "words": [
            {"word": "山", "reading": "やま", "meaning": "gunung"},
            {"word": "富士山", "reading": "ふじさん", "meaning": "Gunung Fuji"},
            {"word": "山登り", "reading": "やまのぼり", "meaning": "mendaki gunung"}
        ],
        "sentence": {
            "japanese": "週末に山へ登りました。",
            "reading": "しゅうまつに やまへ のぼりました。",
            "meaning": "Akhir pekan kemarin saya mendaki gunung."
        }
    },
    "川": {
        "meaning": "sungai",
        "meaningEn": "River, Stream",
        "onyomi": ["セン"],
        "kunyomi": ["かわ"],
        "words": [
            {"word": "川", "reading": "かわ", "meaning": "sungai"},
            {"word": "ナイル川", "reading": "ナイルがわ", "meaning": "Sungai Nil"}
        ],
        "sentence": {
            "japanese": "川の水はとてもきれいです。",
            "reading": "かわの みずは とても きれいです。",
            "meaning": "Air sungainya sangat bersih."
        }
    },
    "万": {
        "meaning": "sepuluh ribu (10.000)",
        "meaningEn": "Ten Thousand, 10,000",
        "onyomi": ["マン", "バン"],
        "kunyomi": ["よろず"],
        "words": [
            {"word": "一万", "reading": "いちまん", "meaning": "sepuluh ribu"},
            {"word": "一万円", "reading": "いちまんえん", "meaning": "sepuluh ribu yen"},
            {"word": "万国", "reading": "ばんこく", "meaning": "semua bangsa"}
        ],
        "sentence": {
            "japanese": "この辞書は一万円でした。",
            "reading": "この じしょは いちまんえん でした。",
            "meaning": "Kamus ini harganya sepuluh ribu yen."
        }
    },
    "中": {
        "meaning": "tengah, dalam",
        "meaningEn": "In, Inside, Middle",
        "onyomi": ["チュウ"],
        "kunyomi": ["なか"],
        "words": [
            {"word": "中", "reading": "なか", "meaning": "dalam"},
            {"word": "一日中", "reading": "いちにちじゅう", "meaning": "sepanjang hari"},
            {"word": "中国", "reading": "ちゅうごく", "meaning": "Tiongkok"}
        ],
        "sentence": {
            "japanese": "かばんの中に財布があります。",
            "reading": "かばんの なかに さいふが あります。",
            "meaning": "Ada dompet di dalam tas."
        }
    },
    "五": {
        "meaning": "lima",
        "meaningEn": "Five",
        "onyomi": ["ゴ"],
        "kunyomi": ["いつ", "いつ.つ"],
        "words": [
            {"word": "五つ", "reading": "いつつ", "meaning": "lima buah"},
            {"word": "五時", "reading": "ごじ", "meaning": "jam 5"},
            {"word": "五月", "reading": "ごがつ", "meaning": "bulan Mei"}
        ],
        "sentence": {
            "japanese": "五時に図書館で会いましょう。",
            "reading": "ごじに としょかんで あいましょう。",
            "meaning": "Mari bertemu di perpustakaan pada jam lima."
        }
    },
    "六": {
        "meaning": "enam",
        "meaningEn": "Six",
        "onyomi": ["ロク"],
        "kunyomi": ["む", "む.つ", "むっ.つ", "むい"],
        "words": [
            {"word": "六つ", "reading": "むっつ", "meaning": "enam buah"},
            {"word": "六時", "reading": "ろくじ", "meaning": "jam 6"},
            {"word": "六日", "reading": "むいか", "meaning": "tanggal 6 / enam hari"}
        ],
        "sentence": {
            "japanese": "毎朝六時にジョギングをします。",
            "reading": "まいあさ ろくじに ジョギングを します。",
            "meaning": "Setiap pagi jam enam saya lari pagi."
        }
    },
    "円": {
        "meaning": "yen, lingkaran",
        "meaningEn": "Yen, Circle, Round",
        "onyomi": ["エン"],
        "kunyomi": ["まる.い"],
        "words": [
            {"word": "百円", "reading": "ひゃくえん", "meaning": "100 yen"},
            {"word": "千円", "reading": "せんえん", "meaning": "1000 yen"},
            {"word": "円", "reading": "えん", "meaning": "yen (mata uang Jepang)"}
        ],
        "sentence": {
            "japanese": "このお茶は百円です。",
            "reading": "この おちゃは ひゃくえんです。",
            "meaning": "Teh hijau ini harganya seratus yen."
        }
    },
    "天": {
        "meaning": "langit, surga",
        "meaningEn": "Heavens, Sky",
        "onyomi": ["テン"],
        "kunyomi": ["あめ", "あま"],
        "words": [
            {"word": "天気", "reading": "てんき", "meaning": "cuaca"},
            {"word": "天国", "reading": "てんごく", "meaning": "surga"},
            {"word": "天ぷら", "reading": "てんぷら", "meaning": "tempura"}
        ],
        "sentence": {
            "japanese": "今日の天気はとてもいいです。",
            "reading": "きょうの てんきは とても いいです。",
            "meaning": "Cuaca hari ini sangat cerah."
        }
    },
    "日": {
        "meaning": "hari, matahari",
        "meaningEn": "Day, Sun, Japan",
        "onyomi": ["ニチ", "ジツ"],
        "kunyomi": ["ひ", "か"],
        "words": [
            {"word": "日本", "reading": "にほん", "meaning": "Jepang"},
            {"word": "日曜日", "reading": "にちようび", "meaning": "hari Minggu"},
            {"word": "今日", "reading": "きょう", "meaning": "hari ini"}
        ],
        "sentence": {
            "japanese": "今日は日曜日です。",
            "reading": "きょうは にちようび です。",
            "meaning": "Hari ini adalah hari Minggu."
        }
    },
    "月": {
        "meaning": "bulan",
        "meaningEn": "Month, Moon",
        "onyomi": ["ゲツ", "ガツ"],
        "kunyomi": ["つき"],
        "words": [
            {"word": "月曜日", "reading": "げつようび", "meaning": "hari Senin"},
            {"word": "今月", "reading": "こんげつ", "meaning": "bulan ini"},
            {"word": "一月", "reading": "いちがつ", "meaning": "bulan Januari"}
        ],
        "sentence": {
            "japanese": "今夜は月がとても明るいです。",
            "reading": "こんやは つきが とても あかるいです。",
            "meaning": "Malam ini bulannya sangat terang."
        }
    },
    "木": {
        "meaning": "pohon, kayu",
        "meaningEn": "Tree, Wood",
        "onyomi": ["モク", "ボク"],
        "kunyomi": ["き"],
        "words": [
            {"word": "木", "reading": "き", "meaning": "pohon"},
            {"word": "木曜日", "reading": "もくようび", "meaning": "hari Kamis"},
            {"word": "木材", "reading": "もくざい", "meaning": "kayu bangunan"}
        ],
        "sentence": {
            "japanese": "庭の木に鳥がいます。",
            "reading": "にわの きに とりが います。",
            "meaning": "Ada burung di pohon taman."
        }
    },
    "水": {
        "meaning": "air",
        "meaningEn": "Water",
        "onyomi": ["スイ"],
        "kunyomi": ["みず"],
        "words": [
            {"word": "水", "reading": "みず", "meaning": "air dingin/tawar"},
            {"word": "水曜日", "reading": "すいようび", "meaning": "hari Rabu"},
            {"word": "水泳", "reading": "すいえい", "meaning": "renang"}
        ],
        "sentence": {
            "japanese": "冷たい水を一杯飲みました。",
            "reading": "つめたい みずを いっぱい のみました。",
            "meaning": "Saya meminum segelas air dingin."
        }
    },
    "火": {
        "meaning": "api",
        "meaningEn": "Fire",
        "onyomi": ["カ"],
        "kunyomi": ["ひ"],
        "words": [
            {"word": "火曜日", "reading": "かようび", "meaning": "hari Selasa"},
            {"word": "火山", "reading": "かざん", "meaning": "gunung berapi"},
            {"word": "火事", "reading": "かじ", "meaning": "kebakaran"}
        ],
        "sentence": {
            "japanese": "火曜日に日本語のテストがあります。",
            "reading": "かようびに にほんごの テストが あります。",
            "meaning": "Pada hari Selasa ada ujian bahasa Jepang."
        }
    },
    "今": {
        "meaning": "sekarang",
        "meaningEn": "Now",
        "onyomi": ["コン"],
        "kunyomi": ["いま"],
        "words": [
            {"word": "今", "reading": "いま", "meaning": "sekarang"},
            {"word": "今日", "reading": "きょう", "meaning": "hari ini"},
            {"word": "今週", "reading": "こんしゅう", "meaning": "minggu ini"}
        ],
        "sentence": {
            "japanese": "今何時ですか。",
            "reading": "いま なんじ ですか。",
            "meaning": "Sekarang jam berapa?"
        }
    },
    "午": {
        "meaning": "tengah hari, siang",
        "meaningEn": "Noon",
        "onyomi": ["ゴ"],
        "kunyomi": ["うま"],
        "words": [
            {"word": "午前", "reading": "ごぜん", "meaning": "pagi / a.m."},
            {"word": "午後", "reading": "ごご", "meaning": "siang-malam / p.m."},
            {"word": "正午", "reading": "しょうご", "meaning": "tengah hari / jam 12 siang"}
        ],
        "sentence": {
            "japanese": "明日の午後、図書館へ行きます。",
            "reading": "あしたの ごご、としょかんへ いきます。",
            "meaning": "Besok siang saya akan pergi ke perpustakaan."
        }
    },
    "友": {
        "meaning": "teman",
        "meaningEn": "Friend",
        "onyomi": ["ユウ"],
        "kunyomi": ["とも"],
        "words": [
            {"word": "友達", "reading": "ともだち", "meaning": "teman"},
            {"word": "友人", "reading": "ゆうじん", "meaning": "sahabat / rekan"},
            {"word": "親友", "reading": "しんゆう", "meaning": "sahabat karib"}
        ],
        "sentence": {
            "japanese": "週末に友達と映画を見ました。",
            "reading": "しゅうまつに ともだちと えいがを みました。",
            "meaning": "Akhir pekan kemarin saya menonton film bersama teman."
        }
    },
    "父": {
        "meaning": "ayah (sendiri)",
        "meaningEn": "Father",
        "onyomi": ["フ"],
        "kunyomi": ["ちち"],
        "words": [
            {"word": "父", "reading": "ちち", "meaning": "ayah saya"},
            {"word": "お父さん", "reading": "おとうさん", "meaning": "ayah / bapak"},
            {"word": "父母", "reading": "ふぼ", "meaning": "orang tua"}
        ],
        "sentence": {
            "japanese": "私の父は毎朝新聞を読みます。",
            "reading": "わたしの ちちは まいあさ しんぶんを よみます。",
            "meaning": "Ayah saya membaca koran setiap pagi."
        }
    },
    "出": {
        "meaning": "keluar",
        "meaningEn": "Exit, Leave, Go Out",
        "onyomi": ["シュツ"],
        "kunyomi": ["で.る", "だ.す"],
        "words": [
            {"word": "出る", "reading": "でる", "meaning": "keluar"},
            {"word": "出口", "reading": "でぐち", "meaning": "pintu keluar"},
            {"word": "出す", "reading": "だす", "meaning": "mengeluarkan / mengumpulkan"}
        ],
        "sentence": {
            "japanese": "毎朝七時に家を出ます。",
            "reading": "まいあさ しちじに いえを でます。",
            "meaning": "Saya keluar rumah setiap pagi pada jam tujuh."
        }
    },
    "右": {
        "meaning": "kanan",
        "meaningEn": "Right",
        "onyomi": ["ウ", "ユウ"],
        "kunyomi": ["みぎ"],
        "words": [
            {"word": "右", "reading": "みぎ", "meaning": "kanan"},
            {"word": "右手", "reading": "みぎて", "meaning": "tangan kanan"},
            {"word": "右側", "reading": "みぎがわ", "meaning": "sebelah kanan"}
        ],
        "sentence": {
            "japanese": "次の角を右へ曲がってください。",
            "reading": "つぎの かどを みぎへ まがってください。",
            "meaning": "Silakan belok kanan di tikungan berikutnya."
        }
    },
    "四": {
        "meaning": "empat",
        "meaningEn": "Four",
        "onyomi": ["シ"],
        "kunyomi": ["よ", "よ.つ", "よっ.つ", "よん"],
        "words": [
            {"word": "四", "reading": "よん", "meaning": "empat"},
            {"word": "四時", "reading": "よじ", "meaning": "jam 4"},
            {"word": "四季", "reading": "しき", "meaning": "empat musim"}
        ],
        "sentence": {
            "japanese": "日本には美しい四季があります。",
            "reading": "にほんには うつくしい しきが あります。",
            "meaning": "Di Jepang ada empat musim yang indah."
        }
    },
    "左": {
        "meaning": "kiri",
        "meaningEn": "Left",
        "onyomi": ["サ"],
        "kunyomi": ["ひだり"],
        "words": [
            {"word": "左", "reading": "ひだり", "meaning": "kiri"},
            {"word": "左手", "reading": "ひだりて", "meaning": "tangan kiri"},
            {"word": "左側", "reading": "ひだりがわ", "meaning": "sebelah kiri"}
        ],
        "sentence": {
            "japanese": "郵便局は駅の左側にあります。",
            "reading": "ゆうびんきょくは えきの ひだりがわに あります。",
            "meaning": "Kantor pos ada di sebelah kiri stasiun."
        }
    },
    "本": {
        "meaning": "buku, asal",
        "meaningEn": "Book, Origin, Main",
        "onyomi": ["ホン"],
        "kunyomi": ["もと"],
        "words": [
            {"word": "本", "reading": "ほん", "meaning": "buku"},
            {"word": "日本", "reading": "にほん", "meaning": "Jepang"},
            {"word": "本屋", "reading": "ほんや", "meaning": "toko buku"}
        ],
        "sentence": {
            "japanese": "図書館で日本語の本を借りました。",
            "reading": "としょかんで にほんごの ほんを かりました。",
            "meaning": "Saya meminjam buku bahasa Jepang di perpustakaan."
        }
    },
    "生": {
        "meaning": "hidup, lahir, murid",
        "meaningEn": "Life, Birth, Student",
        "onyomi": ["セイ", "ショウ"],
        "kunyomi": ["い.きる", "う.まれる", "なま"],
        "words": [
            {"word": "学生", "reading": "がくせい", "meaning": "murid / pelajar"},
            {"word": "先生", "reading": "せんせい", "meaning": "guru"},
            {"word": "生まれる", "reading": "うまれる", "meaning": "lahir"}
        ],
        "sentence": {
            "japanese": "私は高校生です。",
            "reading": "わたしは こうこうせいです。",
            "meaning": "Saya adalah siswa SMA."
        }
    },
    "白": {
        "meaning": "putih",
        "meaningEn": "White",
        "onyomi": ["ハク"],
        "kunyomi": ["しろ", "しろ.い"],
        "words": [
            {"word": "白い", "reading": "しろい", "meaning": "putih"},
            {"word": "白", "reading": "しろ", "meaning": "warna putih"},
            {"word": "面白い", "reading": "おもしろい", "meaning": "menarik / seru"}
        ],
        "sentence": {
            "japanese": "白い猫が庭で寝ています。",
            "reading": "しろい ねこが にわで ねています。",
            "meaning": "Kucing putih sedang tidur di halaman."
        }
    },
    "北": {
        "meaning": "utara",
        "meaningEn": "North",
        "onyomi": ["ホク"],
        "kunyomi": ["きた"],
        "words": [
            {"word": "北", "reading": "きた", "meaning": "utara"},
            {"word": "北口", "reading": "きたぐち", "meaning": "pintu keluar utara"},
            {"word": "北海道", "reading": "ほっかいどう", "meaning": "Hokkaido"}
        ],
        "sentence": {
            "japanese": "冬休みに北海道へ旅行します。",
            "reading": "ふゆやすみに ほっかいどうへ りょこうします。",
            "meaning": "Pada liburan musim dingin saya akan berlibur ke Hokkaido."
        }
    },
    "半": {
        "meaning": "setengah, separuh",
        "meaningEn": "Half",
        "onyomi": ["ハン"],
        "kunyomi": ["なか.ば"],
        "words": [
            {"word": "半分", "reading": "はんぶん", "meaning": "setengah bagian"},
            {"word": "八時半", "reading": "はちじはん", "meaning": "jam 8 lewat 30 menit / setengah sembilan"},
            {"word": "半年", "reading": "はんとし", "meaning": "setengah tahun"}
        ],
        "sentence": {
            "japanese": "学校は八時半に始まります。",
            "reading": "がっこうは はちじはんに はじまります。",
            "meaning": "Sekolah dimulai pada pukul setengah sembilan (08.30)."
        }
    },
    "外": {
        "meaning": "luar",
        "meaningEn": "Outside",
        "onyomi": ["ガイ", "ゲ"],
        "kunyomi": ["そと", "ほか"],
        "words": [
            {"word": "外", "reading": "そと", "meaning": "luar"},
            {"word": "外国", "reading": "がいこく", "meaning": "luar negeri"},
            {"word": "外国人", "reading": "がいこくじん", "meaning": "orang asing"}
        ],
        "sentence": {
            "japanese": "外は雨が降っています。",
            "reading": "そとは あめが ふっています。",
            "meaning": "Di luar sedang turun hujan."
        }
    },
    "母": {
        "meaning": "ibu (sendiri)",
        "meaningEn": "Mother",
        "onyomi": ["ボ"],
        "kunyomi": ["はは"],
        "words": [
            {"word": "母", "reading": "はは", "meaning": "ibu saya"},
            {"word": "お母さん", "reading": "おかあさん", "meaning": "ibu / mama"},
            {"word": "父母", "reading": "ふぼ", "meaning": "orang tua"}
        ],
        "sentence": {
            "japanese": "母は料理がとても上手です。",
            "reading": "ははは りょうりが とても じょうずです。",
            "meaning": "Ibu saya sangat pandai memasak."
        }
    },
    "休": {
        "meaning": "istirahat, libur",
        "meaningEn": "Rest, Day Off",
        "onyomi": ["キュウ"],
        "kunyomi": ["やす.む", "やす.み"],
        "words": [
            {"word": "休む", "reading": "やすむ", "meaning": "beristirahat / libur"},
            {"word": "休み", "reading": "やすみ", "meaning": "libur / istirahat"},
            {"word": "夏休み", "reading": "なつやすみ", "meaning": "liburan musim panas"}
        ],
        "sentence": {
            "japanese": "少し休みましょう。",
            "reading": "すこし やすみましょう。",
            "meaning": "Mari beristirahat sebentar."
        }
    },
    "先": {
        "meaning": "sebelumnya, ujung, depan",
        "meaningEn": "Before, Ahead, Previous",
        "onyomi": ["セン"],
        "kunyomi": ["さき"],
        "words": [
            {"word": "先生", "reading": "せんせい", "meaning": "guru"},
            {"word": "先週", "reading": "せんしゅう", "meaning": "minggu lalu"},
            {"word": "お先に", "reading": "おさきに", "meaning": "duluan"}
        ],
        "sentence": {
            "japanese": "先生に質問をしました。",
            "reading": "せんせいに しつもんを しました。",
            "meaning": "Saya mengajukan pertanyaan kepada guru."
        }
    },
    "名": {
        "meaning": "nama",
        "meaningEn": "Name, Noted",
        "onyomi": ["メイ", "ミョウ"],
        "kunyomi": ["な"],
        "words": [
            {"word": "名前", "reading": "なまえ", "meaning": "nama"},
            {"word": "有名", "reading": "ゆうめい", "meaning": "terkenal"},
            {"word": "名字", "reading": "みょうじ", "meaning": "nama keluarga / marga"}
        ],
        "sentence": {
            "japanese": "お名前を教えてください。",
            "reading": "おなまえを おしえて ください。",
            "meaning": "Tolong beri tahu nama Anda."
        }
    },
    "年": {
        "meaning": "tahun",
        "meaningEn": "Year",
        "onyomi": ["ネン"],
        "kunyomi": ["とし"],
        "words": [
            {"word": "今年", "reading": "ことし", "meaning": "tahun ini"},
            {"word": "来年", "reading": "らいねん", "meaning": "tahun depan"},
            {"word": "去年", "reading": "きょねん", "meaning": "tahun lalu"}
        ],
        "sentence": {
            "japanese": "来年日本へ行きたいです。",
            "reading": "らいねん にほんへ いきたいです。",
            "meaning": "Tahun depan saya ingin pergi ke Jepang."
        }
    },
    "気": {
        "meaning": "udara, semangat, perasaan",
        "meaningEn": "Spirit, Mind, Air",
        "onyomi": ["キ"],
        "kunyomi": ["き"],
        "words": [
            {"word": "元気", "reading": "げんき", "meaning": "sehat / bersemangat"},
            {"word": "天気", "reading": "てんき", "meaning": "cuaca"},
            {"word": "気をつける", "reading": "きをつける", "meaning": "berhati-hati"}
        ],
        "sentence": {
            "japanese": "お元気ですか。",
            "reading": "おげんき ですか。",
            "meaning": "Apa kabar? (Apakah sehat?)"
        }
    },
    "百": {
        "meaning": "ratus",
        "meaningEn": "Hundred",
        "onyomi": ["ヒャク"],
        "kunyomi": ["もも"],
        "words": [
            {"word": "百", "reading": "ひゃく", "meaning": "seratus"},
            {"word": "百円", "reading": "ひゃくえん", "meaning": "seratus yen"},
            {"word": "三百", "reading": "さんびゃく", "meaning": "tiga ratus"}
        ],
        "sentence": {
            "japanese": "このペンは百円です。",
            "reading": "この ペンは ひゃくえんです。",
            "meaning": "Pulpen ini harganya seratus yen."
        }
    },
    "毎": {
        "meaning": "setiap",
        "meaningEn": "Every",
        "onyomi": ["マイ"],
        "kunyomi": ["ごと"],
        "words": [
            {"word": "毎日", "reading": "まいにち", "meaning": "setiap hari"},
            {"word": "毎朝", "reading": "まいあさ", "meaning": "setiap pagi"},
            {"word": "毎週", "reading": "まいしゅう", "meaning": "setiap minggu"}
        ],
        "sentence": {
            "japanese": "毎日日本語を勉強しています。",
            "reading": "まいにち にほんごを べんきょうしています。",
            "meaning": "Setiap hari saya belajar bahasa Jepang."
        }
    },
    "行": {
        "meaning": "pergi, melakukan",
        "meaningEn": "Going, Journey, Carry Out",
        "onyomi": ["コウ", "ギョウ"],
        "kunyomi": ["い.く", "おこな.う"],
        "words": [
            {"word": "行く", "reading": "いく", "meaning": "pergi"},
            {"word": "銀行", "reading": "ぎんこう", "meaning": "bank"},
            {"word": "旅行", "reading": "りょこう", "meaning": "tamasya / wisata"}
        ],
        "sentence": {
            "japanese": "明日友達と図書館へ行きます。",
            "reading": "あした ともだちと としょかんへ いきます。",
            "meaning": "Besok saya pergi ke perpustakaan bersama teman."
        }
    },
    "西": {
        "meaning": "barat",
        "meaningEn": "West",
        "onyomi": ["セイ", "サイ"],
        "kunyomi": ["にし"],
        "words": [
            {"word": "西", "reading": "にし", "meaning": "barat"},
            {"word": "西口", "reading": "にしぐち", "meaning": "pintu keluar barat"},
            {"word": "関西", "reading": "かんさい", "meaning": "wilayah Kansai"}
        ],
        "sentence": {
            "japanese": "太陽は西に沈みます。",
            "reading": "たいようは にしに しずみます。",
            "meaning": "Matahari terbenam di sebelah barat."
        }
    },
    "男": {
        "meaning": "laki-laki, pria",
        "meaningEn": "Male",
        "onyomi": ["ダン", "ナン"],
        "kunyomi": ["おとこ"],
        "words": [
            {"word": "男の子", "reading": "おとこのこ", "meaning": "anak laki-laki"},
            {"word": "男の人", "reading": "おとこのひと", "meaning": "pria / laki-laki"},
            {"word": "男性", "reading": "だんせい", "meaning": "pria"}
        ],
        "sentence": {
            "japanese": "男の子がサッカーをしています。",
            "reading": "おとこのこが サッカーを しています。",
            "meaning": "Anak laki-laki sedang bermain sepak bola."
        }
    },
    "見": {
        "meaning": "melihat",
        "meaningEn": "See, Look",
        "onyomi": ["ケン"],
        "kunyomi": ["み.る", "み.える", "み.せる"],
        "words": [
            {"word": "見る", "reading": "みる", "meaning": "melihat / menonton"},
            {"word": "見せる", "reading": "みせる", "meaning": "memperlihatkan"},
            {"word": "花見", "reading": "はなみ", "meaning": "melihat bunga sakura"}
        ],
        "sentence": {
            "japanese": "昨日面白い映画を見ました。",
            "reading": "きのう おもしろい えいがを みました。",
            "meaning": "Kemarin saya menonton film yang menarik."
        }
    },
    "車": {
        "meaning": "mobil, kendaraan",
        "meaningEn": "Car, Vehicle",
        "onyomi": ["シャ"],
        "kunyomi": ["くるま"],
        "words": [
            {"word": "車", "reading": "くるま", "meaning": "mobil"},
            {"word": "電車", "reading": "でんしゃ", "meaning": "kereta listrik"},
            {"word": "自転車", "reading": "じてんしゃ", "meaning": "sepeda"}
        ],
        "sentence": {
            "japanese": "父は毎日車で仕事に行きます。",
            "reading": "ちちは まいにち くるまで しごとに いきます。",
            "meaning": "Ayah setiap hari pergi bekerja naik mobil."
        }
    },
    "何": {
        "meaning": "apa",
        "meaningEn": "What",
        "onyomi": ["カ"],
        "kunyomi": ["なに", "なん"],
        "words": [
            {"word": "何", "reading": "なに", "meaning": "apa"},
            {"word": "何時", "reading": "なんじ", "meaning": "jam berapa"},
            {"word": "何人", "reading": "なんにん", "meaning": "berapa orang"}
        ],
        "sentence": {
            "japanese": "今何をしていますか。",
            "reading": "いま なにを していますか。",
            "meaning": "Sekarang kamu sedang apa?"
        }
    },
    "来": {
        "meaning": "datang, masa depan",
        "meaningEn": "Come, Next",
        "onyomi": ["ライ"],
        "kunyomi": ["く.る", "き.たる"],
        "words": [
            {"word": "来る", "reading": "くる", "meaning": "datang"},
            {"word": "来年", "reading": "らいねん", "meaning": "tahun depan"},
            {"word": "来週", "reading": "らいしゅう", "meaning": "minggu depan"}
        ],
        "sentence": {
            "japanese": "明日は早く学校へ来てください。",
            "reading": "あしたは はやく がっこうへ きてください。",
            "meaning": "Besok silakan datang lebih awal ke sekolah."
        }
    },
    "学": {
        "meaning": "belajar, ilmu",
        "meaningEn": "Study, Learning, Science",
        "onyomi": ["ガク"],
        "kunyomi": ["まな.ぶ"],
        "words": [
            {"word": "学生", "reading": "がくせい", "meaning": "murid"},
            {"word": "学校", "reading": "がっこう", "meaning": "sekolah"},
            {"word": "大学", "reading": "だいがく", "meaning": "universitas"}
        ],
        "sentence": {
            "japanese": "大学で日本語を勉強します。",
            "reading": "だいがくで にほんごを べんきょうします。",
            "meaning": "Saya belajar bahasa Jepang di universitas."
        }
    },
    "金": {
        "meaning": "emas, uang, hari Jumat",
        "meaningEn": "Gold, Money, Friday",
        "onyomi": ["キン", "コン"],
        "kunyomi": ["かね"],
        "words": [
            {"word": "お金", "reading": "おかね", "meaning": "uang"},
            {"word": "金曜日", "reading": "きんようび", "meaning": "hari Jumat"},
            {"word": "料金", "reading": "りょうきん", "meaning": "tarif / biaya"}
        ],
        "sentence": {
            "japanese": "金曜日にテストがあります。",
            "reading": "きんようびに テストが あります。",
            "meaning": "Ada ujian pada hari Jumat."
        }
    },
    "雨": {
        "meaning": "hujan",
        "meaningEn": "Rain",
        "onyomi": ["ウ"],
        "kunyomi": ["あめ", "あま"],
        "words": [
            {"word": "雨", "reading": "あめ", "meaning": "hujan"},
            {"word": "大雨", "reading": "おおあめ", "meaning": "hujan lebat"},
            {"word": "雨具", "reading": "あまぐ", "meaning": "jas hujan / payung"}
        ],
        "sentence": {
            "japanese": "今日は朝から雨が降っています。",
            "reading": "きょうは あさから あめが ふっています。",
            "meaning": "Hari ini hujan turun sejak pagi."
        }
    },
    "国": {
        "meaning": "negara",
        "meaningEn": "Country",
        "onyomi": ["コク"],
        "kunyomi": ["くに"],
        "words": [
            {"word": "国", "reading": "くに", "meaning": "negara"},
            {"word": "外国", "reading": "がいこく", "meaning": "luar negeri"},
            {"word": "中国", "reading": "ちゅうごく", "meaning": "Tiongkok"}
        ],
        "sentence": {
            "japanese": "お国はどちらですか。",
            "reading": "おくには どちら ですか。",
            "meaning": "Anda berasal dari negara mana?"
        }
    },
    "東": {
        "meaning": "timur",
        "meaningEn": "East",
        "onyomi": ["トウ"],
        "kunyomi": ["ひがし"],
        "words": [
            {"word": "東", "reading": "ひがし", "meaning": "timur"},
            {"word": "東京", "reading": "とうきょう", "meaning": "Tokyo"},
            {"word": "東口", "reading": "ひがしぐち", "meaning": "pintu keluar timur"}
        ],
        "sentence": {
            "japanese": "太陽は東から昇ります。",
            "reading": "たいようは ひがしから のぼります。",
            "meaning": "Matahari terbit dari timur."
        }
    },
    "長": {
        "meaning": "panjang, ketua",
        "meaningEn": "Long, Leader",
        "onyomi": ["チョウ"],
        "kunyomi": ["なが.い"],
        "words": [
            {"word": "長い", "reading": "ながい", "meaning": "panjang"},
            {"word": "校長", "reading": "こうちょう", "meaning": "kepala sekolah"},
            {"word": "社長", "reading": "しゃちょう", "meaning": "direktur perusahaan"}
        ],
        "sentence": {
            "japanese": "この川はとても長いです。",
            "reading": "この かわは とても ながいです。",
            "meaning": "Sungai ini sangat panjang."
        }
    },
    "前": {
        "meaning": "depan, sebelum",
        "meaningEn": "Before, Front",
        "onyomi": ["ゼン"],
        "kunyomi": ["まえ"],
        "words": [
            {"word": "前", "reading": "まえ", "meaning": "depan / sebelum"},
            {"word": "午前", "reading": "ごぜん", "meaning": "pagi / a.m."},
            {"word": "名前", "reading": "なまえ", "meaning": "nama"}
        ],
        "sentence": {
            "japanese": "駅の前に大きいスーパーがあります。",
            "reading": "えきの まえに おおきい スーパーが あります。",
            "meaning": "Ada supermarket besar di depan stasiun."
        }
    },
    "南": {
        "meaning": "selatan",
        "meaningEn": "South",
        "onyomi": ["ナン"],
        "kunyomi": ["みなみ"],
        "words": [
            {"word": "南", "reading": "みなみ", "meaning": "selatan"},
            {"word": "南口", "reading": "みなみぐち", "meaning": "pintu keluar selatan"},
            {"word": "東南アジア", "reading": "とうなんアジア", "meaning": "Asia Tenggara"}
        ],
        "sentence": {
            "japanese": "窓を開けると南風が入ってきます。",
            "reading": "まどを あけると みなみかぜが はいってきます。",
            "meaning": "Saat membuka jendela, angin selatan berhembus masuk."
        }
    },
    "後": {
        "meaning": "belakang, setelah",
        "meaningEn": "Behind, After",
        "onyomi": ["ゴ", "コウ"],
        "kunyomi": ["のち", "うし.ろ", "あと"],
        "words": [
            {"word": "後ろ", "reading": "うしろ", "meaning": "belakang"},
            {"word": "午後", "reading": "ごご", "meaning": "sore-malam / p.m."},
            {"word": "後で", "reading": "あとで", "meaning": "nanti"}
        ],
        "sentence": {
            "japanese": "ご飯を食べた後で散歩します。",
            "reading": "ごはんを たべた あとで さんぽします。",
            "meaning": "Setelah makan saya berjalan-jalan."
        }
    },
    "食": {
        "meaning": "makan, makanan",
        "meaningEn": "Eat, Food",
        "onyomi": ["ショク"],
        "kunyomi": ["た.べる", "く.う"],
        "words": [
            {"word": "食べる", "reading": "たべる", "meaning": "makan"},
            {"word": "食事", "reading": "しょくじ", "meaning": "makan / santapan"},
            {"word": "朝食", "reading": "ちょうしょく", "meaning": "sarapan"}
        ],
        "sentence": {
            "japanese": "毎日朝ご飯を食べます。",
            "reading": "まいにち あさごはんを たべます。",
            "meaning": "Saya makan sarapan setiap hari."
        }
    },
    "校": {
        "meaning": "sekolah",
        "meaningEn": "School",
        "onyomi": ["コウ"],
        "kunyomi": [],
        "words": [
            {"word": "学校", "reading": "がっこう", "meaning": "sekolah"},
            {"word": "高校", "reading": "こうこう", "meaning": "SMA"},
            {"word": "中学校", "reading": "ちゅうがっこう", "meaning": "SMP"}
        ],
        "sentence": {
            "japanese": "私たちは同じ高校の生徒です。",
            "reading": "わたしたちは おなじ こうこうの せいとです。",
            "meaning": "Kami adalah murid dari SMA yang sama."
        }
    },
    "時": {
        "meaning": "waktu, jam",
        "meaningEn": "Time, Hour",
        "onyomi": ["ジ"],
        "kunyomi": ["とき"],
        "words": [
            {"word": "時間", "reading": "じかん", "meaning": "waktu / durasi"},
            {"word": "時計", "reading": "とけい", "meaning": "jam tangan / dinding"},
            {"word": "時々", "reading": "ときどき", "meaning": "kadang-kadang"}
        ],
        "sentence": {
            "japanese": "今は時間がありません。",
            "reading": "いまは じかんが ありません。",
            "meaning": "Sekarang saya tidak punya waktu."
        }
    },
    "書": {
        "meaning": "menulis",
        "meaningEn": "Write",
        "onyomi": ["ショ"],
        "kunyomi": ["か.く"],
        "words": [
            {"word": "書く", "reading": "かく", "meaning": "menulis"},
            {"word": "読書", "reading": "どくしょ", "meaning": "membaca buku"},
            {"word": "図書館", "reading": "としょかん", "meaning": "perpustakaan"}
        ],
        "sentence": {
            "japanese": "ノートに新しい漢字を書きます。",
            "reading": "ノートに あたらしい かんじを かきます。",
            "meaning": "Saya menulis kanji baru di buku catatan."
        }
    },
    "高": {
        "meaning": "tinggi, mahal",
        "meaningEn": "Tall, High, Expensive",
        "onyomi": ["コウ"],
        "kunyomi": ["たか.い"],
        "words": [
            {"word": "高い", "reading": "たかい", "meaning": "tinggi / mahal"},
            {"word": "高校", "reading": "こうこう", "meaning": "SMA"},
            {"word": "高校生", "reading": "こうこうせい", "meaning": "siswa SMA"}
        ],
        "sentence": {
            "japanese": "あのビルはとても高いです。",
            "reading": "あの ビルは とても たかいです。",
            "meaning": "Gedung itu sangat tinggi."
        }
    },
    "間": {
        "meaning": "antara, waktu, jeda",
        "meaningEn": "Interval, Space, Between",
        "onyomi": ["カン", "ケン"],
        "kunyomi": ["あいだ", "ま"],
        "words": [
            {"word": "間", "reading": "あいだ", "meaning": "antara / di sela"},
            {"word": "時間", "reading": "じかん", "meaning": "waktu"},
            {"word": "一週間", "reading": "いっしゅうかん", "meaning": "selama satu minggu"}
        ],
        "sentence": {
            "japanese": "本屋と郵便局の間に銀行があります。",
            "reading": "ほんやと ゆうびんきょくの あいだに ぎんこうが あります。",
            "meaning": "Ada bank di antara toko buku dan kantor pos."
        }
    },
    "話": {
        "meaning": "berbicara, cerita",
        "meaningEn": "Talk, Tale, Speak",
        "onyomi": ["ワ"],
        "kunyomi": ["はな.す", "はなし"],
        "words": [
            {"word": "話す", "reading": "はなす", "meaning": "berbicara"},
            {"word": "電話", "reading": "でんわ", "meaning": "telepon"},
            {"word": "会話", "reading": "かいわ", "meaning": "percakapan"}
        ],
        "sentence": {
            "japanese": "先生と日本語で話しました。",
            "reading": "せんせいと にほんごで はなしました。",
            "meaning": "Saya berbicara dengan guru dalam bahasa Jepang."
        }
    },
    "電": {
        "meaning": "listrik",
        "meaningEn": "Electricity",
        "onyomi": ["デン"],
        "kunyomi": [],
        "words": [
            {"word": "電車", "reading": "でんしゃ", "meaning": "kereta listrik"},
            {"word": "電話", "reading": "でんわ", "meaning": "telepon"},
            {"word": "電気", "reading": "でんき", "meaning": "listrik / lampu"}
        ],
        "sentence": {
            "japanese": "部屋の電気を消してください。",
            "reading": "へやの でんきを けして ください。",
            "meaning": "Tolong matikan lampu kamar."
        }
    },
    "聞": {
        "meaning": "mendengar, bertanya",
        "meaningEn": "Hear, Ask, Listen",
        "onyomi": ["ブン", "モン"],
        "kunyomi": ["き.く", "き.こえる"],
        "words": [
            {"word": "聞く", "reading": "きく", "meaning": "mendengar / bertanya"},
            {"word": "新聞", "reading": "しんぶん", "meaning": "koran"},
            {"word": "聞こえる", "reading": "きこえる", "meaning": "terdengar"}
        ],
        "sentence": {
            "japanese": "毎朝ラジオを聞いています。",
            "reading": "まいあさ ラジオを きいています。",
            "meaning": "Setiap pagi saya mendengarkan radio."
        }
    },
    "語": {
        "meaning": "bahasa, kata",
        "meaningEn": "Language, Word",
        "onyomi": ["ゴ"],
        "kunyomi": ["かた.る"],
        "words": [
            {"word": "日本語", "reading": "にほんご", "meaning": "bahasa Jepang"},
            {"word": "英語", "reading": "えいご", "meaning": "bahasa Inggris"},
            {"word": "単語", "reading": "たんご", "meaning": "kosakata"}
        ],
        "sentence": {
            "japanese": "日本語の勉強はとても楽しいです。",
            "reading": "にほんごの べんきょうは とても たのしいです。",
            "meaning": "Belajar bahasa Jepang sangat menyenangkan."
        }
    },
    "読": {
        "meaning": "membaca",
        "meaningEn": "Read",
        "onyomi": ["ドク"],
        "kunyomi": ["よ.む"],
        "words": [
            {"word": "読む", "reading": "よむ", "meaning": "membaca"},
            {"word": "読書", "reading": "どくしょ", "meaning": "membaca buku"},
            {"word": "読み方", "reading": "よみかた", "meaning": "cara membaca"}
        ],
        "sentence": {
            "japanese": "毎晩寝る前に本を読みます。",
            "reading": "まいばん ねる まえに ほんを よみます。",
            "meaning": "Setiap malam sebelum tidur saya membaca buku."
        }
    }
}


EN_TO_ID = {
    'power': 'kekuatan', 'eye': 'mata', 'capital': 'ibu kota', 'correct': 'benar',
    'parent': 'orang tua', 'morning': 'pagi', 'road-way': 'jalan', 'road': 'jalan',
    'direction': 'arah', 'cut': 'memotong', 'house': 'rumah', 'negative': 'tidak',
    'meal': 'makanan', 'wait': 'menunggu', 'pass through': 'melewati', 'map': 'peta',
    'younger brother': 'adik laki-laki', 'leg': 'kaki', 'foot': 'kaki', 'near': 'dekat',
    'many': 'banyak', 'exist': 'ada', 'possess': 'memiliki', 'have': 'punya',
    'town': 'kota', 'wind': 'angin', 'roof': 'atap', 'shop': 'toko',
    'degree': 'derajat', 'time': 'kali', 'west': 'barat', 'western': 'barat',
    'heavy': 'berat', 'true': 'asli', 'depart': 'berangkat', 'leave': 'pergi',
    'teach': 'mengajar', 'music': 'musik', 'comfort': 'nyaman', 'song': 'lagu',
    'sing': 'bernyanyi', 'chinese': 'Tiongkok', 'rice': 'nasi', 'walk': 'berjalan',
    'craft': 'kerajinan', 'sentence': 'kalimat', 'public': 'publik', 'stop': 'berhenti',
    'few': 'sedikit', 'little': 'sedikit', 'heart': 'hati', 'mind': 'pikiran',
    'body': 'tubuh', 'make': 'membuat', 'build': 'membangun', 'speak': 'berbicara',
    'say': 'berkata', 'word': 'kata', 'live': 'tinggal', 'reside': 'tinggal',
    'doctor': 'dokter', 'medicine': 'obat', 'study': 'belajar', 'research': 'penelitian',
    'separate': 'terpisah', 'sky': 'langit', 'empty': 'kosong', 'blue': 'biru',
    'green': 'hijau', 'bright': 'terang', 'light': 'cahaya', 'know': 'tahu',
    'matter': 'masalah', 'thing': 'benda', 'use': 'menggunakan', 'taste': 'rasa',
    'flavor': 'rasa', 'start': 'mulai', 'begin': 'mulai', 'clothes': 'pakaian',
    'clothing': 'pakaian', 'pour': 'menuang', 'person': 'orang', 'hero': 'pahlawan',
    'sound': 'suara', 'noise': 'bunyi', 'room': 'kamar', 'spring': 'musim semi',
    'daytime': 'siang', 'sea': 'laut', 'ocean': 'samudra', 'plan': 'rencana',
    'goods': 'barang', 'emergency': 'darurat', 'hold': 'memegang', 'world': 'dunia',
    'polish': 'memoles', 'send': 'mengirim', 'reflect': 'memantulkan', 'return': 'pulang',
    'diligent': 'rajin', 'employee': 'karyawan', 'travel': 'bepergian', 'trip': 'perjalanan',
    'sick': 'sakit', 'ill': 'sakit', 'wake up': 'bangun', 'borrow': 'meminjam',
    'fee': 'biaya', 'fare': 'ongkos', 'logic': 'logika', 'reason': 'alasan',
    'field': 'ladang', 'bird': 'burung', 'move': 'bergerak', 'motion': 'gerakan',
    'question': 'pertanyaan', 'bad': 'buruk', 'evil': 'jahat', 'family': 'keluarga',
    'tribe': 'suku', 'end': 'selesai', 'finish': 'akhir', 'turn': 'berputar',
    'hall': 'aula', 'place': 'tempat', 'location': 'lokasi', 'answer': 'jawaban',
    'arrive': 'tiba', 'wear': 'memakai', 'carry': 'membawa', 'luck': 'keberuntungan',
    'open': 'membuka', 'gather': 'berkumpul', 'meet': 'bertemu', 'idea': 'ide',
    'thought': 'pikiran', 'business': 'bisnis', 'test': 'menguji', 'try': 'mencoba',
    'quality': 'kualitas', 'substance': 'zat', 'building': 'gedung', 'mansion': 'gedung besar',
    'topic': 'topik', 'subject': 'subjek', 'effect': 'efek', 'dew': 'embun',
    'single': 'sendirian', 'orchid': 'anggrek', 'universal': 'universal',
    'noon': 'siang', 'tree': 'pohon', 'wood': 'pohon', 'rest': 'istirahat',
    'soil': 'tanah', 'earth': 'tanah', 'woman': 'perempuan', 'female': 'perempuan',
    'middle': 'tengah', 'circle': 'lingkaran', 'yen': 'yen', 'heaven': 'langit',
    'day': 'hari', 'sun': 'matahari', 'month': 'bulan', 'moon': 'bulan',
    'water': 'air', 'fire': 'api', 'gold': 'emas', 'money': 'uang',
    'year': 'tahun', 'now': 'sekarang', 'snow': 'salju', 'rain': 'hujan',
    'electricity': 'listrik', 'fish': 'ikan', 'meat': 'daging', 'tea': 'teh',
    'flower': 'bunga', 'forest': 'hutan', 'woods': 'hutan', 'gate': 'gerbang',
    'silver': 'perak', 'station': 'stasiun', 'school': 'sekolah', 'company': 'perusahaan',
    'book': 'buku', 'origin': 'asal', 'life': 'hidup', 'birth': 'lahir',
    'death': 'kematian', 'die': 'mati', 'see': 'melihat', 'look': 'melihat',
    'eat': 'makan', 'drink': 'minum', 'buy': 'membeli', 'sell': 'menjual',
    'write': 'menulis', 'read': 'membaca', 'listen': 'mendengar', 'hear': 'mendengar'
}

def clean_single_meaning(k):
    m_id = k.get('meaning', '').strip()
    m_en = k.get('meaningEn', '').strip()
    
    en_parts = [p.strip().lower() for p in re.split(r'[,/;]', m_en) if p.strip()]
    id_parts = [p.strip() for p in re.split(r'[,/;]', m_id) if p.strip()]
    
    clean_id_parts = []
    for p in id_parts:
        p_clean = re.sub(r'\(.*?\)', '', p).strip()
        if p_clean and not re.match(r'^\d+(\*\*\d+)?$', p_clean) and 'counter' not in p_clean.lower() and 'radikal' not in p_clean.lower():
            clean_id_parts.append(p_clean)
            
    if not clean_id_parts and id_parts:
        clean_id_parts = [re.sub(r'\(.*?\)', '', id_parts[0]).strip() or id_parts[0]]

    # Cek apakah ada EN keyword yang cocok dengan terjemahan ID
    for en_word in en_parts:
        if en_word in EN_TO_ID:
            target_id = EN_TO_ID[en_word]
            for part in clean_id_parts:
                if target_id.lower() in part.lower():
                    return target_id
            return target_id

    if clean_id_parts:
        first = clean_id_parts[0]
        first = re.sub(r'^(untuk|menjadi|sebuah|para)\s+', '', first).strip()
        return first
        
    return m_id

def sync_kanji():
    kanji_json_path = os.path.join(BASE_DIR, "data", "kanji.json")
    meta_json_path = os.path.join(BASE_DIR, "data", "kanji-meta.json")
    kanji_js_path = os.path.join(BASE_DIR, "js", "kanji.js")

    with open(kanji_json_path, "r", encoding="utf-8") as f:
        kanji_list = json.load(f)

    print(f"[sync_datasets] Membaca {len(kanji_list)} kanji dari data/kanji.json...")

    meta_dict = {}
    verified_count = 0
    needs_verif_count = 0

    for item in kanji_list:
        char = item["kanji"]
        # Audit dan perbarui jika masuk dalam daftar 79 N5
        if char in VERIFIED_N5_KANJI:
            v = VERIFIED_N5_KANJI[char]
            item["meaning"] = clean_single_meaning({"meaning": v["meaning"], "meaningEn": v["meaningEn"]})
            item["meaningEn"] = v["meaningEn"]
            item["onyomi"] = v["onyomi"]
            item["kunyomi"] = v["kunyomi"]
            item["examples"] = v["words"]
            item["words"] = v["words"]
            item["sentence"] = v["sentence"]
            item["verified"] = True
            item["verification_status"] = "verified"
            verified_count += 1
        else:
            item["meaning"] = clean_single_meaning(item)
            item["verified"] = False
            item["verification_status"] = "needs_verification"
            needs_verif_count += 1

        # Isi metadata stroke & grade
        strokes = item.get("strokes", 0)
        grade = item.get("grade", 99)
        meta_dict[char] = [strokes, grade]

    # Simpan kembali canonical data/kanji.json
    with open(kanji_json_path, "w", encoding="utf-8") as f:
        json.dump(kanji_list, f, ensure_ascii=False, indent=2)
    print(f"[sync_datasets] data/kanji.json berhasil diperbarui: {verified_count} terverifikasi, {needs_verif_count} ditandai needs_verification.")

    # Simpan data/kanji-meta.json
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(meta_dict, f, ensure_ascii=False, indent=2)
    print(f"[sync_datasets] data/kanji-meta.json disinkronkan ({len(meta_dict)} entri).")

    # Perbarui embedded window.KANJI_FULL_DATA di js/kanji.js
    with open(kanji_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Bersihkan sisa broken lines (seperti ... [truncated for diff preview]) dan assignment lama
    json_str = json.dumps(kanji_list, ensure_ascii=False)
    target_assign = f"window.KANJI_FULL_DATA = {json_str};\n"

    # Regex untuk mengganti seluruh blok assignment KANJI_FULL_DATA di awal file
    pattern = re.compile(r'window\.KANJI_FULL_DATA\s*=\s*\[.*?\];\s*', re.DOTALL)
    if pattern.search(js_content):
        # Bersihkan jika ada multiple atau broken
        new_js = pattern.sub('', js_content)
        # Hapus sisa placeholder truncation jika ada
        new_js = new_js.replace("... [truncated for diff preview]\n", "")
        # Selipkan kembali di bawah komentar header
        header_end = new_js.find("*/\n\nconst KanjiAPI =")
        if header_end == -1:
            header_end = new_js.find("const KanjiAPI =")
            new_js = new_js[:header_end] + target_assign + "\n" + new_js[header_end:]
        else:
            insert_pos = header_end + 3
            new_js = new_js[:insert_pos] + "\n" + target_assign + new_js[insert_pos:]
    else:
        # Selipkan sebelum KanjiAPI
        pos = js_content.find("const KanjiAPI =")
        new_js = js_content[:pos] + target_assign + "\n" + js_content[pos:]

    with open(kanji_js_path, "w", encoding="utf-8") as f:
        f.write(new_js)
    print(f"[sync_datasets] js/kanji.js window.KANJI_FULL_DATA berhasil disinkronkan ({len(kanji_list)} item).")


if __name__ == "__main__":
    sync_kanji()

