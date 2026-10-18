/**
 * File: js/progress.js
 * Fungsi: Sistem Manajemen Progres Belajar Terpusat (MiraiProgress Engine v1).
 * Penyimpanan: 100% LocalStorage di sisi peramban pengguna (mirai_progress_v1).
 * Fitur:
 *  - Pelacakan 7 modul kurikulum (Hiragana, Katakana, Kosakata, Jikoshokai, Grammar, Kanji, Kalimat).
 *  - Migrasi data lama nir-kehilangan (backward-compatible dengan mirai_completed_materi, mirai_weak_kana, dll).
 *  - Penghitungan streak harian nyata berbasis tanggal lokal (YYYY-MM-DD).
 *  - Target belajar harian (default: 10 soal per hari).
 *  - Akumulasi XP dan Level pengguna (1000 XP per level).
 *  - Ekspor & Impor berkas progres format JSON agar pengguna dapat memindahkan data antar-perangkat.
 *  - Sinkronisasi instan ke UI kartu modul, tombol "Lanjutkan Belajar", dan panel statistik.
 */

(function (window, document) {
  "use strict";

  const STORAGE_KEY_V1 = "mirai_progress_v1";

  // Modul resmi Mirai no Buuku (7 modul berjenjang)
  const LESSON_MODULES = [
    {
      id: "hiragana",
      slug: "hiragana",
      num: "01",
      title: "Huruf Hiragana",
      jp: "平仮名",
      category: "dasar",
      url: "materi/dasar/hiragana.html"
    },
    {
      id: "katakana",
      slug: "katakana",
      num: "02",
      title: "Huruf Katakana",
      jp: "片仮名",
      category: "dasar",
      url: "materi/dasar/katakana.html"
    },
    {
      id: "kosakata",
      slug: "kosakata",
      num: "03",
      title: "Kosakata Dasar",
      jp: "基本単語",
      category: "dasar",
      url: "materi/dasar/kosakata.html"
    },
    {
      id: "jikoshokai",
      slug: "jikoshokai",
      num: "04",
      title: "Salam & Jikoshokai",
      jp: "挨拶と自己紹介",
      category: "dasar",
      url: "materi/dasar/jikoshokai.html"
    },
    {
      id: "grammar",
      slug: "grammar",
      num: "05",
      title: "Tata Bahasa & Partikel",
      jp: "文法と助詞",
      category: "lanjutan",
      url: "materi/lanjutan/grammar.html"
    },
    {
      id: "kanji",
      slug: "kanji",
      num: "06",
      title: "Aksara Kanji & JLPT",
      jp: "漢字とJLPT",
      category: "lanjutan",
      url: "materi/lanjutan/kanji.html"
    },
    {
      id: "kalimat",
      slug: "kalimat",
      num: "07",
      title: "Membaca Kalimat Sederhana",
      jp: "短文読解",
      category: "lanjutan",
      url: "materi/lanjutan/kalimat.html"
    }
  ];

  // Helper tanggal lokal format YYYY-MM-DD
  function getTodayString() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const date = String(d.getDate()).padStart(2, "0");
    return `${year}-${month}-${date}`;
  }

  // Helper selisih hari antara dua string YYYY-MM-DD
  function getDayDifference(dateStrA, dateStrB) {
    if (!dateStrA || !dateStrB) return 999;
    const a = new Date(dateStrA + "T00:00:00");
    const b = new Date(dateStrB + "T00:00:00");
    const diffTime = Math.abs(b.getTime() - a.getTime());
    return Math.round(diffTime / (1000 * 60 * 60 * 24));
  }

  // Template default progres v1
  function createDefaultProgress() {
    return {
      version: 1,
      streak: 1,
      lastStudyDate: getTodayString(),
      xp: 0,
      dailyGoal: 10,
      dailyProgress: {
        date: getTodayString(),
        answered: 0
      },
      lessonsDone: {
        hiragana: false,
        katakana: false,
        kosakata: false,
        jikoshokai: false,
        grammar: false,
        kanji: false,
        kalimat: false
      },
      lastLesson: {
        id: "hiragana",
        title: "Huruf Hiragana",
        step: "Langkah 1 dari 8",
        url: "materi/dasar/hiragana.html"
      },
      quizBest: {},
      weakItems: {}, // Digunakan Leitner Box 1..5 di Tahap C
      settings: {
        furigana: true,
        romaji: true
      }
    };
  }

  const MiraiProgress = {
    LESSONS: LESSON_MODULES,

    // Muat data terpusat dengan migrasi otomatis dari data versi lama
    load() {
      let data = null;
      try {
        const raw = localStorage.getItem(STORAGE_KEY_V1);
        if (raw) {
          data = JSON.parse(raw);
        }
      } catch (e) {
        console.warn("Gagal mem-parse mirai_progress_v1, menginisialisasi ulang:", e);
      }

      if (!data || typeof data !== "object") {
        data = this.migrateLegacyData();
        this.save(data);
      } else {
        // Pastikan field penting selalu ada meskipun data lama
        data.lessonsDone = data.lessonsDone || {};
        LESSSON_MODULES.forEach((mod) => {
          if (typeof data.lessonsDone[mod.id] === "undefined") {
            data.lessonsDone[mod.id] = false;
          }
        });
        if (!data.dailyProgress || data.dailyProgress.date !== getTodayString()) {
          data.dailyProgress = {
            date: getTodayString(),
            answered: 0
          };
        }
        if (typeof data.streak !== "number" || data.streak < 1) {
          data.streak = 1;
        }
        if (typeof data.xp !== "number") {
          data.xp = 0;
        }
        if (typeof data.dailyGoal !== "number") {
          data.dailyGoal = 10;
        }
        if (!data.quizBest || typeof data.quizBest !== "object") {
          data.quizBest = {};
        }
        if (!data.weakItems || typeof data.weakItems !== "object") {
          data.weakItems = {};
        }
      }

      return data;
    },

    // Migrasi data lama dari berbagai kunci localStorage terpisah
    migrateLegacyData() {
      const fresh = createDefaultProgress();

      try {
        // 1. Migrasi modul yang sudah selesai (mirai_completed_materi)
        const oldCompletedRaw = localStorage.getItem("mirai_completed_materi");
        if (oldCompletedRaw) {
          const list = JSON.parse(oldCompletedRaw);
          if (Array.isArray(list)) {
            list.forEach((id) => {
              const cleanId = String(id).replace("materi-dasar-", "").replace("materi-lanjutan-", "");
              if (typeof fresh.lessonsDone[cleanId] !== "undefined") {
                fresh.lessonsDone[cleanId] = true;
                fresh.xp += 50; // Bonus XP modul selesai
              }
            });
          }
        }

        // 2. Migrasi pelajaran terakhir (mirai_last_materi)
        const oldLastRaw = localStorage.getItem("mirai_last_materi");
        if (oldLastRaw) {
          const item = JSON.parse(oldLastRaw);
          if (item && item.id) {
            const cleanId = String(item.id).replace("materi-dasar-", "").replace("materi-lanjutan-", "");
            fresh.lastLesson = {
              id: cleanId,
              title: item.title || cleanId,
              step: item.step || "",
              url: item.url || ""
            };
          }
        }

        // 3. Migrasi skor terbaik lama
        const keysToMigrate = [
          "mirai_time_attack_best",
          "mirai_time_attack_best_hiragana",
          "mirai_time_attack_best_katakana",
          "mirai_mode_best_bunpou",
          "mirai_mode_best_custom",
          "mirai_memory_best_flips",
          "mirai_memory_best_flips_6",
          "mirai_memory_best_flips_12",
          "mirai_memory_best_flips_24"
        ];
        keysToMigrate.forEach((k) => {
          const v = localStorage.getItem(k);
          if (v !== null) {
            fresh.quizBest[k] = isNaN(Number(v)) ? v : Number(v);
          }
        });

        // 4. Migrasi weak kana lama
        const oldWeakRaw = localStorage.getItem("mirai_weak_kana");
        if (oldWeakRaw) {
          const weakObj = JSON.parse(oldWeakRaw);
          if (weakObj && typeof weakObj === "object") {
            Object.keys(weakObj).forEach((char) => {
              fresh.weakItems[`kana_${char}`] = {
                type: "kana",
                prompt: char,
                answer: weakObj[char]?.romaji || "",
                box: 1,
                nextReview: Date.now(),
                failCount: weakObj[char]?.mistakes || 1,
                passCount: 0
              };
            });
          }
        }
      } catch (err) {
        console.warn("Kesalahan parsial saat migrasi data lama:", err);
      }

      return fresh;
    },

    // Simpan progres ke localStorage sekaligus sinkronisasi kunci backward-compatible
    save(data) {
      if (!data) return;
      try {
        localStorage.setItem(STORAGE_KEY_V1, JSON.stringify(data));

        // Sinkronkan ke kunci lama agar kode lama yang membaca langsung tidak rusak
        const completedArr = Object.keys(data.lessonsDone)
          .filter((k) => data.lessonsDone[k])
          .map((k) => {
            const mod = LESSON_MODULES.find((m) => m.id === k);
            return mod && mod.category === "lanjutan" ? `materi-lanjutan-${k}` : `materi-dasar-${k}`;
          });
        localStorage.setItem("mirai_completed_materi", JSON.stringify(completedArr));

        if (data.lastLesson && data.lastLesson.url) {
          localStorage.setItem(
            "mirai_last_materi",
            JSON.stringify({
              id: data.lastLesson.id,
              title: data.lastLesson.title,
              step: data.lastLesson.step || "",
              url: data.lastLesson.url,
              timestamp: Date.now()
            })
          );
        }
      } catch (e) {
        console.error("Gagal menyimpan mirai_progress_v1:", e);
      }
    },

    // Ambil data progres saat ini
    getProgress() {
      return this.load();
    },

    // Catat aktivitas belajar & perbarui streak harian
    recordActivity(questionsCount = 1, earnedXp = 10) {
      const data = this.load();
      const today = getTodayString();
      const lastDate = data.lastStudyDate;

      if (!lastDate) {
        data.streak = 1;
      } else if (lastDate === today) {
        // Sudah belajar hari ini, streak tidak berubah
      } else {
        const diff = getDayDifference(lastDate, today);
        if (diff === 1) {
          // Belajar beruntun hari berikutnya!
          data.streak = (data.streak || 0) + 1;
        } else {
          // Terlewat lebih dari 1 hari, reset streak ke 1
          data.streak = 1;
        }
      }

      data.lastStudyDate = today;

      // Update target harian
      if (!data.dailyProgress || data.dailyProgress.date !== today) {
        data.dailyProgress = { date: today, answered: 0 };
      }
      data.dailyProgress.answered += Math.max(0, questionsCount);

      // Tambah XP
      data.xp = (data.xp || 0) + Math.max(0, earnedXp);

      this.save(data);
      this.updateAllUI();
      return data;
    },

    // Tandai modul materi selesai / belum selesai
    toggleLessonDone(lessonId) {
      const data = this.load();
      const isCurrentlyDone = !!data.lessonsDone[lessonId];
      const newState = !isCurrentlyDone;
      data.lessonsDone[lessonId] = newState;

      if (newState) {
        // Bonus 50 XP penyelesaian modul
        data.xp = (data.xp || 0) + 50;
        this.recordActivity(0, 0); // Perbarui streak jika belum hari ini
      }

      this.save(data);
      this.updateAllUI();
      return newState;
    },

    // Set pelajaran terakhir yang dibuka pengguna
    setLastLesson(id, title, step, url) {
      if (!id) return;
      const data = this.load();
      data.lastLesson = {
        id,
        title: title || id,
        step: step || "",
        url: url || window.location.href
      };
      this.save(data);
    },

    // Catat skor kuis terbaik
    recordQuizBest(modeKey, score) {
      if (!modeKey) return;
      const data = this.load();
      const prev = data.quizBest[modeKey] || 0;
      if (typeof score === "number" && score > prev) {
        data.quizBest[modeKey] = score;
        this.save(data);
      }
    },

    // Hitung persentase modul selesai
    getCompletionRate() {
      const data = this.load();
      const total = LESSON_MODULES.length;
      const completed = Object.keys(data.lessonsDone).filter((k) => data.lessonsDone[k]).length;
      return Math.round((completed / total) * 100);
    },

    // Dapatkan data URL pelajaran berikutnya atau pelajaran terakhir
    getResumeUrl(currentBasePath = "") {
      const data = this.load();
      if (data.lastLesson && data.lastLesson.url) {
        // Sesuaikan path jika dipanggil dari subfolder berbeda
        return data.lastLesson.url;
      }
      // Default: modul pertama yang belum selesai
      const unfinished = LESSON_MODULES.find((m) => !data.lessonsDone[m.id]);
      if (unfinished) {
        return (currentBasePath ? currentBasePath + "/" : "") + unfinished.url;
      }
      return (currentBasePath ? currentBasePath + "/" : "") + LESSON_MODULES[0].url;
    },

    // Ekspor seluruh data progres ke format JSON yang dapat diunduh pengguna
    exportJSON() {
      const data = this.load();
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      const d = new Date();
      const timeTag = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}`;
      a.href = url;
      a.download = `mirai-progress-${timeTag}.json`;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 500);
    },

    // Impor progres dari teks JSON yang diunggah / ditempel
    importJSON(jsonString) {
      try {
        const parsed = JSON.parse(jsonString);
        if (!parsed || typeof parsed !== "object") {
          throw new Error("Format JSON tidak valid");
        }
        if (!parsed.version && !parsed.lessonsDone && !parsed.xp) {
          throw new Error("Berkas bukan cadangan progres Mirai no Hana yang valid");
        }

        const current = this.load();
        const merged = {
          ...current,
          ...parsed,
          version: 1,
          lessonsDone: {
            ...current.lessonsDone,
            ...(parsed.lessonsDone || {})
          },
          quizBest: {
            ...current.quizBest,
            ...(parsed.quizBest || {})
          },
          weakItems: {
            ...current.weakItems,
            ...(parsed.weakItems || {})
          }
        };

        this.save(merged);
        this.updateAllUI();
        return { success: true };
      } catch (e) {
        return { success: false, error: e.message };
      }
    },

    // Perbarui seluruh elemen UI yang terikat dengan atribut progres
    updateAllUI() {
      const data = this.load();
      const level = Math.floor((data.xp || 0) / 1000) + 1;
      const levelXp = (data.xp || 0) % 1000;
      const xpPercent = Math.min(100, Math.round((levelXp / 1000) * 100));

      // 1. Perbarui angka Streak
      document.querySelectorAll("[data-streak]").forEach((el) => {
        el.textContent = data.streak || 1;
      });

      // 2. Perbarui Level & XP
      document.querySelectorAll("[data-user-level]").forEach((el) => {
        el.textContent = level;
      });
      document.querySelectorAll("[data-total-xp]").forEach((el) => {
        el.textContent = data.xp || 0;
      });
      document.querySelectorAll("[data-level-xp]").forEach((el) => {
        el.textContent = levelXp;
      });
      document.querySelectorAll("[data-xp-bar]").forEach((el) => {
        el.style.width = `${xpPercent}%`;
      });

      // 3. Perbarui Target Harian
      const answeredToday = data.dailyProgress?.answered || 0;
      const dailyGoal = data.dailyGoal || 10;
      document.querySelectorAll("[data-daily-progress]").forEach((el) => {
        el.textContent = answeredToday;
      });
      document.querySelectorAll("[data-daily-goal]").forEach((el) => {
        el.textContent = dailyGoal;
      });
      document.querySelectorAll("[data-daily-percent]").forEach((el) => {
        const pct = Math.min(100, Math.round((answeredToday / dailyGoal) * 100));
        el.textContent = `${pct}%`;
      });
      document.querySelectorAll("[data-daily-bar]").forEach((el) => {
        const pct = Math.min(100, Math.round((answeredToday / dailyGoal) * 100));
        el.style.width = `${pct}%`;
      });

      // 4. Perbarui Jumlah Item Lemah
      const weakCount = Object.keys(data.weakItems || {}).length;
      document.querySelectorAll("[data-review-count]").forEach((el) => {
        el.textContent = weakCount;
      });

      // 5. Perbarui Status Tiap Modul di Daftar Modul (kelas/index.html & materi/*/index.html)
      LESSON_MODULES.forEach((mod) => {
        const isDone = !!data.lessonsDone[mod.id];
        document.querySelectorAll(`[data-module-card="${mod.id}"]`).forEach((card) => {
          card.classList.toggle("is-completed", isDone);
          const badge = card.querySelector(".mod-status-badge");
          if (badge) {
            badge.className = `mod-status-badge ${isDone ? "is-done" : "is-pending"}`;
            badge.innerHTML = isDone ? "✓ Selesai" : "Belum Selesai";
          }
          const bar = card.querySelector(".mod-progress-fill");
          if (bar) {
            bar.style.width = isDone ? "100%" : "0%";
          }
        });
      });

      // 6. Perbarui Tombol "Lanjutkan Belajar"
      document.querySelectorAll("[data-resume-link]").forEach((link) => {
        const rawUrl = data.lastLesson?.url || "materi/dasar/hiragana.html";
        // Sesuaikan path relatif terhadap letak halaman pemanggil
        const isMateriSub = window.location.pathname.includes("/materi/dasar/") || window.location.pathname.includes("/materi/lanjutan/");
        const isMateriRoot = window.location.pathname.endsWith("/materi/dasar/index.html") || window.location.pathname.endsWith("/materi/lanjutan/index.html");
        const isKelas = window.location.pathname.includes("/kelas/");

        let targetHref = rawUrl;
        if (isKelas) {
          targetHref = rawUrl.startsWith("../") ? rawUrl : "../" + rawUrl;
        } else if (isMateriSub) {
          targetHref = rawUrl.split("/").pop();
        } else if (isMateriRoot) {
          targetHref = rawUrl.replace("materi/dasar/", "").replace("materi/lanjutan/", "../lanjutan/");
        }

        link.setAttribute("href", targetHref);
        const label = link.querySelector("[data-resume-title]");
        if (label) {
          label.textContent = data.lastLesson?.title || "Hiragana";
        }
      });
    },

    // Inisialisasi logika pada halaman materi (mini kuis 5 soal + tombol tandai selesai)
    initMateriPage() {
      const container = document.querySelector("[data-materi-id]");
      if (!container) return;

      const rawId = container.dataset.materiId;
      const cleanId = rawId.replace("materi-dasar-", "").replace("materi-lanjutan-", "");
      const title = container.dataset.materiTitle || document.title.split("—")[0].trim();
      const step = container.dataset.materiStep || "Modul";

      // Catat sebagai modul terakhir yang dipelajari
      this.setLastLesson(cleanId, title, step, window.location.pathname);

      // Pengendali tombol "Tandai Selesai"
      const toggleBtn = document.querySelector(".materi-complete-toggle");
      if (toggleBtn) {
        const updateBtn = (isDone) => {
          toggleBtn.classList.toggle("is-active", isDone);
          toggleBtn.setAttribute("aria-pressed", isDone ? "true" : "false");
          toggleBtn.innerHTML = isDone
            ? `<span>✓</span><span>Materi Selesai</span>`
            : `<span>○</span><span>Tandai Selesai</span>`;
        };

        const currentDone = !!this.load().lessonsDone[cleanId];
        updateBtn(currentDone);

        toggleBtn.addEventListener("click", () => {
          const isNowDone = this.toggleLessonDone(cleanId);
          updateBtn(isNowDone);
        });
      }

      // Pengendali Mini Kuis 5 Soal
      const quizCards = document.querySelectorAll(".buuku-quiz-card");
      let answeredInThisLesson = 0;
      let correctInThisLesson = 0;

      quizCards.forEach((card, index) => {
        const optButtons = card.querySelectorAll(".buuku-quiz-opt-btn");
        const feedbackEl = card.querySelector(".buuku-quiz-feedback");

        optButtons.forEach((btn) => {
          btn.addEventListener("click", () => {
            const isCorrect = btn.dataset.correct === "true";
            optButtons.forEach((b) => {
              b.disabled = true;
              if (b.dataset.correct === "true") {
                b.classList.add("is-correct");
              }
            });

            if (!isCorrect) {
              btn.classList.add("is-wrong");
            } else {
              correctInThisLesson++;
            }

            if (feedbackEl) {
              feedbackEl.classList.add("is-visible");
              feedbackEl.classList.add(isCorrect ? "correct" : "wrong");
            }

            answeredInThisLesson++;

            // Catat ke progres terpusat
            MiraiProgress.recordActivity(1, isCorrect ? 10 : 2);

            // Jika semua 5 soal dijawab, beri umpan balik penyelesaian
            if (answeredInThisLesson === quizCards.length) {
              const quizHeader = document.querySelector(".buuku-quiz-header");
              if (quizHeader && !document.querySelector(".quiz-completion-banner")) {
                const banner = document.createElement("div");
                banner.className = "quiz-completion-banner";
                banner.style.cssText =
                  "margin: 16px 0; padding: 14px 18px; border-radius: 12px; background: #ecfdf5; border: 1.5px solid #10b981; color: #065f46; font-size: 14px; font-weight: 600; display: flex; align-items: center; justify-content: space-between; gap: 12px;";
                banner.innerHTML = `
                  <div>
                    <span>🎉 Kuis Pemahaman Selesai! Skor: <strong>${correctInThisLesson}/${quizCards.length}</strong></span>
                    <span style="font-size:12px; display:block; opacity:0.85; margin-top:2px;">Progres harian bertambah +${answeredInThisLesson} soal!</span>
                  </div>
                  <button type="button" class="btn-complete-prompt" style="padding: 6px 14px; background:#059669; color:#fff; border:none; border-radius:8px; font-size:12px; font-weight:700; cursor:pointer;">
                    Tandai Selesai ✓
                  </button>
                `;
                const promptBtn = banner.querySelector(".btn-complete-prompt");
                if (promptBtn) {
                  promptBtn.addEventListener("click", () => {
                    MiraiProgress.toggleLessonDone(cleanId);
                    if (toggleBtn) {
                      toggleBtn.classList.add("is-active");
                      toggleBtn.setAttribute("aria-pressed", "true");
                      toggleBtn.innerHTML = `<span>✓</span><span>Materi Selesai</span>`;
                    }
                    promptBtn.textContent = "Tersimpan ✓";
                    promptBtn.disabled = true;
                  });
                }
                quizHeader.parentNode.insertBefore(banner, quizHeader.nextSibling);
              }
            }
          });
        });
      });
    },

    // Inisialisasi modal Ekspor/Impor pada halaman kelas/index.html
    setupExportImportModal() {
      const exportBtn = document.querySelector("[data-action-export]");
      const importBtn = document.querySelector("[data-action-import]");
      const modal = document.querySelector("#progress-sync-modal");

      if (exportBtn) {
        exportBtn.addEventListener("click", () => {
          this.exportJSON();
        });
      }

      if (importBtn && modal) {
        importBtn.addEventListener("click", () => {
          modal.removeAttribute("hidden");
          modal.classList.add("is-active");
        });

        const closeBtn = modal.querySelector(".modal-close-btn");
        if (closeBtn) {
          closeBtn.addEventListener("click", () => {
            modal.setAttribute("hidden", "");
            modal.classList.remove("is-active");
          });
        }

        const fileInput = modal.querySelector("#progress-file-input");
        const submitFileBtn = modal.querySelector("#progress-submit-file");
        const textInput = modal.querySelector("#progress-text-input");
        const submitTextBtn = modal.querySelector("#progress-submit-text");
        const statusMsg = modal.querySelector("#progress-modal-status");

        if (submitTextBtn && textInput) {
          submitTextBtn.addEventListener("click", () => {
            const raw = textInput.value.trim();
            if (!raw) {
              if (statusMsg) statusMsg.textContent = "Silakan tempel teks JSON terlebih dahulu.";
              return;
            }
            const res = MiraiProgress.importJSON(raw);
            if (res.success) {
              if (statusMsg) {
                statusMsg.textContent = "✓ Progres berhasil dipulihkan!";
                statusMsg.style.color = "#059669";
              }
              setTimeout(() => {
                modal.setAttribute("hidden", "");
                modal.classList.remove("is-active");
                window.location.reload();
              }, 1200);
            } else {
              if (statusMsg) {
                statusMsg.textContent = `Gagal: ${res.error}`;
                statusMsg.style.color = "#dc2626";
              }
            }
          });
        }

        if (fileInput) {
          fileInput.addEventListener("change", (e) => {
            const file = e.target.files && e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (evt) => {
              const res = MiraiProgress.importJSON(evt.target.result);
              if (res.success) {
                if (statusMsg) {
                  statusMsg.textContent = "✓ Berkas berhasil diimpor!";
                  statusMsg.style.color = "#059669";
                }
                setTimeout(() => {
                  modal.setAttribute("hidden", "");
                  modal.classList.remove("is-active");
                  window.location.reload();
                }, 1200);
              } else {
                if (statusMsg) {
                  statusMsg.textContent = `Gagal membaca berkas: ${res.error}`;
                  statusMsg.style.color = "#dc2626";
                }
              }
            };
            reader.readAsText(file);
          });
        }
      }
    },

    // Inisialisasi awal
    init() {
      this.updateAllUI();
      this.initMateriPage();
      this.setupExportImportModal();
    }
  };

  // Ekspor ke scope global window
  window.MiraiProgress = MiraiProgress;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => MiraiProgress.init());
  } else {
    MiraiProgress.init();
  }
})(window, document);
