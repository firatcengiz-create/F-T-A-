/* ═══════════════════════════════════════════════════════════════
   Antigravity Fitness Engine — Frontend Logic
   Lightweight state management  •  Async fetch  •  Particle FX
   ═══════════════════════════════════════════════════════════════ */

// ─── Lightweight State Store ────────────────────────────────
const Store = (() => {
    let _state = {
        profile: null,
        plan: null,
        loading: false,
        antigravityMode: false,
    };
    const _listeners = [];

    return {
        get:       ()       => ({ ..._state }),
        set:       (patch)  => { _state = { ..._state, ...patch }; _listeners.forEach(fn => fn(_state)); },
        subscribe: (fn)     => { _listeners.push(fn); return () => _listeners.splice(_listeners.indexOf(fn), 1); },
    };
})();


// ─── DOM References ─────────────────────────────────────────
const $  = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const dom = {
    form:           $('#profileForm'),
    submitBtn:      $('#submitBtn'),
    resultsSection: $('#resultsSection'),
    planHeader:     $('#planHeader'),
    daysGrid:       $('#daysGrid'),
    tipsCard:       $('#tipsCard'),
    toast:          $('#toast'),
    canvas:         $('#particleCanvas'),
};


// ═══════════════════ API LAYER ══════════════════════════════

async function apiGenerate(profile) {
    const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail?.[0]?.msg || err.detail || 'Generation failed');
    }
    return res.json();
}

async function apiAntigravity() {
    const res = await fetch('/api/antigravity');
    return res.json();
}


// ═══════════════════ FORM HANDLING ══════════════════════════

function scrollToForm() {
    $('#formSection').scrollIntoView({ behavior: 'smooth' });
}

async function handleSubmit(e) {
    e.preventDefault();

    const profile = {
        age:           parseInt($('#age').value, 10),
        weight:        parseFloat($('#weight').value),
        fitness_level: $('#fitnessLevel').value,
        goal:          $('#goal').value,
    };

    Store.set({ loading: true, profile });
    dom.submitBtn.classList.add('btn--loading');
    dom.submitBtn.disabled = true;

    try {
        const plan = await apiGenerate(profile);
        Store.set({ plan, loading: false });
        renderPlan(plan);
        showToast('✨ Program oluşturuldu!');
    } catch (err) {
        showToast('⚠️ ' + err.message);
        Store.set({ loading: false });
    } finally {
        dom.submitBtn.classList.remove('btn--loading');
        dom.submitBtn.disabled = false;
    }
}


// ═══════════════════ RENDERERS ══════════════════════════════

