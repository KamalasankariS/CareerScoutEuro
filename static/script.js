/* ============================================
   CareerScoutEuro - Y2K Frontend Logic
   ============================================ */

// --- Tab Navigation ---
function switchTab(tabName) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.finder-nav button').forEach(b => b.classList.remove('active'));

  document.getElementById('tab-' + tabName).classList.add('active');
  event.target.classList.add('active');

  // Load data for the tab if not loaded
  loadTabData(tabName);
}

// --- Data Loading ---
const loadedTabs = new Set();

function loadTabData(tabName) {
  if (loadedTabs.has(tabName)) return;

  switch(tabName) {
    case 'currency': loadCurrency(); break;
    case 'jobs': loadJobs(); break;
    case 'github': loadGitHub(); break;
    case 'universities': loadUniversities(); break;
    case 'community': loadCommunity(); break;
    case 'tips': loadTips(); break;
  }
}

// --- Currency Tab ---
async function loadCurrency() {
  const container = document.getElementById('currency-data');
  container.innerHTML = '<div class="y2k-loader"><div class="spinner"></div><br>Loading currency data...</div>';

  try {
    const resp = await fetch('/api/currency');
    const data = await resp.json();
    loadedTabs.add('currency');

    let html = `
      <div class="guestbook-note">
        Base Rate: 1 USD = ${data.base_usd_to_inr} INR | Last updated: ${new Date(data.timestamp).toLocaleString()}
      </div>
      <div class="filter-bar">
        <label><input type="checkbox" id="filter-english" onchange="filterCurrencyTable()"> English-Friendly Only</label>
        <label>Sort by:
          <select id="sort-currency" onchange="filterCurrencyTable()">
            <option value="strength">Currency Strength</option>
            <option value="country">Country Name</option>
            <option value="inr">INR Value</option>
          </select>
        </label>
      </div>
      <div class="currency-table-wrapper">
        <table class="y2k-table" id="currency-table">
          <thead>
            <tr>
              <th>Country</th>
              <th>Capital</th>
              <th>Currency</th>
              <th>Code</th>
              <th>Language</th>
              <th>English?</th>
              <th>1 USD = INR</th>
              <th>1 Unit = INR</th>
              <th>Stronger?</th>
              <th>Ratio</th>
            </tr>
          </thead>
          <tbody id="currency-tbody">
    `;

    for (const c of data.countries) {
      const englishClass = c.english_friendly ? 'english-yes' : 'english-no';
      const strongerClass = c.stronger_currency === 'US Dollar' ? 'stronger-usd' : 'stronger-local';
      html += `
        <tr data-english="${c.english_friendly}" data-strength="${c.strength_ratio}" data-inr="${c.currency_to_inr}" data-country="${c.country}">
          <td><strong>${c.country}</strong></td>
          <td>${c.capital}</td>
          <td>${c.currency_name}</td>
          <td><span class="badge badge-swe">${c.currency_code}</span></td>
          <td>${c.language}</td>
          <td class="${englishClass}">${c.english_friendly ? 'Yes' : 'No'}</td>
          <td>${c.usd_to_inr}</td>
          <td>${c.currency_to_inr}</td>
          <td class="${strongerClass}">${c.stronger_currency}</td>
          <td>${c.strength_ratio}x</td>
        </tr>
      `;
    }

    html += '</tbody></table></div>';
    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error loading currency data: ${err.message}. Try the scrape button!</div>`;
  }
}

function filterCurrencyTable() {
  const englishOnly = document.getElementById('filter-english').checked;
  const sortBy = document.getElementById('sort-currency').value;
  const tbody = document.getElementById('currency-tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  rows.forEach(row => {
    if (englishOnly && row.dataset.english === 'false') {
      row.style.display = 'none';
    } else {
      row.style.display = '';
    }
  });

  // Sort
  rows.sort((a, b) => {
    switch(sortBy) {
      case 'strength': return parseFloat(b.dataset.strength) - parseFloat(a.dataset.strength);
      case 'country': return a.dataset.country.localeCompare(b.dataset.country);
      case 'inr': return parseFloat(b.dataset.inr) - parseFloat(a.dataset.inr);
      default: return 0;
    }
  });

  rows.forEach(row => tbody.appendChild(row));
}

// --- Jobs Tab ---
async function loadJobs() {
  const container = document.getElementById('jobs-data');
  container.innerHTML = '<div class="y2k-loader"><div class="spinner"></div><br>Loading job platforms...</div>';

  try {
    const resp = await fetch('/api/platforms');
    const platforms = await resp.json();
    loadedTabs.add('jobs');

    let html = `
      <div class="filter-bar">
        <label><input type="checkbox" id="filter-visa" onchange="filterJobs()"> Visa Sponsorship</label>
        <label><input type="checkbox" id="filter-jobs-english" onchange="filterJobs()"> English-Friendly</label>
        <label><input type="checkbox" id="filter-no-rec" onchange="filterJobs()"> No Recommendations</label>
        <label>Type:
          <select id="filter-job-type" onchange="filterJobs()">
            <option value="all">All Types</option>
            <option value="phd_research">PhD & Research</option>
            <option value="tech_jobs">Tech/SWE Jobs</option>
            <option value="ai_specific">AI/ML Specific</option>
            <option value="visa_resource">Visa Resources</option>
          </select>
        </label>
      </div>
      <div class="cards-grid" id="jobs-grid">
    `;

    for (const p of platforms) {
      const badges = [];
      if (p.type === 'phd_research') badges.push('<span class="badge badge-phd">PhD/Research</span>');
      if (p.type === 'tech_jobs') badges.push('<span class="badge badge-swe">Tech/SWE</span>');
      if (p.type === 'ai_specific') badges.push('<span class="badge badge-ai">AI/ML</span>');
      if (p.type === 'visa_resource') badges.push('<span class="badge badge-visa">Visa</span>');
      if (p.english_friendly === true) badges.push('<span class="badge badge-english">English OK</span>');
      if (p.recommendations_required === false || p.recommendations_required === 'sometimes')
        badges.push('<span class="badge badge-no-rec">No Recs</span>');
      if (p.visa_sponsorship === true) badges.push('<span class="badge badge-visa">Visa Sponsor</span>');

      html += `
        <div class="y2k-card" data-type="${p.type}" data-visa="${p.visa_sponsorship}" data-english="${p.english_friendly}" data-rec="${p.recommendations_required}">
          <div class="card-header">${p.name}</div>
          <div class="card-body">
            <p>${p.description}</p>
            <div style="margin-top: 10px">
              <a href="${p.url}" target="_blank" class="y2k-link">Browse Jobs</a>
              ${p.search_url !== p.url ? ` | <a href="${p.search_url}" target="_blank" class="y2k-link">AI/ML Search</a>` : ''}
            </div>
          </div>
          <div class="card-footer">${badges.join(' ')}</div>
        </div>
      `;
    }

    html += '</div>';
    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error loading jobs: ${err.message}</div>`;
  }
}

