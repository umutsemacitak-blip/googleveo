document.addEventListener('DOMContentLoaded', () => {
    console.log("Veo Academy Script Loaded (SEO Optimized Pagination Mode)");

    // --- DOM Elements ---
    const promptGrid = document.getElementById('promptGrid');
    const searchInput = document.getElementById('searchInput');
    const noResults = document.getElementById('noResults');
    const categoryNav = document.getElementById('categoryNav');

    // --- State ---
    let allPrompts = [];
    let currentFilteredPrompts = [];
    const ITEMS_PER_PAGE = 30; // 30 items per page

    // Get params from URL
    const urlParams = new URLSearchParams(window.location.search);
    let currentCategory = urlParams.get('category') || 'All';
    let currentPage = parseInt(urlParams.get('page') || '1', 10);
    if (isNaN(currentPage) || currentPage < 1) currentPage = 1;

    // --- Sidebar Logic ---
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    window.toggleSidebar = () => {
        if (sidebar && overlay) {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        }
    };

    const mobileBtn = document.getElementById('mobileMenuBtn');
    if (mobileBtn) mobileBtn.addEventListener('click', window.toggleSidebar);

    // --- Init ---
    function init() {
        if (typeof promptData !== 'undefined') {
            try {
                // Flatten Data
                const categories = Object.keys(promptData);
                categories.forEach(cat => {
                    const items = promptData[cat];
                    if (Array.isArray(items)) {
                        items.forEach(text => {
                            if (typeof text === 'string') {
                                allPrompts.push({ category: cat, text: text.trim() });
                            }
                        });
                    }
                });

                // Apply Initial Filter based on URL
                applyFilterAndRender();

                // Search Listener
                if (searchInput) {
                    searchInput.addEventListener('input', (e) => {
                        const term = e.target.value.toLowerCase();
                        if (!term) {
                            // Reset to category state
                            filterByCategory(currentCategory);
                        } else {
                            // Client-side search overrides URL page/category temporarily
                            currentFilteredPrompts = allPrompts.filter(p =>
                                p.text.toLowerCase().includes(term) ||
                                p.category.toLowerCase().includes(term)
                            );
                            currentPage = 1; // Reset to page 1 for search results
                        }
                        renderGrid();
                    });
                }

                // Render Sidebar (Categories)
                renderNavigation();

            } catch (e) {
                console.error("Init Error:", e);
            }
        }
    }

    function filterByCategory(cat) {
        if (cat === 'All') {
            currentFilteredPrompts = allPrompts;
        } else {
            currentFilteredPrompts = allPrompts.filter(p => p.category === cat);
        }
    }

    function applyFilterAndRender() {
        filterByCategory(currentCategory);
        renderGrid();
    }

    // --- Navigation (Sidebar) ---
    function renderNavigation() {
        if (!categoryNav) return;

        const categories = ['All', ...Object.keys(promptData)];

        categoryNav.innerHTML = categories.map(c => {
            const isActive = c === currentCategory ? 'active' : '';
            // SEO-FRIENDLY: Using proper <a> tags for direct crawling.
            // URL search params handle the state.
            const url = new URL(window.location);
            url.searchParams.set('category', c);
            url.searchParams.set('page', '1');

            return `
            <a href="${url.toString()}" class="category-btn ${isActive}">
                <i class="ph ph-folder${c === 'All' ? '-open' : ''}"></i>
                <span>${c === 'All' ? 'All Prompts' : c}</span>
            </a>
            `;
        }).join('');
    }

    window.navigateToCategory = (cat) => {
        // Full page reload/navigation to update URL params
        // This ensures the URL is shareable and indexable
        const url = new URL(window.location);
        url.searchParams.set('category', cat);
        url.searchParams.set('page', '1'); // Always reset to page 1
        window.location.href = url.toString();
    };

    // --- Grid Rendering with Pagination ---
    function renderGrid() {
        if (!promptGrid) return;

        promptGrid.innerHTML = '';

        if (currentFilteredPrompts.length === 0) {
            if (noResults) noResults.style.display = 'block';

            // Remove old pagination if exists
            const existingPag = document.querySelector('.pagination-container');
            if (existingPag) existingPag.remove();

            return;
        } else {
            if (noResults) noResults.style.display = 'none';
        }

        // Calculate Slice
        const totalItems = currentFilteredPrompts.length;
        const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);

        // Ensure currentPage is valid
        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const startIdx = (currentPage - 1) * ITEMS_PER_PAGE;
        const endIdx = Math.min(startIdx + ITEMS_PER_PAGE, totalItems);

        const pageItems = currentFilteredPrompts.slice(startIdx, endIdx);

        // Render Cards
        const html = pageItems.map(p => `
            <div class="prompt-card">
                <div class="card-header">
                    <span class="badge">${p.category}</span>
                    <i class="ph ph-hash" style="color:var(--primary-light)"></i>
                </div>
                <div class="prompt-text">${escapeHtml(p.text)}</div>
                <div class="card-actions">
                    <button class="btn-copy" onclick="copyText(this, '${escapeHtml(p.text)}')">
                        <i class="ph-bold ph-copy"></i> Copy Prompt
                    </button>
                </div>
            </div>
        `).join('');

        promptGrid.innerHTML = html;

        // Render Pagination Controls
        renderPaginationControls(totalPages);
    }

    function renderPaginationControls(totalPages) {
        // Remove old pagination
        const existingPag = document.querySelector('.pagination-container');
        if (existingPag) existingPag.remove();

        if (totalPages <= 1) return;

        const paginationContainer = document.createElement('div');
        paginationContainer.className = 'pagination-container';

        // Helper to generate URL
        const getUrl = (p) => {
            const url = new URL(window.location);
            url.searchParams.set('category', currentCategory);
            url.searchParams.set('page', p);
            return url.toString();
        };

        let paginationHTML = '';

        // Previous
        if (currentPage > 1) {
            paginationHTML += `<a href="${getUrl(currentPage - 1)}" class="page-link"><i class="ph ph-caret-left"></i></a>`;
        }

        // Logic for "Smart" Pagination (1, 2 ... 5 6 7 ... 99)
        const range = 2; // Neighbors

        for (let i = 1; i <= totalPages; i++) {
            // Show first, last, current, and neighbors
            if (i === 1 || i === totalPages || (i >= currentPage - range && i <= currentPage + range)) {
                paginationHTML += `<a href="${getUrl(i)}" class="page-link ${i === currentPage ? 'active' : ''}">${i}</a>`;
            } else if (i === currentPage - range - 1 || i === currentPage + range + 1) {
                paginationHTML += `<span class="page-link dots">...</span>`;
            }
        }

        // Next
        if (currentPage < totalPages) {
            paginationHTML += `<a href="${getUrl(currentPage + 1)}" class="page-link"><i class="ph ph-caret-right"></i></a>`;
        }

        paginationContainer.innerHTML = paginationHTML;

        // Append after grid
        promptGrid.parentNode.insertBefore(paginationContainer, promptGrid.nextSibling);
    }

    // --- Utilities ---
    window.copyText = (btn, text) => {
        navigator.clipboard.writeText(text).then(() => {
            const originalContent = btn.innerHTML;
            btn.innerHTML = '<i class="ph-bold ph-check" style="color:var(--accent-primary)"></i> Copied';
            btn.style.borderColor = 'var(--accent-primary)';

            setTimeout(() => {
                btn.innerHTML = originalContent;
                btn.style.borderColor = '';
            }, 2000);
        });
    };

    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // --- ANTIGRAVITY PARALLAX ENGINE (Disabled - causes CLS) ---
    // Parallax animations cause layout shift = bad performance
    /*
    const parallaxElements = document.querySelectorAll('[data-parallax-speed]');
    const isMobile = window.innerWidth < 900;

    if (parallaxElements.length > 0 && !isMobile) {
        let ticking = false;

        function updateParallax() {
            const scrollY = window.scrollY;

            parallaxElements.forEach(el => {
                const speed = parseFloat(el.getAttribute('data-parallax-speed') || 0);
                const offset = scrollY * speed;
                el.style.transform = `translate3d(0, ${offset}px, 0)`;
            });

            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });
    }
    */

    // Start
    init();
});