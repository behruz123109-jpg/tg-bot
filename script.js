const tg = window.Telegram.WebApp;
tg.expand();

// O'yin ma'lumotlari (Boshlang'ich holat)
let totalCoins = 0; // Balans
let sessionEarnedCoins = 0; // Shu safar topilgan
let sessionSpentCoins = 0; // Upgradelarga sarflangan

let tapValue = 1; // Boshida 1 ta beradi
let maxEnergy = 100; // Limit 100
let currentEnergy = 100;

// Upgradelar narxi
let multitapCost = 500;
let energyLimitCost = 500;

const displayCoins = document.getElementById('display-coins');
const energyText = document.getElementById('energy-text');
const mainCoin = document.getElementById('main-coin');
const coinSection = document.getElementById('coin-section');

// Ekranni yangilash
function updateUI() {
    displayCoins.innerText = totalCoins.toLocaleString();
    energyText.innerText = `${currentEnergy}/${maxEnergy}`;
    document.getElementById('multitap-cost').innerText = multitapCost;
    document.getElementById('energy-cost').innerText = energyLimitCost;
}

// Telegramning Rasmiy Tugmasini sozlash (Saqlash uchun)
tg.MainButton.setText("🔄 Natijani saqlash va chiqish");
tg.MainButton.color = "#facc15"; // Tilla rang
tg.MainButton.textColor = "#000000";

// Asosiy bosish funksiyasi
function handleTap(e) {
    if (currentEnergy >= tapValue) {
        currentEnergy -= tapValue;
        totalCoins += tapValue;
        sessionEarnedCoins += tapValue;
        updateUI();

        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('light');

        // Foydalanuvchi birinchi marta bosganda Saqlash tugmasi chiqadi
        if (!tg.MainButton.isVisible) {
            tg.MainButton.show();
        }

        // Animatsiya
        const rect = coinSection.getBoundingClientRect();
        let clientX = e.type.includes('touch') ? e.touches[e.touches.length - 1].clientX : e.clientX;
        let clientY = e.type.includes('touch') ? e.touches[e.touches.length - 1].clientY : e.clientY;

        const x = clientX - rect.left;
        const y = clientY - rect.top;

        const floatNum = document.createElement('div');
        floatNum.classList.add('float-text');
        floatNum.innerText = `+${tapValue}`;
        floatNum.style.left = `${x}px`;
        floatNum.style.top = `${y}px`;
        floatNum.style.marginLeft = `${(Math.random() - 0.5) * 40}px`;

        coinSection.appendChild(floatNum);
        setTimeout(() => floatNum.remove(), 1000);
    }
}

// Multitouch
mainCoin.addEventListener('touchstart', (e) => {
    e.preventDefault(); 
    for(let i=0; i < e.changedTouches.length; i++) handleTap(e);
});
mainCoin.addEventListener('mousedown', handleTap);

// Energiya tiklanishi
setInterval(() => {
    if (currentEnergy < maxEnergy) {
        currentEnergy += 1;
        updateUI();
    }
}, 1000);

// --- BOOST PANEL LOGIKASI ---
document.getElementById('open-boosts-btn').addEventListener('click', () => {
    document.getElementById('boost-modal').classList.add('active');
});

document.getElementById('close-boosts-btn').addEventListener('click', () => {
    document.getElementById('boost-modal').classList.remove('active');
});

// Multitap sotib olish
document.getElementById('buy-multitap').addEventListener('click', () => {
    if (totalCoins >= multitapCost) {
        totalCoins -= multitapCost;
        sessionSpentCoins += multitapCost;
        tapValue += 1; // Bosish kuchi 1 taga oshadi
        multitapCost = Math.floor(multitapCost * 2); // Keyingi safar 2 barobar qimmatlashadi
        updateUI();
        if (!tg.MainButton.isVisible) tg.MainButton.show();
        tg.showAlert(`✅ Tabriklaymiz! Endi siz har bosganda ${tapValue} tanga olasiz.`);
    } else {
        tg.showAlert("❌ Bunga tangangiz yetmaydi!");
    }
});

// Energiya Limit sotib olish
document.getElementById('buy-energy').addEventListener('click', () => {
    if (totalCoins >= energyLimitCost) {
        totalCoins -= energyLimitCost;
        sessionSpentCoins += energyLimitCost;
        maxEnergy += 100; // Limit 100 taga oshadi
        energyLimitCost = Math.floor(energyLimitCost * 2);
        updateUI();
        if (!tg.MainButton.isVisible) tg.MainButton.show();
        tg.showAlert(`✅ Tabriklaymiz! Energiya limitingiz ${maxEnergy} ga oshdi.`);
    } else {
        tg.showAlert("❌ Bunga tangangiz yetmaydi!");
    }
});

// Telegram rasmiy tugmasi bosilganda ma'lumotni botga jo'natish
tg.MainButton.onClick(() => {
    const data = {
        earnedCoins: sessionEarnedCoins,
        spentCoins: sessionSpentCoins,
        energy: currentEnergy,
        maxEnergy: maxEnergy,
        tapValue: tapValue
    };
    tg.sendData(JSON.stringify(data)); 
});

