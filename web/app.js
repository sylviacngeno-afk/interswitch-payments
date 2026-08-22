async function loadSystemStatus() {
  const grid = document.getElementById('statusGrid');
  if (!grid) return;
  grid.innerHTML = '<p style="color:#777">Loading status...</p>';
  
  try {
    const response = await fetch('/api/status');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    
    grid.innerHTML = '';
    
    const updated = document.createElement('p');
    updated.style.cssText = 'color:#777; font-size:0.85rem; margin-bottom:16px; grid-column:1/-1;';
    updated.textContent = `Last updated: ${new Date(data.lastUpdated).toLocaleTimeString()}`;
    grid.appendChild(updated);
    
    data.services.forEach(service => {
      const card = document.createElement('div');
      card.className = `status-card ${service.status}`;
      card.innerHTML = `
        <div>
          <span class="service-name">${service.name}</span>
          <span class="service-meta">Uptime: ${service.uptime} | Latency: ${service.latency}</span>
        </div>
        <span class="service-status">
          ${service.status === 'operational' ? 'Operational' : 'Maintenance'}
        </span>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    grid.innerHTML = `<p style="color:#C62828">Could not load status: ${err.message}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadSystemStatus();
  setInterval(loadSystemStatus, 30000);
});
