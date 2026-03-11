let papers = [];

const tabs = document.querySelectorAll('nav button');
tabs.forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.tab').forEach(s => s.classList.remove('active'));
  document.getElementById(btn.dataset.tab).classList.add('active');
}));

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  return res.json();
}

async function loadPapers() {
  const data = await fetchJSON('/api/papers');
  papers = data.papers;
  const el = document.getElementById('paperList');
  el.innerHTML = papers.map(p => `
    <label class="paper-row">
      <input type="checkbox" value="${p.id}" />
      <span>#${p.id} ${p.title} ${p.doi ? `(DOI: ${p.doi})` : ''}</span>
    </label>
  `).join('') || '<p>暂无文献</p>';
}

document.getElementById('refreshBtn').addEventListener('click', loadPapers);

document.getElementById('importBtn').addEventListener('click', async () => {
  const input = document.getElementById('paperInput').value;
  const data = await fetchJSON('/api/import-papers', { method: 'POST', body: JSON.stringify({ input }) });
  document.getElementById('importResult').innerText = `成功导入 ${data.count} 条`;
  await loadPapers();
});

function selectedIds() {
  return [...document.querySelectorAll('#paperList input:checked')].map(i => Number(i.value));
}

document.getElementById('exportBtn').addEventListener('click', async () => {
  const ids = selectedIds();
  const data = await fetchJSON(`/api/export-bibtex?ids=${ids.join(',')}`);
  document.getElementById('bibtexOutput').value = data.bibtex;
});

async function loadZoteroConfig() {
  const data = await fetchJSON('/api/zotero-config');
  const zotero = data.zotero || {};
  document.getElementById('zoteroUserId').value = zotero.user_id || '';
  document.getElementById('zoteroApiKey').value = zotero.api_key || '';
  document.getElementById('zoteroLibraryType').value = zotero.library_type || 'user';
  document.getElementById('zoteroCollectionKey').value = zotero.collection_key || '';
}

document.getElementById('pushToZoteroBtn').addEventListener('click', async () => {
  const ids = selectedIds();
  const zotero = {
    user_id: document.getElementById('zoteroUserId').value,
    api_key: document.getElementById('zoteroApiKey').value,
    library_type: document.getElementById('zoteroLibraryType').value,
    collection_key: document.getElementById('zoteroCollectionKey').value,
  };
  const data = await fetchJSON('/api/import-to-zotero', {
    method: 'POST',
    body: JSON.stringify({ paper_ids: ids, zotero })
  });
  document.getElementById('zoteroResult').innerText = JSON.stringify(data, null, 2);
});

async function loadLlmConfig() {
  const data = await fetchJSON('/api/llm-config');
  const container = document.getElementById('llmConfig');
  container.innerHTML = data.providers.map((p, idx) => `
    <div class="llm-item" data-idx="${idx}">
      <label><input type="checkbox" class="enabled" ${p.enabled ? 'checked' : ''}/>启用 ${p.name}</label>
      <input class="name" value="${p.name}" />
      <input class="base_url" value="${p.base_url}" />
      <input class="model" value="${p.model}" />
      <input class="api_key" value="${p.api_key}" placeholder="API Key" />
    </div>
  `).join('');
}

document.getElementById('saveSettingsBtn').addEventListener('click', async () => {
  const providers = [...document.querySelectorAll('.llm-item')].map(item => ({
    name: item.querySelector('.name').value,
    base_url: item.querySelector('.base_url').value,
    model: item.querySelector('.model').value,
    api_key: item.querySelector('.api_key').value,
    enabled: item.querySelector('.enabled').checked,
  }));
  const zotero = {
    user_id: document.getElementById('zoteroUserId').value,
    api_key: document.getElementById('zoteroApiKey').value,
    library_type: document.getElementById('zoteroLibraryType').value,
    collection_key: document.getElementById('zoteroCollectionKey').value,
  };

  const llmResult = await fetchJSON('/api/llm-config', { method: 'POST', body: JSON.stringify({ providers }) });
  await fetchJSON('/api/zotero-config', { method: 'POST', body: JSON.stringify({ zotero }) });
  document.getElementById('settingsResult').innerText = `已保存 ${llmResult.providers.length} 个 LLM 配置与 Zotero 配置`;
});

loadPapers();
loadLlmConfig();
loadZoteroConfig();