function filterJobs() {
  const visa = document.getElementById('filter-visa').checked;
  const english = document.getElementById('filter-jobs-english').checked;
  const noRec = document.getElementById('filter-no-rec').checked;
  const type = document.getElementById('filter-job-type').value;

  document.querySelectorAll('#jobs-grid .y2k-card').forEach(card => {
    let show = true;
    if (visa && card.dataset.visa !== 'true') show = false;
    if (english && card.dataset.english !== 'true') show = false;
    if (noRec && card.dataset.rec !== 'false') show = false;
    if (type !== 'all' && card.dataset.type !== type) show = false;
    card.style.display = show ? '' : 'none';
  });
}

// --- GitHub Tab ---
async function loadGitHub() {
  const container = document.getElementById('github-data');
  container.innerHTML = '<div class="y2k-loader"><div class="spinner"></div><br>Searching GitHub repos...</div>';

  try {
    const resp = await fetch('/api/github');
    const repos = await resp.json();
    loadedTabs.add('github');

    let html = '<div class="cards-grid">';
    for (const r of repos) {
      html += `
        <div class="y2k-card">
          <div class="card-header">
            <span class="badge badge-github">GitHub</span>
            ${r.name}
          </div>
          <div class="card-body">
            <p>${r.description || 'No description'}</p>
            <div style="margin-top: 8px">
              <a href="${r.url}" target="_blank" class="y2k-link">View Repository</a>
            </div>
          </div>
          <div class="card-footer">
            <span>${r.stars !== 'curated' ? r.stars + ' stars' : 'Curated Pick'}</span>
            <span>${r.language || ''}</span>
            <span>${r.source === 'curated_list' ? 'Curated' : 'Search: ' + r.query}</span>
          </div>
        </div>
      `;
    }
    html += '</div>';
    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error: ${err.message}. Click "Scrape Everything" to fetch data!</div>`;
  }
}

// --- Universities Tab ---
async function loadUniversities() {
  const container = document.getElementById('universities-data');
  container.innerHTML = '<div class="y2k-loader"><div class="spinner"></div><br>Loading university data...</div>';

  try {
    const resp = await fetch('/api/universities');
    const data = await resp.json();
    loadedTabs.add('universities');

    let html = '';

    // Professor outreach section
    html += '<div class="section-header">Professor Outreach Email Template</div>';
    html += `
      <div class="email-template" id="email-template">
        <button class="copy-btn" onclick="copyEmail()">Copy</button>
        ${escapeHtml(data.outreach.email_template)}
      </div>
    `;

    // Strategies
    html += '<div class="section-header">Strategies to Reach Professors & Get Positions</div>';
    html += '<div class="tips-box"><ul>';
    for (const tip of data.outreach.strategies) {
      html += `<li>${escapeHtml(tip)}</li>`;
    }
    html += '</ul></div>';

    // TA/RA strategies
    html += '<div class="section-header">TA/RA Position Strategies (Often No Recommendations!)</div>';
    html += '<div class="tips-box"><ul>';
    for (const tip of data.outreach.ta_ra_strategies) {
      html += `<li>${escapeHtml(tip)}</li>`;
    }
    html += '</ul></div>';

    // University list
    html += '<div class="section-header">Elite European CS/AI Universities & Research Labs</div>';
    html += '<div class="filter-bar"><label>Filter by country: <select id="filter-uni-country" onchange="filterUnis()"><option value="all">All Countries</option>';
    const countries = [...new Set(data.universities.map(u => u.country))].sort();
    for (const c of countries) {
      html += `<option value="${c}">${c}</option>`;
    }
    html += '</select></label></div>';

    html += '<div class="cards-grid" id="uni-grid">';
    for (const u of data.universities) {
      html += `
        <div class="y2k-card" data-country="${u.country}">
          <div class="card-header">${u.name}</div>
          <div class="card-body">
            <div class="uni-country">${u.country}</div>
            <div class="uni-links" style="margin-top: 10px">
              <a href="${u.url}" target="_blank" class="y2k-link">University</a>
              <a href="${u.cs_dept}" target="_blank" class="y2k-link">CS Department</a>
            </div>
          </div>
          <div class="card-footer">
            <span class="badge badge-phd">Research</span>
            <span class="badge badge-ai">AI/ML</span>
          </div>
        </div>
      `;
    }
    html += '</div>';

    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error: ${err.message}</div>`;
  }
}

