const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

let coins = 0;
let olmos = 0;
let currentEnergy = 1000;
let maxEnergy = 1000;

const coinBtn = document.getElementById('coinBtn');
const tapArea = document.getElementById('tapArea');

function handleTap(x, y) {
    if (currentEnergy > 0) {
        coins += 1;
        currentEnergy -= 1;
        updateUI();
        
        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('light');
        createFloatNum(x, y);
    }
}

// MULTI-TOUCH (Bir nechta barmoq bilan tezkor bosishni qo'llash)
coinBtn.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Ekran surilib ketmasligi va tez ishlashi uchun
    coinBtn.classList.add('pressed');
    
    const rect = tapArea.getBoundingClientRect();
    // Har bir teggan barmoqni alohida hisoblaymiz
    for (let i = 0; i < e.changedTouches.length; i++) {
        let touch = e.changedTouches[i];
        handleTap(touch.clientX, touch.clientY - rect.top);
    }
}, { passive: false });

coinBtn.addEventListener('touchend', () => {
    coinBtn.classList.remove('pressed');
});

// Sichqoncha bilan bosganda ham ishlashi uchun (Kompyuterda)
coinBtn.addEventListener('mousedown', (e) => {
    coinBtn.classList.add('pressed');
    const rect = tapArea.getBoundingClientRect();
    handleTap(e.clientX, e.clientY - rect.top);
});
coinBtn.addEventListener('mouseup', () => coinBtn.classList.remove('pressed'));

// Energiyani tiklash (Soniyasiga +3 energiya)
setInterval(() => {
    if (currentEnergy < maxEnergy) {
        currentEnergy = Math.min(maxEnergy, currentEnergy + 3);
        updateUI();
    }
}, 1000);

function updateUI() {
    document.getElementById('coinBalance').innerText = coins;
    document.getElementById('chipBalance').innerText = olmos;
    document.getElementById('energyText').innerText = currentEnergy;
    document.getElementById('energyFill').style.width = (currentEnergy / maxEnergy * 100) + '%';
}

function createFloatNum(x, y) {
    const el = document.createElement('div');
    el.className = 'floating-number';
    el.innerText = '+1';
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    tapArea.appendChild(el);
    
    setTimeout(() => {
        el.style.transform = 'translateY(-100px) scale(1.2)';
        el.style.opacity = '0';
    }, 20);
    
    setTimeout(() => el.remove(), 600);
}
