// Telegram WebApp obyektini faollashtirish
let tg = window.Telegram.WebApp;
tg.expand();

let coins = 0;
let energy = 500;
const maxEnergy = 500;

const coinEl = document.getElementById("coins");
const energyEl = document.getElementById("energy");
const tapBtn = document.getElementById("tap-btn");

tapBtn.addEventListener("click", (event) => {
    if (energy > 0) {
        coins += 1;
        energy -= 1;
        
        // Ekrandagi qiymatlarni yangilash
        coinEl.textContent = `${coins} 🪙`;
        energyEl.textContent = energy;
        
        // Tugma bosilganda telefon titrashi (Haptic Feedback)
        if (tg.HapticFeedback) {
            tg.HapticFeedback.impactOccurred("light");
        }
    } else {
        if (tg.HapticFeedback) {
            tg.HapticFeedback.notificationOccurred("error");
        }
    }
});

// Energiyani har 1 sekundda 1 tadan tiklab borish funksiyasi
setInterval(() => {
    if (energy < maxEnergy) {
        energy += 1;
        energyEl.textContent = energy;
    }
}, 1000);
