const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

let coins = 0;
let chips = 0;
let maxEnergy = 1000;
let currentEnergy = 1000;

const coinEl = document.getElementById('coinBalance');
const chipEl = document.getElementById('chipBalance');
const energyText = document.getElementById('energyText');
const energyFill = document.getElementById('energyFill');
const modalChips = document.getElementById('modalChips');
const tapArea = document.getElementById('tapArea');
const coinBtn = document.getElementById('coin');

// Bosish (Tap) Logikasi
coinBtn.addEventListener('pointerdown', (e) => {
    if (currentEnergy > 0) {
        coins += 1;
        currentEnergy -= 1;
        updateUI();
        
        // Haptic feedback (Telefon tebranishi)
        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('light');
        
        // Uchib chiquvchi raqam (Animation)
        const rect = tapArea.getBoundingClientRect();
        createFloatNumber(e.clientX - 10, e.clientY - rect.top - 20);
    } else {
        if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
    }
});

// Energiyani tiklash
setInterval(() => {
    if (currentEnergy < maxEnergy) {
        currentEnergy = Math.min(maxEnergy, currentEnergy + 2);
        updateUI();
    }
}, 1000);

function updateUI() {
    coinEl.innerText = coins;
    chipEl.innerText = chips;
    modalChips.innerText = chips;
    energyText.innerText = currentEnergy;
    energyFill.style.width = (currentEnergy / maxEnergy * 100) + '%';
}

function createFloatNumber(x, y) {
    const floatNum = document.createElement('div');
    floatNum.className = 'floating-number';
    floatNum.innerText = '+1';
    floatNum.style.left = x + 'px';
    floatNum.style.top = y + 'px';
    tapArea.appendChild(floatNum);
    
    setTimeout(() => {
        floatNum.style.transform = 'translateY(-80px)';
        floatNum.style.opacity = '0';
    }, 10);
    
    setTimeout(() => floatNum.remove(), 500);
}

// Hamyon Modali boshqaruvi
function openWallet() {
    document.getElementById('walletModal').style.display = 'flex';
    setTimeout(() => document.getElementById('walletContent').classList.add('open'), 10);
}

function closeWallet(e) {
    if (e.target.id === 'walletModal') {
        document.getElementById('walletContent').classList.remove('open');
        setTimeout(() => document.getElementById('walletModal').style.display = 'none', 300);
    }
}

// ================= ASOSIY HARAKATLAR =================

function swapCoins() {
    if (coins >= 100000) {
        tg.showConfirm("100,000 Tangani 50 Olmosga almashtirasizmi?", function(c) {
            if(c) {
                coins -= 100000; 
                chips += 50; 
                updateUI();
                tg.HapticFeedback.notificationOccurred('success');
            }
        });
    } else {
        tg.showAlert(`Tangalar yetarli emas! Yana ${100000 - coins} Tanga yig'ing.`);
    }
}

function buyDiamonds() {
    // Botga ma'lumot yuborish, bot esa Invoice (Stars) ochadi
    tg.sendData(JSON.stringify({action: "buy_stars", amount: 100}));
    tg.close();
}

function withdraw() {
    if(chips >= 10000) {
        // Chiqim qilish uchun botga qaytarish
        tg.sendData(JSON.stringify({action: "withdraw_uc"}));
        tg.close();
    } else {
        tg.showAlert(`Balans yetarli emas! Yana ${10000 - chips} 💎 kerak.`);
    }
}

function showTasks() {
    tg.showAlert("Bu bo'limda tez orada homiylar kanallari va qimmatli vazifalar paydo bo'ladi!");
}
