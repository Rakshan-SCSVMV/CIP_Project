document.addEventListener('DOMContentLoaded', () => {
    // Current active records set for exporting
    let currentRenderedRecords = [];

    const searchForm = document.getElementById('search-form');
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('results-section');
    const noResultsSection = document.getElementById('no-results');
    const resultCount = document.getElementById('result-count');
    
    // Desktop vs Mobile containers
    const tableBody = document.getElementById('table-body');
    const mobileCards = document.getElementById('mobile-cards');

    // Dashboard Overview
    const dashboardStats = document.getElementById('dashboard-stats');
    const statTotal = document.getElementById('stat-total');
    const statCleared = document.getElementById('stat-cleared');
    const statLitigation = document.getElementById('stat-litigation');
    
    // Chart Elements
    const pbGreen = document.getElementById('pb-green');
    const pbYellow = document.getElementById('pb-yellow');
    const pbRed = document.getElementById('pb-red');

    // Hierarchy Selectors
    const stateSelect = document.getElementById('state');
    const districtSelect = document.getElementById('district');
    const villageSelect = document.getElementById('village');
    const sectorInput = document.getElementById('sector');

    // Modals
    const dossierModal = document.getElementById('dossier-modal');
    const dossierContent = document.getElementById('dossier-content');
    const adminModal = document.getElementById('admin-modal');

    // Data Load
    const hierarchy = window.landData.hierarchy;
    const masterDb = window.landData.records;

    // --- DARK MODE LOGIC ---
    const darkToggleBtn = document.getElementById('dark-mode-toggle');
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }
    darkToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    });

    // --- POPULATE CASCADING DROPDOWNS ---
    for(let s in hierarchy) {
        let opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        stateSelect.appendChild(opt);
    }

    stateSelect.addEventListener('change', () => {
        districtSelect.innerHTML = '<option value="">Select District</option>';
        villageSelect.innerHTML = '<option value="">Select Village</option>';
        villageSelect.disabled = true;

        if (stateSelect.value) {
            districtSelect.disabled = false;
            for(let d in hierarchy[stateSelect.value]) {
                let opt = document.createElement('option');
                opt.value = d;
                opt.textContent = d;
                districtSelect.appendChild(opt);
            }
        } else {
            districtSelect.disabled = true;
        }
    });

    districtSelect.addEventListener('change', () => {
        villageSelect.innerHTML = '<option value="">Select Village</option>';

        if (districtSelect.value && stateSelect.value) {
            villageSelect.disabled = false;
            let villages = hierarchy[stateSelect.value][districtSelect.value];
            villages.forEach(v => {
                let opt = document.createElement('option');
                opt.value = v;
                opt.textContent = v;
                villageSelect.appendChild(opt);
            });
        } else {
            villageSelect.disabled = true;
        }
    });

    // --- HELPERS ---
    function getStatusDetails(originalStatus) {
        if (originalStatus === 'Clear' || originalStatus === 'No Litigation') {
            return { text: 'No Litigation', colorClass: 'status-green' };
        } else if (originalStatus === 'Under Court Stay') {
            return { text: 'Pending Case', colorClass: 'status-yellow' };
        } else {
            return { text: 'Under Litigation', colorClass: 'status-red' };
        }
    }

    function updateDashboardStats(dataArray) {
        let total = dataArray.length;
        let clearCount = 0;
        let litCount = 0;
        let pendingCount = 0;
        
        dataArray.forEach(item => {
            const status = getStatusDetails(item.litigationStatus).text;
            if (status === 'No Litigation') clearCount++;
            else if (status === 'Pending Case') pendingCount++;
            else litCount++;
        });

        statTotal.textContent = total;
        statCleared.textContent = clearCount;
        statLitigation.textContent = litCount + pendingCount;
        
        // Advanced Visual Chart Updates
        pbGreen.style.width = `${(clearCount / total) * 100}%`;
        pbYellow.style.width = `${(pendingCount / total) * 100}%`;
        pbRed.style.width = `${(litCount / total) * 100}%`;
        
        dashboardStats.classList.remove('hidden');
    }

    // --- DOSSIER RENDERING ---
    function showDossier(recordIndex) {
        const record = currentRenderedRecords[recordIndex];
        const statusInfo = getStatusDetails(record.litigationStatus);
        
        let dossierHtml = '';
        if (statusInfo.text !== 'No Litigation') {
             dossierHtml += `
                <div class="dossier-warning">
                    ⚠️ ALERT: This property is actively under dispute constraints. Transactions without judicial clearance are void.
                </div>
             `;
        }
        
        dossierHtml += `
            <div class="dossier-grid">
                <div class="dossal-box">
                    <span class="db-label">Registered Owner</span>
                    <span class="db-val">${record.ownerName}</span>
                </div>
                <div class="dossal-box">
                    <span class="db-label">Location</span>
                    <span class="db-val" style="font-size:0.9rem;">Village: ${record.villageName}, Sector ${record.sectorNumber} / Plot ${record.plotNumber}</span>
                </div>
                <div class="dossal-box">
                    <span class="db-label">Last Survey & Type</span>
                    <span class="db-val">${record.surveyYear} - ${record.landType}</span>
                </div>
                <div class="dossal-box">
                    <span class="db-label">Property Valuation (Approx)</span>
                    <span class="db-val">${record.propertyValuation}</span>
                </div>
            </div>
        `;
        
        if (statusInfo.text !== 'No Litigation') {
            dossierHtml += `
                <h3 style="margin:20px 0 10px; font-size:1.1rem; color:var(--text-main);">Litigation & Legal Context</h3>
                <div class="dossier-grid">
                    <div class="dossal-box">
                        <span class="db-label">Case No. & Court</span>
                        <span class="db-val" style="color:var(--status-red);">${record.caseNumber} - ${record.courtName}</span>
                    </div>
                    <div class="dossal-box">
                        <span class="db-label">Legal Context</span>
                        <span class="db-val">${record.caseSummary}</span>
                    </div>
                    <div class="dossal-box">
                        <span class="db-label">Previous Hearing</span>
                        <span class="db-val">${record.previousHearing}</span>
                    </div>
                    <div class="dossal-box">
                        <span class="db-label">Next Scheduled Hearing</span>
                        <span class="db-val">${record.nextHearing}</span>
                    </div>
                </div>
            `;
        }

        dossierContent.innerHTML = dossierHtml;
        dossierModal.classList.remove('hidden');
    }

    // --- FORM SEARCH & RENDERING ---
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const selState = stateSelect.value;
        const selDist = districtSelect.value;
        const selVill = villageSelect.value;
        const selSector = sectorInput.value.trim();

        const filterType = document.getElementById('filter-type').value;
        const filterStatus = document.getElementById('filter-status').value;

        // Reset UI
        resultsSection.classList.add('hidden');
        noResultsSection.classList.add('hidden');
        dashboardStats.classList.add('hidden');
        tableBody.innerHTML = '';
        mobileCards.innerHTML = '';
        currentRenderedRecords = [];
        loader.classList.remove('hidden');

        let params = new URLSearchParams({
            state: selState,
            district: selDist,
            villageName: selVill,
            sectorNumber: selSector
        });

        fetch(`/api/records?${params.toString()}`)
            .then(res => res.json())
            .then(data => {
                loader.classList.add('hidden');
                if (data.success && data.data.length > 0) {
                    let finalHits = data.data.filter(item => {
                        let passType = (filterType === 'All') || (item.landType.includes(filterType) || (filterType === 'Public' && item.landType === 'Public Infrastructure'));
                        let currentStatusMap = getStatusDetails(item.litigationStatus).text;
                        let passStatus = (filterStatus === 'All') || (currentStatusMap === filterStatus);
                        return passType && passStatus;
                    });
                    if (finalHits.length > 0) {
                        currentRenderedRecords = finalHits; // Save global state for export and modals
                        updateDashboardStats(finalHits);
                        renderResults(finalHits);
                    } else {
                        noResultsSection.classList.remove('hidden');
                    }
                } else {
                    noResultsSection.classList.remove('hidden');
                }
            })
            .catch(err => {
                console.error("Fetch Error:", err);
                loader.classList.add('hidden');
                noResultsSection.classList.remove('hidden');
            });
    });

    function renderResults(records) {
        resultCount.textContent = `${records.length} Found`;
        
        records.forEach((record, index) => {
            const statusInfo = getStatusDetails(record.litigationStatus);
            
            let caseStr = record.caseNumber;
            let courtStr = record.courtName;
            if (statusInfo.text === 'No Litigation') {
                caseStr = '-';
                courtStr = '-';
            }

            // Desktop Row
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <span class="bold-td">Plot: ${record.plotNumber}</span>
                    <span class="small-td">${record.landArea}</span>
                </td>
                <td class="bold-td">${record.ownerName}</td>
                <td>${record.landType}</td>
                <td><span class="status-pill ${statusInfo.colorClass}">${statusInfo.text}</span></td>
                <td>
                    <span class="bold-td">${caseStr}</span>
                    <span class="small-td">${courtStr}</span>
                </td>
                <td><button class="action-btn dossier-trigger" data-idx="${index}">View Details</button></td>
            `;
            tableBody.appendChild(tr);

            // Mobile Card
            const mCard = document.createElement('div');
            mCard.className = 'mobile-card';
            mCard.innerHTML = `
                <div class="m-card-header">
                    <span class="bold-td">Plot: ${record.plotNumber}</span>
                    <span class="status-pill ${statusInfo.colorClass}">${statusInfo.text}</span>
                </div>
                <div class="m-card-row">
                    <span class="m-card-label">Owner</span><span class="m-card-val">${record.ownerName}</span>
                </div>
                <div class="m-card-row">
                    <span class="m-card-label">Area / Type</span><span class="m-card-val">${record.landArea} | ${record.landType}</span>
                </div>
                <div class="m-card-row">
                    <span class="m-card-label">Case No</span><span class="m-card-val">${caseStr}</span>
                </div>
                <div style="margin-top: 12px; text-align: center;">
                    <button class="action-btn dossier-trigger" data-idx="${index}" style="width: 100%;">View Details</button>
                </div>
            `;
            mobileCards.appendChild(mCard);
        });

        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // --- GLOBAL EVENT LISTENERS ---

    // Export CSV Feature
    document.getElementById('btn-export-csv').addEventListener('click', () => {
        if (currentRenderedRecords.length === 0) return;
        
        const headers = ['State', 'District', 'Village', 'Sector', 'Plot', 'Owner', 'Area', 'Type', 'Status', 'CaseNo', 'Court'];
        const rows = currentRenderedRecords.map(r => 
            `"${r.state}","${r.district}","${r.villageName}","${r.sectorNumber}","${r.plotNumber}","${r.ownerName}","${r.landArea}","${r.landType}","${r.litigationStatus}","${r.caseNumber}","${r.courtName}"`
        );
        
        const csvContent = "data:text/csv;charset=utf-8," + headers.join(',') + "\n" + rows.join("\n");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `land_records_export_${new Date().getTime()}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Print Feature
    document.getElementById('btn-print').addEventListener('click', () => {
        window.print();
    });

    // Official Login Button
    const adminLoginBtn = document.getElementById('admin-login-btn');
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            adminModal.classList.remove('hidden');
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const adminId = document.getElementById('admin-id').value;
            const password = document.getElementById('admin-pass').value;

            fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ adminId, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    localStorage.setItem('adminToken', data.token);
                    alert("Authentication successful. Redirecting to Secure Official Dash...");
                    window.location.href = '/admin.html';
                } else {
                    alert('Invalid credentials. Access denied.');
                }
            })
            .catch(err => alert('Authentication Server unreachable.'));
        });
    }

    // Language Toggle
    const langToggle = document.querySelector('.lang-toggle');
    if (langToggle) {
        langToggle.addEventListener('click', () => {
            alert('Regional language support is currently unavailable in the demo environment. English is set as default.');
        });
    }

    // Modal Close logic
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.modal').classList.add('hidden');
        });
    });

    document.body.addEventListener('click', (e) => {
        if (e.target.classList.contains('dossier-trigger')) {
            showDossier(parseInt(e.target.getAttribute('data-idx')));
        } else if (e.target.classList.contains('modal')) {
            e.target.classList.add('hidden');
        }
    });

    const navLinks = document.querySelectorAll('.header-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const text = e.target.textContent;
            if (text === 'Home') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
                resultsSection.classList.add('hidden');
                noResultsSection.classList.add('hidden');
                dashboardStats.classList.add('hidden');
                searchForm.reset();
                districtSelect.innerHTML = '<option value="">Select District</option>';
                districtSelect.disabled = true;
                villageSelect.innerHTML = '<option value="">Select Village</option>';
                villageSelect.disabled = true;
            } else if (text === 'Help / Support') {
                e.preventDefault();
                alert("For support, contact admin@landrecords.gov.in or call 1800-11-2026.");
            } else if (text === 'Case Status') {
                e.preventDefault();
                alert("Redirection to external e-Courts portal is disabled in demo mode.");
            }
        });
    });
});
