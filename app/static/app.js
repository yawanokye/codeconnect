const state = {
  token: localStorage.getItem('code_token'),
  user: null,
  centres: [],
  adminOffices: [],
  channels: [],
};

const api = async (path, options = {}) => {
  const headers = options.headers || {};
  if (!(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    let message = 'Request failed';
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch (_) {}
    throw new Error(message);
  }
  return res.json();
};

const qs = (selector) => document.querySelector(selector);
const el = (tag, className = '', text = '') => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
};

const formatDate = (value) => {
  if (!value) return '';
  const date = new Date(value);
  return date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
};

const roleLabel = (role) => role.replaceAll('_', ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
const canPostOfficial = () => ['SUPER_ADMIN','CODE_ADMIN','MANAGEMENT','PROVOST','COLLEGE_REGISTRAR','DIRECTOR','CAMPUS_DIRECTOR','HEAD_OF_DEPARTMENT','DEPARTMENTAL_REGISTRATION_OFFICER','UNIT_COORDINATOR','SECTION_HEAD','FINANCE_OFFICER','PROCUREMENT_HEAD','ADMISSIONS_HEAD','EXAMS_HEAD','REGIONAL_COORDINATOR','CENTER_COORDINATOR','STUDENT_SUPPORT','QA_OFFICER'].includes(state.user?.role);
const canPostDesag = () => ['SUPER_ADMIN','CODE_ADMIN','DESAG_NATIONAL','DESAG_REGIONAL','DESAG_CENTER'].includes(state.user?.role);
const canManageTicket = () => ['SUPER_ADMIN','CODE_ADMIN','MANAGEMENT','PROVOST','COLLEGE_REGISTRAR','DIRECTOR','CAMPUS_DIRECTOR','HEAD_OF_DEPARTMENT','DEPARTMENTAL_REGISTRATION_OFFICER','UNIT_COORDINATOR','SECTION_HEAD','FINANCE_OFFICER','PROCUREMENT_HEAD','ADMISSIONS_HEAD','EXAMS_HEAD','REGIONAL_COORDINATOR','CENTER_COORDINATOR','STUDENT_SUPPORT','QA_OFFICER','DESAG_NATIONAL','DESAG_REGIONAL','DESAG_CENTER'].includes(state.user?.role);
const canCreateChannel = () => ['SUPER_ADMIN','CODE_ADMIN','MANAGEMENT','REGIONAL_COORDINATOR','CENTER_COORDINATOR','TUTOR','DESAG_NATIONAL','DESAG_REGIONAL','DESAG_CENTER','CLASS_REP'].includes(state.user?.role);

function showApp() {
  qs('#loginView').classList.add('hidden');
  qs('#appView').classList.remove('hidden');
  qs('#logoutBtn').classList.remove('hidden');
}

function showLogin() {
  qs('#loginView').classList.remove('hidden');
  qs('#appView').classList.add('hidden');
  qs('#logoutBtn').classList.add('hidden');
}

async function bootstrap() {
  if (!state.token) return showLogin();
  try {
    state.user = await api('/api/auth/me');
    showApp();
    await loadAll();
  } catch (err) {
    localStorage.removeItem('code_token');
    state.token = null;
    showLogin();
  }
}

async function loadAll() {
  qs('#userName').textContent = state.user.full_name;
  qs('#userRole').textContent = `${roleLabel(state.user.role)}${state.user.region ? ' • ' + state.user.region : ''}${state.user.programme ? ' • ' + state.user.programme : ''}${state.user.level ? ' • Level ' + state.user.level : ''}`;
  await Promise.all([
    loadLinks(),
    loadDashboard(),
    loadCentres(),
    renderOfficial(),
    renderDesag(),
    renderAdminOffices(),
    renderTickets(),
    renderEvents(),
    renderDiscussions(),
  ]);
}

async function loadLinks() {
  const links = await api('/api/links');
  const host = qs('#quickLinks');
  host.innerHTML = '';
  [
    ['MyUCC Portal', links.myucc_url],
    ['UCC eLearning', links.ucc_elearning_url],
    ['CoDE Website', links.code_website_url],
  ].forEach(([label, url]) => {
    const a = el('a', 'link-button', label);
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener';
    host.appendChild(a);
  });
}

async function loadDashboard() {
  const data = await api('/api/dashboard');
  const cards = [
    ['Users', data.users],
    ['Study Centres', data.centres],
    ['Admin Offices', data.administrative_offices],
    ['CoDE Notices', data.announcements],
    ['DESAG Notices', data.desag_announcements],
    ['Open Tickets', data.open_tickets],
    ['Events', data.events],
    ['Discussion Rooms', data.discussion_channels],
  ];
  qs('#statsGrid').innerHTML = cards.map(([label, value]) => `
    <article class="stat-card"><h3>${value}</h3><p>${label}</p></article>
  `).join('');
}

async function loadCentres() {
  state.centres = await api('/api/centres');
}

function centreOptions(selected = '') {
  return `<option value="">No specific centre</option>` + state.centres.map(c => `<option value="${c.id}" ${String(selected) === String(c.id) ? 'selected' : ''}>${c.name} • ${c.region}</option>`).join('');
}

function noticeCard(item, desag = false) {
  return `
    <article class="item-card">
      <div class="item-head">
        <h3>${escapeHtml(item.title)}</h3>
        <span class="badge ${desag ? 'desag' : ''}">${item.scope_type}</span>
      </div>
      <p>${escapeHtml(item.body)}</p>
      <small>${formatDate(item.created_at)}${item.region ? ' • ' + item.region : ''}${item.programme ? ' • ' + item.programme : ''}</small>
    </article>`;
}

async function renderOfficial() {
  const host = qs('#official');
  const notices = await api('/api/announcements?notice_type=OFFICIAL_CODE');
  host.innerHTML = `
    <div class="module-head">
      <div><p class="eyebrow">Verified college communication</p><h2>Official CoDE notices</h2><p class="muted">Official notices must stay separate from DESAG and peer communication.</p></div>
    </div>
    <div class="two-col">
      ${canPostOfficial() ? officialForm('OFFICIAL_CODE') : `<div class="empty">Only approved CoDE officers can publish official notices.</div>`}
      <div class="list">${notices.length ? notices.map(n => noticeCard(n)).join('') : '<div class="empty">No official notices yet.</div>'}</div>
    </div>`;
  attachNoticeForm('officialNoticeForm');
}

function officialForm(type) {
  return `
    <form id="${type === 'DESAG' ? 'desagNoticeForm' : 'officialNoticeForm'}" class="form-grid item-card">
      <h3>Post notice</h3>
      <input name="title" placeholder="Title" required />
      <textarea name="body" placeholder="Write the notice" required></textarea>
      <div class="row">
        <select name="scope_type">
          <option value="ALL">All</option>
          <option value="NATIONAL">National</option>
          <option value="REGIONAL">Regional</option>
          <option value="CENTER">Centre</option>
          <option value="PROGRAMME">Programme</option>
        </select>
        <input name="region" placeholder="Region, optional" />
      </div>
      <div class="row">
        <input name="programme" placeholder="Programme, optional" />
        <input name="level" placeholder="Level, optional" />
      </div>
      <select name="center_id">${centreOptions()}</select>
      <input type="hidden" name="notice_type" value="${type}" />
      <button type="submit">Publish</button>
      <p class="success"></p>
    </form>`;
}

function attachNoticeForm(id) {
  const form = qs(`#${id}`);
  if (!form) return;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = formData(form);
    data.center_id = data.center_id ? Number(data.center_id) : null;
    try {
      await api('/api/announcements', { method: 'POST', body: JSON.stringify(data) });
      form.reset();
      if (id.includes('desag')) await renderDesag();
      else await renderOfficial();
      await loadDashboard();
    } catch (err) {
      form.querySelector('.success').textContent = err.message;
      form.querySelector('.success').className = 'error';
    }
  });
}

