const API_URL = 'http://127.0.0.1:8000/api';

let cart            = JSON.parse(localStorage.getItem('aura_cart')) || [];
let currentFile     = null;
let activeTryOnItem = null;
let allProducts     = [];
let cameraStream    = null;

document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();
    loadStorefront();
    updateCartUI();
});

// ── API STATUS ────────────────────────────
async function checkApiStatus() {
    const el = document.getElementById('apiStatus');
    try {
        const res = await fetch('http://127.0.0.1:8000/');
        if (res.ok) {
            el.innerHTML = '⬤ Online';
            el.style.color = '#2d8c4e';
        }
    } catch {
        el.innerHTML = '⬤ Offline';
        el.style.color = '#b91c1c';
    }
}

// ── STOREFRONT ────────────────────────────
async function loadStorefront() {
    try {
        const res   = await fetch(`${API_URL}/products`);
        allProducts = await res.json();
        renderCards('storeEarrings',  allProducts.filter(p => p.type === 'earring'));
        renderCards('storeNecklaces', allProducts.filter(p => p.type === 'necklace'));
    } catch (e) {
        console.error("Failed to load products", e);
    }
}

function renderCards(containerId, items) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    items.forEach(item => {
        const discount = Math.round((1 - item.price / item.original_price) * 100);

        const card = document.createElement('div');
        card.className = 'j-card';
        card.innerHTML = `
            <div class="j-card-img">
                <img src="http://127.0.0.1:8000/static/jewellery/${item.image}"
                     alt="${item.name}"
                     onerror="this.style.display='none'">
            </div>
            <div class="j-card-body">
                <div class="j-card-name">${item.name}</div>
                <div class="j-card-rating">
                    <span>★</span> ${item.rating} (${item.reviews} reviews)
                </div>
                <div class="j-card-prices">
                    <span class="price-now">₹${item.price.toLocaleString()}</span>
                    <span class="price-old">₹${item.original_price.toLocaleString()}</span>
                    <span class="price-discount">${discount}% off</span>
                </div>
                <div class="j-card-actions">
                    <button class="btn-tryon" onclick="openTryOn(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                        ✨ Virtual Try-On
                    </button>
                    <button class="btn-cart" onclick="addToCart(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                        Add to Cart
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// ── CART ──────────────────────────────────
function addToCart(product) {
    if (!product) return;
    const idx = cart.findIndex(i => i.id === product.id);
    if (idx > -1) cart[idx].quantity += 1;
    else cart.push({ ...product, quantity: 1 });
    localStorage.setItem('aura_cart', JSON.stringify(cart));
    updateCartUI();

    // Flash feedback
    const btn = document.getElementById('cartBtn');
    btn.style.background = '#2d8c4e';
    setTimeout(() => btn.style.background = '', 600);
}

function updateCartUI() {
    const total = cart.reduce((s, i) => s + i.quantity, 0);
    document.getElementById('cartCount').textContent = total;
}

async function checkout() {
    if (cart.length === 0) return alert("Your cart is empty!");

    const total = cart.reduce((s, i) => s + i.price * i.quantity, 0);
    const orderData = {
        customer_name:  "Guest User",
        customer_email: "guest@aura.com",
        customer_phone: "0000000000",
        items: cart.map(i => ({
            jewellery_id: i.id,
            name:         i.name,
            price:        i.price,
            quantity:     i.quantity
        })),
        total
    };

    try {
        const res  = await fetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });
        const data = await res.json();
        if (res.ok) {
            alert(`🎉 ${data.message}\nOrder ID: ${data.order_id}`);
            cart = [];
            localStorage.removeItem('aura_cart');
            updateCartUI();
        }
    } catch { alert("Could not connect to server."); }
}

// ── TRY-ON NAVIGATION ─────────────────────
function openTryOn(item) {
    activeTryOnItem = item;
    document.getElementById('storeView').style.display  = 'none';
    document.getElementById('tryonView').style.display  = 'block';
    document.getElementById('tryonTitle').textContent   = item.name;
    document.getElementById('tryonPrice').textContent   = item.price.toLocaleString();

    // Reset state
    resetUpload();
    document.getElementById('resultCard') && (document.getElementById('resultCard').style.display = 'none');
    document.getElementById('canvasContainer').style.display  = 'none';
    document.getElementById('canvasPlaceholder').style.display = 'flex';
    document.getElementById('dragHint').style.display         = 'none';
    document.getElementById('errorBox').style.display         = 'none';
    document.querySelectorAll('.draggable-jewellery').forEach(j => j.remove());

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function closeTryOn() {
    document.getElementById('tryonView').style.display = 'none';
    document.getElementById('storeView').style.display = 'block';
    if (cameraStream) stopCamera();
    currentFile     = null;
    activeTryOnItem = null;
}

// ── TABS ──────────────────────────────────
function switchTab(tab) {
    document.getElementById('tabUpload').classList.toggle('active', tab === 'upload');
    document.getElementById('tabCamera').classList.toggle('active', tab === 'camera');
    document.getElementById('uploadSection').style.display = tab === 'upload' ? 'block' : 'none';
    document.getElementById('cameraSection').style.display = tab === 'camera' ? 'block' : 'none';
    if (tab === 'upload' && cameraStream) stopCamera();
}

// ── UPLOAD ────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('fileInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        currentFile = file;
        document.getElementById('uploadBox').style.display     = 'none';
        document.getElementById('photoPreview').style.display  = 'block';
        document.getElementById('previewImg').src = URL.createObjectURL(file);
    });
});

function resetUpload() {
    currentFile = null;
    const fi = document.getElementById('fileInput');
    if (fi) fi.value = '';
    document.getElementById('uploadBox').style.display    = 'block';
    document.getElementById('photoPreview').style.display = 'none';
}

// ── CAMERA ────────────────────────────────
async function startCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: 480 }
        });
        const video = document.getElementById('video');
        video.srcObject = cameraStream;
        video.style.display = 'block';
        document.getElementById('startCamBtn').style.display = 'none';
        document.getElementById('snapBtn').style.display     = 'inline-block';
    } catch { alert("Camera access denied."); }
}

function snapPhoto() {
    const video  = document.getElementById('video');
    const canvas = document.getElementById('cameraCanvas');
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.toBlob(blob => {
        currentFile = new File([blob], "snap.jpg", { type: "image/jpeg" });
        document.getElementById('snapPreview').style.display = 'block';
        document.getElementById('snapImg').src = URL.createObjectURL(blob);
        document.getElementById('snapBtn').style.display    = 'none';
        stopCamera();
    }, 'image/jpeg', 0.95);
}

function retake() {
    currentFile = null;
    document.getElementById('snapPreview').style.display = 'none';
    startCamera();
}

function stopCamera() {
    if (cameraStream) { cameraStream.getTracks().forEach(t => t.stop()); cameraStream = null; }
    const v = document.getElementById('video');
    if (v) v.style.display = 'none';
    document.getElementById('startCamBtn').style.display = 'inline-block';
    document.getElementById('snapBtn').style.display     = 'none';
}

// ── TRY-ON ENGINE ─────────────────────────
async function runTryon() {
    if (!currentFile) return showError("Please upload or take a photo first.");

    const btn  = document.getElementById('tryonBtn');
    const text = document.getElementById('tryonBtnText');
    btn.disabled  = true;
    text.textContent = '⏳ Processing...';
    hideError();

    const formData = new FormData();
    formData.append('file', currentFile);

    if (activeTryOnItem.type === 'earring')
        formData.append('earring_id', activeTryOnItem.id);
    else
        formData.append('necklace_id', activeTryOnItem.id);

    try {
        const res  = await fetch(`${API_URL}/tryon`, { method: 'POST', body: formData });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Try-on failed");

        // Show canvas, hide placeholder
        document.getElementById('canvasPlaceholder').style.display = 'none';
        document.getElementById('canvasContainer').style.display   = 'block';
        document.getElementById('dragHint').style.display          = 'block';

        // Set base image
        const baseImg = document.getElementById('baseImage');
        baseImg.src   = URL.createObjectURL(currentFile);

        baseImg.onload = function() {
            // Scale factor: rendered size vs actual pixel size
            const scaleX = baseImg.clientWidth  / data.image_size.width;
            const scaleY = baseImg.clientHeight / data.image_size.height;

            // Remove old jewellery
            document.querySelectorAll('.draggable-jewellery').forEach(j => j.remove());

            const container = document.getElementById('canvasContainer');

            if (data.earring_left)  spawnItem(container, activeTryOnItem.image, data.earring_left,  scaleX, scaleY, false);
            if (data.earring_right) spawnItem(container, activeTryOnItem.image, data.earring_right, scaleX, scaleY, true);
            if (data.necklace)      spawnItem(container, activeTryOnItem.image, data.necklace,      scaleX, scaleY, false);
        };

    } catch (err) {
        showError(err.message.includes('fetch') ? 'Cannot connect to backend.' : err.message);
    } finally {
        btn.disabled     = false;
        text.textContent = '✨ Generate Try-On';
    }
}

function spawnItem(container, imageFile, coords, scaleX, scaleY, flip) {
    const img     = document.createElement('img');
    img.src       = `http://127.0.0.1:8000/static/jewellery/${imageFile}`;
    img.className = 'draggable-jewellery';

    img.style.left   = (coords.x * scaleX) + 'px';
    img.style.top    = (coords.y * scaleY) + 'px';
    img.style.width  = (coords.width  * scaleX) + 'px';
    img.style.height = (coords.height * scaleY) + 'px';
    if (flip) img.style.transform = 'scaleX(-1)';

    container.appendChild(img);
    makeDraggable(img);
}

// ── DRAG ENGINE ───────────────────────────
function makeDraggable(el) {
    let x1=0, y1=0, x2=0, y2=0;
    el.onmousedown = function(e) {
        e.preventDefault();
        x2 = e.clientX; y2 = e.clientY;
        document.onmousemove = function(e) {
            x1 = x2 - e.clientX; y1 = y2 - e.clientY;
            x2 = e.clientX;      y2 = e.clientY;
            el.style.top  = (el.offsetTop  - y1) + 'px';
            el.style.left = (el.offsetLeft - x1) + 'px';
        };
        document.onmouseup = () => {
            document.onmousemove = null;
            document.onmouseup   = null;
        };
    };
}

// ── HELPERS ───────────────────────────────
function showError(msg) {
    const box = document.getElementById('errorBox');
    box.textContent   = '⚠ ' + msg;
    box.style.display = 'block';
}

function hideError() {
    document.getElementById('errorBox').style.display = 'none';
}