function filterUnis() {
  const country = document.getElementById('filter-uni-country').value;
  document.querySelectorAll('#uni-grid .y2k-card').forEach(card => {
    card.style.display = (country === 'all' || card.dataset.country === country) ? '' : 'none';
  });
}

function copyEmail() {
  const el = document.getElementById('email-template');
  const text = el.innerText.replace('Copy', '').trim();
  navigator.clipboard.writeText(text).then(() => {
    const btn = el.querySelector('.copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}

// --- Community Tab ---
async function loadCommunity() {
  const container = document.getElementById('community-data');
  container.innerHTML = '<div class="y2k-loader"><div class="spinner"></div><br>Searching Reddit & HackerNews...</div>';

  try {
    const resp = await fetch('/api/community');
    const data = await resp.json();
    loadedTabs.add('community');

    let html = '';

    // Subreddits
    html += '<div class="section-header">Useful Subreddits for European Job Hunting</div>';
    html += '<div class="cards-grid">';
    for (const sub of data.subreddits) {
      html += `
        <div class="y2k-card">
          <div class="card-header"><span class="badge badge-reddit">Reddit</span> ${sub.subreddit}</div>
          <div class="card-body">
            <p>${sub.description}</p>
            <a href="${sub.url}" target="_blank" class="y2k-link">Visit Subreddit</a>
          </div>
        </div>
      `;
    }
    html += '</div>';

    // Curated posts
    html += '<div class="section-header">Curated Search Threads</div>';
    html += '<div class="cards-grid">';
    for (const post of data.curated_posts) {
      html += `
        <div class="y2k-card">
          <div class="card-header"><span class="badge badge-reddit">${post.subreddit}</span></div>
          <div class="card-body">
            <p><strong>${post.title}</strong></p>
            <a href="${post.url}" target="_blank" class="y2k-link">Search Results</a>
          </div>
          <div class="card-footer"><span class="badge badge-${post.category === 'visa_guide' ? 'visa' : 'phd'}">${post.category.replace('_', ' ')}</span></div>
        </div>
      `;
    }
    html += '</div>';

    // Reddit search results
    if (data.reddit_results && data.reddit_results.length > 0) {
      html += '<div class="section-header">Live Reddit Search Results</div>';
      html += '<div class="cards-grid">';
      for (const post of data.reddit_results) {
        html += `
          <div class="y2k-card">
            <div class="card-header"><span class="badge badge-reddit">${post.subreddit}</span></div>
            <div class="card-body">
              <p><strong>${escapeHtml(post.title)}</strong></p>
              ${post.selftext_preview ? `<p style="font-size:12px;color:#666;margin-top:6px">${escapeHtml(post.selftext_preview)}...</p>` : ''}
              <a href="${post.url}" target="_blank" class="y2k-link">Read Post</a>
            </div>
            <div class="card-footer">
              <span>${post.score} points</span>
              <span>${post.num_comments} comments</span>
            </div>
          </div>
        `;
      }
      html += '</div>';
    }

    // HackerNews results
    if (data.hackernews_results && data.hackernews_results.length > 0) {
      html += '<div class="section-header">HackerNews Results</div>';
      html += '<div class="cards-grid">';
      for (const post of data.hackernews_results) {
        html += `
          <div class="y2k-card">
            <div class="card-header"><span class="badge badge-hn">HN</span> ${escapeHtml(post.title)}</div>
            <div class="card-body">
              <a href="${post.url}" target="_blank" class="y2k-link">Read Article</a>
            </div>
            <div class="card-footer">
              <span>${post.points} points</span>
              <span>${post.num_comments} comments</span>
            </div>
          </div>
        `;
      }
      html += '</div>';
    }

    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error: ${err.message}. Try "Scrape Everything" first!</div>`;
  }
}

// --- Tips Tab ---
async function loadTips() {
  const container = document.getElementById('tips-data');

  try {
    const resp = await fetch('/api/language-tips');
    const data = await resp.json();
    loadedTabs.add('tips');

    let html = '';

    html += '<div class="section-header">No French Required! English-Friendly Countries</div>';
    html += '<div class="tips-box"><ul>';
    for (const tip of data.no_french_tips) {
      html += `<li>${escapeHtml(tip)}</li>`;
    }
    html += '</ul></div>';

    html += '<div class="section-header">Positions Without Recommendation Letters</div>';
    html += '<div class="tips-box"><ul>';
    for (const tip of data.no_recommendation_tips) {
      html += `<li>${escapeHtml(tip)}</li>`;
    }
    html += '</ul></div>';

    html += `
      <div class="section-header">Your Profile Summary</div>
      <div class="tips-box">
        <h3>What We're Working With:</h3>
        <ul>
          <li><strong>Background:</strong> Indian students studying in the US</li>
          <li><strong>Target Start Date:</strong> June 2026</li>
          <li><strong>Fields:</strong> AI/ML (NLP, CV, Deep Learning), SWE/SDE, Full-stack</li>
          <li><strong>Position Types:</strong> PhD, Research Assistant, TA, Full-time roles</li>
          <li><strong>Languages:</strong> English (fluent), French (basic - no B2 cert)</li>
          <li><strong>Preference:</strong> Positions without recommendation letters (but open to all)</li>
          <li><strong>Visa:</strong> Will need work visa / student visa sponsorship</li>
        </ul>
      </div>

      <div class="section-header">Pro Tips for Indian Students</div>
      <div class="tips-box">
        <ul>
          <li><strong>EU Blue Card:</strong> The best work visa option for skilled tech workers. Most EU countries offer it. Salary threshold varies by country.</li>
          <li><strong>Germany:</strong> No tuition fees for PhDs! Many programs are fully funded + salary. Berlin tech scene is 90% English.</li>
          <li><strong>Netherlands:</strong> "Kennismigrant" (knowledge migrant) visa is fast and easy for tech workers. Amsterdam is incredibly international.</li>
          <li><strong>UK:</strong> Global Talent Visa for AI/ML researchers. Post-study work visa if you do a UK degree first.</li>
          <li><strong>Switzerland:</strong> Highest salaries in Europe. ETH Zurich and EPFL are world-class. English widely spoken in tech.</li>
          <li><strong>Nordics:</strong> Sweden, Denmark, Finland, Norway all have English-friendly tech scenes and great quality of life.</li>
          <li><strong>France:</strong> INRIA is amazing for AI research. Many labs work in English despite being in France. "Passeport Talent" visa for researchers.</li>
          <li><strong>Timing:</strong> Apply 6-12 months before your desired start date. For June 2026, start applying NOW!</li>
          <li><strong>Networking:</strong> Attend European AI conferences (NeurIPS has European workshops, ECML-PKDD, ECAI). Many professors recruit at conferences.</li>
          <li><strong>LinkedIn:</strong> Connect with Indian alumni who moved to Europe - they're usually happy to help!</li>
        </ul>
      </div>
    `;

    container.innerHTML = html;

  } catch (err) {
    container.innerHTML = `<div class="guestbook-note">Error: ${err.message}</div>`;
  }
}

// --- Scrape All Button ---
async function scrapeEverything() {
  const btn = document.getElementById('scrape-btn');
  const status = document.getElementById('scrape-status');
  btn.classList.add('loading');
  btn.textContent = 'SCRAPING...';
  btn.disabled = true;

  try {
    await fetch('/api/scrape-all', { method: 'POST' });

    // Poll for status
    const pollInterval = setInterval(async () => {
      const resp = await fetch('/api/scrape-status');
      const data = await resp.json();
      status.textContent = data.progress;

      if (data.status === 'done' || data.status === 'error') {
        clearInterval(pollInterval);
        btn.classList.remove('loading');
        btn.textContent = data.status === 'done' ? 'SCRAPE COMPLETE!' : 'ERROR - TRY AGAIN';
        btn.disabled = false;
        loadedTabs.clear();

        if (data.status === 'done') {
          // Reload current active tab
          const activeTab = document.querySelector('.finder-nav button.active');
          if (activeTab) {
            const tabName = activeTab.textContent.toLowerCase().replace(/[^a-z]/g, '');
            const tabMap = {
              'currency': 'currency', 'jobboards': 'jobs', 'github': 'github',
              'universities': 'universities', 'community': 'community', 'tips': 'tips'
            };
            if (tabMap[tabName]) loadTabData(tabMap[tabName]);
          }
        }
      }
    }, 1500);

  } catch (err) {
    status.textContent = `Error: ${err.message}`;
    btn.classList.remove('loading');
    btn.textContent = 'SCRAPE EVERYTHING';
    btn.disabled = false;
  }
}

// --- Utility ---
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// --- Visitor Counter (fun Y2K touch) ---
function updateVisitorCounter() {
  let count = parseInt(localStorage.getItem('careerscout_visits') || '0');
  count++;
  localStorage.setItem('careerscout_visits', count.toString());
  const el = document.getElementById('visitor-count');
  if (el) el.textContent = String(count).padStart(6, '0');
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
  updateVisitorCounter();
  // Auto-load currency tab (default)
  loadCurrency();
});