async function renderDesag() {
  const host = qs('#desag');
  const notices = await api('/api/announcements?notice_type=DESAG');
  const events = await api('/api/events?event_type=DESAG');
  host.innerHTML = `
    <div class="module-head">
      <div><p class="eyebrow">Student governance and welfare</p><h2>DESAG module</h2><p class="muted">Managed by DESAG from national to regional and centre levels, with clear separation from official CoDE notices.</p></div>
    </div>
    <div class="two-col">
      ${canPostDesag() ? officialForm('DESAG') : `<div class="empty">DESAG executives can publish notices and activities here.</div>`}
      <div class="list">
        <h3>DESAG notices</h3>
        ${notices.length ? notices.map(n => noticeCard(n, true)).join('') : '<div class="empty">No DESAG notices yet.</div>'}
        <h3>DESAG activities</h3>
        ${events.length ? events.map(eventCard).join('') : '<div class="empty">No DESAG activities yet.</div>'}
      </div>
    </div>`;
  attachNoticeForm('desagNoticeForm');
}

async function renderCentres() {
  const host = qs('#centres');
  host.innerHTML = `
    <div class="module-head"><div><p class="eyebrow">Operational network</p><h2>Study centres</h2></div></div>
    <div class="list">
      ${state.centres.length ? state.centres.map(c => `
        <article class="item-card">
          <div class="item-head"><h3>${escapeHtml(c.name)}</h3><span class="badge">${escapeHtml(c.region)}</span></div>
          <p>${escapeHtml(c.town || '')}${c.zone ? ' • ' + escapeHtml(c.zone) + ' zone' : ''}</p>
          <small>${escapeHtml(c.coordinator_name || 'Coordinator not set')} ${c.coordinator_phone ? ' • ' + escapeHtml(c.coordinator_phone) : ''}</small>
        </article>`).join('') : '<div class="empty">No centres have been created.</div>'}
    </div>`;
}

