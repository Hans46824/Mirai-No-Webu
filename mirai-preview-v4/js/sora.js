window.SoraService = (() => {
    const fallbackReply = (message) => {
        const text = message.toLowerCase().trim();
        if (/は.*が|wa.*ga/.test(text)) {
            return "Hehe, ringkasnya: は menandai topik pembicaraan, sedangkan が sering menandai subjek atau informasi baru. Contoh: わたしは学生です (tentang saya), だれが来ますか (siapa yang datang?).";
        }
        if (/こんにちは|こんばんは|おはよう/.test(text)) {
            return "こんにちは！Yatta, senang bertemu denganmu ✨ Mau mencoba kosakata, mencari kelas, atau membuka Kamus Kanji?";
        }
        if (/nol|dasar|mulai|pemula/.test(text)) {
            return "Ganbatte! Untuk mulai dari nol, coba urutannya: hiragana → katakana → kosakata sehari-hari → pola kalimat dasar → latihan percakapan. Halaman Kelas Dasar bisa jadi titik awalmu.";
        }
        if (/kanji/.test(text)) {
            return "Kamus Kanji Mirai bisa membantumu mencari kanji lewat karakter, arti Indonesia, onyomi, atau kunyomi. Coba buka halaman Kamus Kanji ya!";
        }
        if (/日|arti.*hari|hari.*arti/.test(text)) {
            return "日 dibaca ニチ / ジツ (onyomi) atau ひ / か (kunyomi). Artinya hari atau matahari. Contohnya 日本 (にほん, Jepang) dan 日曜日 (にちようび, Minggu).";
        }
        return "Aku masih memakai mode bantuan lokal, jadi jawabanku belum memakai AI/API sungguhan. Tapi aku bisa membantumu menemukan Kelas Dasar, Kelas Lanjutan, atau Kamus Kanji. Hehe ✨";
    };

    async function sendMessage(message) {
        // Configure window.SORA_API_ENDPOINT from a non-committed config or backend.
        // Credentials belong on that backend, never in this static frontend.
        const endpoint = window.SORA_API_ENDPOINT;
        if (!endpoint) return fallbackReply(message);
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error("Sora sedang tidak dapat dihubungi.");
        const payload = await response.json();
        return payload.reply || payload.message || "Maaf, aku belum menemukan jawaban yang tepat.";
    }

    return { sendMessage };
})();