updateUI();const tg = window.Telegram.WebApp;
tg.expand();

// O'yin ma'lumotlari (Boshlang'ich holat)
let totalCoins = 0; // Balans
let sessionEarnedCoins = 0; // Shu safar topilgan
let sessionSpentCoins = 0; // Upgradelarga sarflangan

let tapValue = 1; // Boshida 1 ta beradi
let maxEnergy = 100; // Limit 100
let currentEnergy = 100;

// Upgradelar narxi
let multitapCost = 500;
let energyLimitCost = 500;

const displayCoins = document.getElementById('display-coins');
const energyText = document.getElementById('energy-text');
const mainCoin = document.getElementById('main-coin');
const coinSection = document.getElementById('coin-section');

// Ekranni yangilash
function updateUI() {
    displayCoins.innerText = totalCoins.toLocaleString();
    energyText.innerText = `${currentEnergy}/${maxEnergy}`;
    document.getElementById('multitap-cost').innerText = multitapCost;
    document.getElementById('energy-cost').innerText = energyLimitCost;
}

// Telegramning Rasmiy Tugmasini sozlash (Saqlash uchun)
tg.MainButton.setText("🔄 Natijani saqlash va chiqish");
tg.MainButton.color = "#facc15"; // Tilla rang
tg.MainButton.textColor = "#000000";

// Asosiy bosish funksiyasi
function handleTap(e) {
    if (currentEnergy >= tapValue) {
        currentEnergy -= tapValue;
        totalCoins += tapValue;
        sessionEarnedCoins += tapValue;
        updateUI();

        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('light');

        // Foydalanuvchi birinchi marta bosganda Saqlash tugmasi chiqadi
        if (!tg.MainButton.isVisible) {
            tg.MainButton.show();
        }

        // Animatsiya
        const rect = coinSection.getBoundingClientRect();
        let clientX = e.type.includes('touch') ? e.touches[e.touches.length - 1].clientX : e.clientX;
        let clientY = e.type.includes('touch') ? e.touches[e.touches.length - 1].clientY : e.clientY;

        const x = clientX - rect.left;
        const y = clientY - rect.top;

        const floatNum = document.createElement('div');
        floatNum.classList.add('float-text');
        floatNum.innerText = `+${tapValue}`;
        floatNum.style.left = `${x}px`;
        floatNum.style.top = `${y}px`;
        floatNum.style.marginLeft = `${(Math.random() - 0.5) * 40}px`;

        coinSection.appendChild(floatNum);
        setTimeout(() => floatNum.remove(), 1000);
    }
}

// Multitouch
mainCoin.addEventListener('touchstart', (e) => {
    e.preventDefault(); 
    for(let i=0; i < e.changedTouches.length; i++) handleTap(e);
});
mainCoin.addEventListener('mousedown', handleTap);

// Energiya tiklanishi
setInterval(() => {
    if (currentEnergy < maxEnergy) {
        currentEnergy += 1;
        updateUI();
    }
}, 1000);

// --- BOOST PANEL LOGIKASI ---
document.getElementById('open-boosts-btn').addEventListener('click', () => {
    document.getElementById('boost-modal').classList.add('active');
});

document.getElementById('close-boosts-btn').addEventListener('click', () => {
    document.getElementById('boost-modal').classList.remove('active');
});

// Multitap sotib olish
document.getElementById('buy-multitap').addEventListener('click', () => {
    if (totalCoins >= multitapCost) {
        totalCoins -= multitapCost;
        sessionSpentCoins += multitapCost;
        tapValue += 1; // Bosish kuchi 1 taga oshadi
        multitapCost = Math.floor(multitapCost * 2); // Keyingi safar 2 barobar qimmatlashadi
        updateUI();
        if (!tg.MainButton.isVisible) tg.MainButton.show();
        tg.showAlert(`✅ Tabriklaymiz! Endi siz har bosganda ${tapValue} tanga olasiz.`);
    } else {
        tg.showAlert("❌ Bunga tangangiz yetmaydi!");
    }
});

// Energiya Limit sotib olish
document.getElementById('buy-energy').addEventListener('click', () => {
    if (totalCoins >= energyLimitCost) {
        totalCoins -= energyLimitCost;
        sessionSpentCoins += energyLimitCost;
        maxEnergy += 100; // Limit 100 taga oshadi
        energyLimitCost = Math.floor(energyLimitCost * 2);
        updateUI();
        if (!tg.MainButton.isVisible) tg.MainButton.show();
        tg.showAlert(`✅ Tabriklaymiz! Energiya limitingiz ${maxEnergy} ga oshdi.`);
    } else {
        tg.showAlert("❌ Bunga tangangiz yetmaydi!");
    }
});

// Telegram rasmiy tugmasi bosilganda ma'lumotni botga jo'natish
tg.MainButton.onClick(() => {
    const data = {
        earnedCoins: sessionEarnedCoins,
        spentCoins: sessionSpentCoins,
        energy: currentEnergy,
        maxEnergy: maxEnergy,
        tapValue: tapValue
    };
    tg.sendData(JSON.stringify(data)); 
});

updateUI();