async function renderTickets() {
  const host = qs('#tickets');
  const tickets = await api('/api/tickets');
  host.innerHTML = `
    <div class="module-head"><div><p class="eyebrow">Helpdesk and escalation</p><h2>Student tickets</h2><p class="muted">Use this to track registration, fee confirmation, timetable, examination, and welfare concerns.</p></div></div>
    <div class="two-col">
      <form id="ticketForm" class="form-grid item-card">
        <h3>Create ticket</h3>
        <input name="subject" placeholder="Subject" required />
        <select name="category">
          <option>Registration problem</option>
          <option>Departmental registration issue</option>
          <option>Fee/payment confirmation issue</option>
          <option>Missing results</option>
          <option>Timetable clash</option>
          <option>Module/material issue</option>
          <option>Examination issue</option>
          <option>Centre-related complaint</option>
          <option>DESAG welfare concern</option>
        </select>
        <textarea name="description" placeholder="Describe the issue" required></textarea>
        <div class="row">
          <select name="priority"><option>NORMAL</option><option>HIGH</option><option>URGENT</option></select>
          <select name="center_id">${centreOptions(state.user.center_id || '')}</select>
        </div>
        <button type="submit">Submit ticket</button>
        <p class="success"></p>
      </form>
      <div class="list">
        ${tickets.length ? tickets.map(ticketCard).join('') : '<div class="empty">No tickets yet.</div>'}
      </div>
    </div>`;
  qs('#ticketForm').addEventListener('submit', submitTicket);
  document.querySelectorAll('[data-ticket-close]').forEach(button => {
    button.addEventListener('click', async () => {
      await api(`/api/tickets/${button.dataset.ticketClose}`, { method: 'PATCH', body: JSON.stringify({ status: 'CLOSED' }) });
      await renderTickets();
      await loadDashboard();
    });
  });
}

function ticketCard(t) {
  return `
    <article class="item-card">
      <div class="item-head"><h3>${escapeHtml(t.subject)}</h3><span class="badge ${t.status === 'CLOSED' ? 'good' : 'open'}">${t.status}</span></div>
      <p>${escapeHtml(t.description)}</p>
      <small>${t.reference} • ${escapeHtml(t.category)} • ${formatDate(t.created_at)}</small>
      ${canManageTicket() && t.status !== 'CLOSED' ? `<p><button class="secondary" data-ticket-close="${t.id}">Close ticket</button></p>` : ''}
    </article>`;
}

async function submitTicket(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = formData(form);
  data.center_id = data.center_id ? Number(data.center_id) : null;
  try {
    await api('/api/tickets', { method: 'POST', body: JSON.stringify(data) });
    form.reset();
    await renderTickets();
    await loadDashboard();
  } catch (err) {
    form.querySelector('.success').textContent = err.message;
    form.querySelector('.success').className = 'error';
  }
}

async function renderEvents() {
  const host = qs('#events');
  const events = await api('/api/events');
  host.innerHTML = `
    <div class="module-head"><div><p class="eyebrow">Academic calendar</p><h2>Timetable and events</h2><p class="muted">Add face-to-face sessions, deadlines, DESAG activities, and centre-specific events.</p></div></div>
    <div class="two-col">
      ${(canPostOfficial() || canPostDesag()) ? eventForm() : `<div class="empty">Approved users can create events.</div>`}
      <div class="list">${events.length ? events.map(eventCard).join('') : '<div class="empty">No events yet.</div>'}</div>
    </div>`;
  const form = qs('#eventForm');
  if (form) form.addEventListener('submit', submitEvent);
}