function renderPlan(plan) {
    // — Header
    const totalCals = plan.days.reduce((s, d) => s + d.total_calories, 0);
    const totalMin  = plan.days.reduce((s, d) => s + d.estimated_duration_min, 0);

    dom.planHeader.innerHTML = `
        <h2 class="plan-header__name">${escHtml(plan.plan_name)}</h2>
        <p class="plan-header__desc">${escHtml(plan.description)}</p>
        <div class="plan-header__stats">
            <div class="stat">
                <span class="stat__value">${plan.days_per_week}</span>
                <span class="stat__label">Gün / Hafta</span>
            </div>
            <div class="stat">
                <span class="stat__value">${totalMin}</span>
                <span class="stat__label">Toplam Dk</span>
            </div>
            <div class="stat">
                <span class="stat__value">${totalCals}</span>
                <span class="stat__label">Tahmini kcal</span>
            </div>
            <div class="stat">
                <span class="stat__value">${plan.level}</span>
                <span class="stat__label">Seviye</span>
            </div>
        </div>
    `;

    // — Day cards
    dom.daysGrid.innerHTML = plan.days.map((day, idx) => `
        <div class="day-card${idx === 0 ? ' open' : ''}" data-day="${idx}">
            <div class="day-card__header" onclick="toggleDay(${idx})">
                <div>
                    <div class="day-card__title">${escHtml(day.day)}</div>
                    <div class="day-card__meta">
                        <span>🕒 ${day.estimated_duration_min} dk</span>
                        <span>🔥 ${day.total_calories} kcal</span>
                        <span>🎯 ${escHtml(day.focus)}</span>
                    </div>
                </div>
                <span class="day-card__chevron">▼</span>
            </div>
            <div class="day-card__body">
                <table class="exercise-table">
                    <thead>
                        <tr>
                            <th>Hareket</th>
                            <th>Set</th>
                            <th>Tekrar</th>
                            <th>Dinlenme</th>
                            <th>Yoğunluk</th>
                            <th>Nasıl Yapılır</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${day.exercises.map(renderExerciseRow).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `).join('');

    // — Tips
    dom.tipsCard.innerHTML = `
        <h3>💡 İpuçları</h3>
        <ul class="tips-list">
            ${plan.tips.map(t => `<li>${escHtml(t)}</li>`).join('')}
        </ul>
    `;

    // Show section
    dom.resultsSection.classList.remove('hidden');
    setTimeout(() => {
        dom.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function renderExerciseRow(ex) {
    const intensityClass = ex.intensity.toLowerCase();
    const safeUrl  = escAttr(ex.tutorial_video_url);
    const safeName = escAttr(ex.exercise_name);
    return `
        <tr>
            <td>
                <div class="ex-name">
                    <span class="ex-icon">${ex.icon}</span>
                    ${escHtml(ex.exercise_name)}
                </div>
            </td>
            <td>${ex.sets}</td>
            <td>${escHtml(ex.reps)}</td>
            <td>${escHtml(ex.rest_time)}</td>
            <td><span class="intensity-badge intensity-badge--${intensityClass}">${ex.intensity}</span></td>
            <td>
                <button class="ex-link ex-link--btn"
                        onclick="openVideoModal('${safeUrl}', '${safeName}')">
                    ▶ İzle
                </button>
            </td>
        </tr>
    `;
}

function toggleDay(idx) {
    const card = document.querySelector(`.day-card[data-day="${idx}"]`);
    card.classList.toggle('open');
}


// ═══════════════════ VIDEO MODAL ════════════════════════════

/**
 * Extracts the YouTube video ID from a full URL and returns the
 * nocookie embed URL so the modal never navigates away.
 */
function getYouTubeEmbedUrl(url) {
    try {
        const u = new URL(url);
        let id = u.searchParams.get('v');          // ?v=xxxx
        if (!id) id = u.pathname.split('/').pop();  // youtu.be/xxxx
        if (!id) return url;
        return `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0&modestbranding=1`;
    } catch {
        return url;
    }
}

function openVideoModal(videoUrl, exerciseName) {
    const modal   = $('#videoModal');
    const iframe  = $('#videoIframe');
    const title   = $('#videoModalTitle');
    const embedUrl = getYouTubeEmbedUrl(videoUrl);

    title.textContent = exerciseName;
    iframe.src = embedUrl;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeVideoModal() {
    const modal  = $('#videoModal');
    const iframe = $('#videoIframe');
    modal.classList.remove('active');
    iframe.src = '';          // stop the video
    document.body.style.overflow = '';
}

// Close on backdrop click
document.addEventListener('click', (e) => {
    if (e.target.id === 'videoModal') closeVideoModal();
});

// Close on ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeVideoModal();
});


// ═══════════════════ EXPORT ═════════════════════════════════

function exportJSON() {
    const { plan } = Store.get();
    if (!plan) return;
    const blob = new Blob([JSON.stringify(plan, null, 2)], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = 'antigravity-workout-plan.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('📋 JSON indirildi!');
}


// ═══════════════════ EASTER EGG 🥚 ═════════════════════════

async function triggerAntigravity() {
    try {
        const data = await apiAntigravity();
        Store.set({ antigravityMode: true });
        showToast(`🚀 ${data.message}`);

        // Make elements float
        const targets = $$('.glass-card, .day-card, .hero__badge, .btn--primary');
        targets.forEach((el, i) => {
            el.classList.add('float-element');
            el.style.animationDelay = `${i * 0.15}s`;
        });

        // Sparkle burst
        for (let i = 0; i < 30; i++) {
            createSparkle();
        }

        // Remove after 8 seconds
        setTimeout(() => {
            targets.forEach(el => {
                el.classList.remove('float-element');
                el.style.animationDelay = '';
            });
            Store.set({ antigravityMode: false });
        }, 8000);

    } catch {
        showToast('🥚 Paskalya yumurtası gizli…');
    }
}

function createSparkle() {
    const el = document.createElement('div');
    el.className = 'sparkle';
    el.textContent = ['✦', '✧', '⭐', '💫', '🌟'][Math.floor(Math.random() * 5)];
    el.style.left = Math.random() * window.innerWidth + 'px';
    el.style.top  = Math.random() * window.innerHeight + 'px';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1000);
}


// ═══════════════════ TOAST ══════════════════════════════════

function showToast(msg) {
    dom.toast.textContent = msg;
    dom.toast.classList.remove('hidden');
    dom.toast.classList.add('show');
    setTimeout(() => {
        dom.toast.classList.remove('show');
        setTimeout(() => dom.toast.classList.add('hidden'), 400);
    }, 3000);
}


// ═══════════════════ PARTICLE BACKGROUND ════════════════════

(function initParticles() {
    const canvas = dom.canvas;
    const ctx    = canvas.getContext('2d');
    let w, h, particles;

    function resize() {
        w = canvas.width  = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function createParticles() {
        const count = Math.min(80, Math.floor(w * h / 15000));
        particles = Array.from({ length: count }, () => ({
            x:  Math.random() * w,
            y:  Math.random() * h,
            r:  Math.random() * 2 + 0.5,
            dx: (Math.random() - 0.5) * 0.4,
            dy: (Math.random() - 0.5) * 0.4,
            alpha: Math.random() * 0.4 + 0.1,
        }));
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        for (const p of particles) {
            // move
            p.x += p.dx;
            p.y += p.dy;
            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            // draw dot
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(94, 173, 255, ${p.alpha})`;
            ctx.fill();
        }

        // draw lines between nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const a = particles[i], b = particles[j];
                const dist = Math.hypot(a.x - b.x, a.y - b.y);
                if (dist < 140) {
                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.strokeStyle = `rgba(94, 173, 255, ${0.08 * (1 - dist / 140)})`;
                    ctx.lineWidth = 0.6;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', () => { resize(); createParticles(); });
    resize();
    createParticles();
    draw();
})();


// ═══════════════════ HELPERS ════════════════════════════════

function escHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}
function escAttr(s) {
    return s.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
