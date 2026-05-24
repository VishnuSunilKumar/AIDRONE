// Update face count every second
setInterval(() => {
  fetch('/api/face_count')
    .then(res => res.json())
    .then(data => {
      document.getElementById('faceCount').textContent = data.face_count;
    });
}, 1000);

// Snapshot function
function takeSnapshot() {
  fetch('/api/snapshot', { method: 'POST' })
    .then(res => res.json())
    .then(data => alert(data.message || data.error));
}

// Map and device location
const map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

navigator.geolocation.getCurrentPosition(position => {
  const lat = position.coords.latitude;
  const lng = position.coords.longitude;
  map.setView([lat, lng], 15);
  L.marker([lat, lng]).addTo(map).bindPopup('Device Location').openPopup();

  fetch('/api/location', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lat, lng })
  });
});