function eventForm() {
  return `
    <form id="eventForm" class="form-grid item-card">
      <h3>Create event</h3>
      <input name="title" placeholder="Title" required />
      <textarea name="description" placeholder="Description"></textarea>
      <div class="row">
        <select name="event_type">
          <option value="CODE">CoDE event</option>
          <option value="ACADEMIC">Academic deadline</option>
          <option value="TIMETABLE">Timetable entry</option>
          <option value="DESAG">DESAG activity</option>
        </select>
        <input name="region" placeholder="Region, optional" />
      </div>
      <div class="row">
        <label>Start <input name="start_at" type="datetime-local" required /></label>
        <label>End <input name="end_at" type="datetime-local" /></label>
      </div>
      <div class="row">
        <input name="programme" placeholder="Programme, optional" />
        <input name="level" placeholder="Level, optional" />
      </div>
      <select name="center_id">${centreOptions()}</select>
      <button type="submit">Create event</button>
      <p class="success"></p>
    </form>`;
}

function eventCard(e) {
  return `
    <article class="item-card">
      <div class="item-head"><h3>${escapeHtml(e.title)}</h3><span class="badge ${e.event_type === 'DESAG' ? 'desag' : ''}">${e.event_type}</span></div>
      <p>${escapeHtml(e.description || '')}</p>
      <small>${formatDate(e.start_at)}${e.end_at ? ' to ' + formatDate(e.end_at) : ''}${e.region ? ' • ' + escapeHtml(e.region) : ''}</small>
    </article>`;
}

async function submitEvent(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = formData(form);
  data.center_id = data.center_id ? Number(data.center_id) : null;
  data.end_at = data.end_at || null;
  try {
    await api('/api/events', { method: 'POST', body: JSON.stringify(data) });
    form.reset();
    await renderEvents();
    await renderDesag();
    await loadDashboard();
  } catch (err) {
    form.querySelector('.success').textContent = err.message;
    form.querySelector('.success').className = 'error';
  }
}

async function renderAdminOffices() {
  const host = qs('#adminOffices');
  state.adminOffices = await api('/api/admin-offices');
  host.innerHTML = `
    <div class="module-head"><div><p class="eyebrow">Administrative dashboards</p><h2>CoDE offices that need dashboards</h2><p class="muted">These offices should have dashboards because they manage College-wide leadership, academic programmes, campuses, sections, units, student support, field coordination, and DESAG liaison.</p></div></div>
    <div class="office-grid">
      ${state.adminOffices.length ? state.adminOffices.map(officeCard).join('') : '<div class="empty">No administrative offices configured.</div>'}
    </div>`;
}

function officeCard(office) {
  const modules = (office.key_modules || '').split(',').map(item => item.trim()).filter(Boolean);
  return `
    <article class="item-card office-card">
      <div class="item-head">
        <h3>${escapeHtml(office.name)}</h3>
        <span class="badge">${escapeHtml(office.office_type)}</span>
      </div>
      <p><strong>${escapeHtml(office.lead_title || office.dashboard_role)}</strong>${office.lead_name ? ' • ' + escapeHtml(office.lead_name) : ''}</p>
      <p>${escapeHtml(office.scope || '')}</p>
      <small>${office.reporting_line ? 'Reports to: ' + escapeHtml(office.reporting_line) : ''}</small>
      <div class="permission-list">
        <span>${office.can_publish_official ? 'Can publish official notices' : 'No official publishing'}</span>
        <span>${office.can_handle_tickets ? 'Can handle tickets' : 'View only'}</span>
        <span>${office.can_view_analytics ? 'Analytics dashboard' : 'No analytics'}</span>
      </div>
      ${modules.length ? `<ul>${modules.map(m => `<li>${escapeHtml(m)}</li>`).join('')}</ul>` : ''}
    </article>`;
}

async function renderDiscussions() {
  const host = qs('#discussions');
  state.channels = await api('/api/discussions/channels');
  host.innerHTML = `
    <div class="module-head"><div><p class="eyebrow">Collaborative environment</p><h2>Discussion rooms</h2><p class="muted">Programme, course, centre, and DESAG rooms can support peer learning and reduce misinformation.</p></div></div>
    <div class="two-col">
      ${canCreateChannel() ? channelForm() : `<div class="empty">Tutors, coordinators, DESAG executives, class reps, and admins can create rooms.</div>`}
      <div class="list">
        ${state.channels.length ? state.channels.map(channelCard).join('') : '<div class="empty">No channels yet.</div>'}
      </div>
    </div>`;
  const form = qs('#channelForm');
  if (form) form.addEventListener('submit', submitChannel);
  document.querySelectorAll('[data-open-channel]').forEach(button => {
    button.addEventListener('click', () => openChannel(Number(button.dataset.openChannel)));
  });
}

function channelForm() {
  return `
    <form id="channelForm" class="form-grid item-card">
      <h3>Create discussion room</h3>
      <input name="name" placeholder="Room name" required />
      <textarea name="description" placeholder="Purpose of the room"></textarea>
      <div class="row">
        <select name="channel_type"><option>COURSE</option><option>PROGRAMME</option><option>CENTRE</option><option>DESAG</option><option>GENERAL</option></select>
        <input name="region" placeholder="Region, optional" />
      </div>
      <div class="row">
        <input name="programme" placeholder="Programme, optional" />
        <input name="level" placeholder="Level, optional" />
      </div>
      <select name="center_id">${centreOptions()}</select>
      <button type="submit">Create room</button>
      <p class="success"></p>
    </form>`;
}

function channelCard(c) {
  return `
    <article class="item-card">
      <div class="item-head"><h3>${escapeHtml(c.name)}</h3><span class="badge ${c.channel_type === 'DESAG' ? 'desag' : ''}">${c.channel_type}</span></div>
      <p>${escapeHtml(c.description || '')}</p>
      <small>${c.region ? escapeHtml(c.region) + ' • ' : ''}${c.programme ? escapeHtml(c.programme) + ' • ' : ''}${formatDate(c.created_at)}</small>
      <p><button class="secondary" data-open-channel="${c.id}">Open room</button></p>
      <div id="channel-${c.id}" class="hidden"></div>
    </article>`;
}

async function submitChannel(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const data = formData(form);
  data.center_id = data.center_id ? Number(data.center_id) : null;
  try {
    await api('/api/discussions/channels', { method: 'POST', body: JSON.stringify(data) });
    form.reset();
    await renderDiscussions();
    await loadDashboard();
  } catch (err) {
    form.querySelector('.success').textContent = err.message;
    form.querySelector('.success').className = 'error';
  }
}

async function openChannel(channelId) {
  const host = qs(`#channel-${channelId}`);
  const messages = await api(`/api/discussions/channels/${channelId}/messages`);
  host.classList.remove('hidden');
  host.innerHTML = `
    <div class="list">
      ${messages.length ? messages.map(m => `<div class="item-card"><p>${escapeHtml(m.body)}</p><small>${formatDate(m.created_at)}</small></div>`).join('') : '<div class="empty">No messages yet.</div>'}
    </div>
    <form class="form-grid" data-message-form="${channelId}">
      <textarea name="body" placeholder="Write a message" required></textarea>
      <button type="submit">Send message</button>
    </form>`;
  host.querySelector('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = formData(event.currentTarget);
    await api(`/api/discussions/channels/${channelId}/messages`, { method: 'POST', body: JSON.stringify(data) });
    await openChannel(channelId);
  });
}

function formData(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach(key => {
    if (data[key] === '') data[key] = null;
  });
  return data;
}

function escapeHtml(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

qs('#loginForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  qs('#loginError').textContent = '';
  try {
    const payload = { email: qs('#email').value, password: qs('#password').value };
    const data = await api('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) });
    state.token = data.access_token;
    state.user = data.user;
    localStorage.setItem('code_token', state.token);
    showApp();
    await loadAll();
  } catch (err) {
    qs('#loginError').textContent = err.message;
  }
});

qs('#logoutBtn').addEventListener('click', () => {
  localStorage.removeItem('code_token');
  state.token = null;
  state.user = null;
  showLogin();
});

document.querySelectorAll('.tab').forEach(button => {
  button.addEventListener('click', async () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.add('hidden'));
    button.classList.add('active');
    qs(`#${button.dataset.tab}`).classList.remove('hidden');
    if (button.dataset.tab === 'centres') await renderCentres();
    if (button.dataset.tab === 'adminOffices') await renderAdminOffices();
  });
});

bootstrap();
