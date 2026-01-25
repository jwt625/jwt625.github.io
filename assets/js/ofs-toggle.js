// OFS Posts Toggle Widget with Proper Pagination
class OFSToggle {
    constructor() {
        this.storageKey = 'ofs_posts_visible';
        this.isVisible = this.loadState();
        this.allPostsData = null;
        this.nonOfsPostsData = null;
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    async init() {
        // Only run on homepage and paginated pages
        if (!this.isHomepage()) {
            console.log('OFS Toggle: Not on homepage, skipping');
            return;
        }

        console.log('OFS Toggle: Initializing on page', this.currentPage);

        // Create button first so user sees it
        this.createToggleButton();
        this.attachEventListeners();

        // Load pagination data
        await this.loadPaginationData();

        // If data loaded successfully, render the page
        if (this.allPostsData && this.nonOfsPostsData) {
            console.log('OFS Toggle: Data loaded, rendering page');
            this.renderCurrentPage();
        } else {
            console.log('OFS Toggle: Data not loaded, button will not function');
        }
    }

    isHomepage() {
        // Work on homepage and all paginated pages
        const path = window.location.pathname;
        return path === '/' || path === '/index.html' || /^\/page\d+\/?$/.test(path);
    }

    getCurrentPage() {
        const path = window.location.pathname;
        const match = path.match(/^\/page(\d+)\/?$/);
        return match ? parseInt(match[1]) : 1;
    }

    async loadPaginationData() {
        try {
            console.log('OFS Toggle: Loading pagination data...');
            const [allResponse, nonOfsResponse] = await Promise.all([
                fetch('/data/paginated-posts-all.json'),
                fetch('/data/paginated-posts-non-ofs.json')
            ]);

            if (!allResponse.ok || !nonOfsResponse.ok) {
                console.error('OFS Toggle: Failed to load pagination data', allResponse.status, nonOfsResponse.status);
                return;
            }

            this.allPostsData = await allResponse.json();
            this.nonOfsPostsData = await nonOfsResponse.json();
            console.log('OFS Toggle: Data loaded successfully', {
                allPosts: this.allPostsData.total_posts,
                nonOfsPosts: this.nonOfsPostsData.total_posts
            });
        } catch (error) {
            console.error('OFS Toggle: Error loading pagination data:', error);
        }
    }

    loadState() {
        const stored = localStorage.getItem(this.storageKey);
        // Default to hidden (false)
        return stored === null ? false : stored === 'true';
    }

    saveState() {
        localStorage.setItem(this.storageKey, this.isVisible.toString());
    }

    createToggleButton() {
        const button = document.createElement('div');
        button.id = 'ofs-toggle-button';
        button.className = 'ofs-toggle-button';
        button.innerHTML = this.isVisible ? 'Hide OFS Posts' : 'Show OFS Posts';
        button.title = 'Toggle Outside Five Sigma weekly posts';
        document.body.appendChild(button);
    }

    attachEventListeners() {
        const button = document.getElementById('ofs-toggle-button');
        if (button) {
            button.addEventListener('click', () => this.toggle());
        }
    }

    toggle() {
        this.isVisible = !this.isVisible;
        this.saveState();
        this.updateButtonText();
        this.renderCurrentPage();
    }

    updateButtonText() {
        const button = document.getElementById('ofs-toggle-button');
        if (button) {
            button.innerHTML = this.isVisible ? 'Hide OFS Posts' : 'Show OFS Posts';
        }
    }

    renderCurrentPage() {
        if (!this.allPostsData || !this.nonOfsPostsData) {
            console.error('OFS Toggle: Pagination data not loaded');
            return;
        }

        const data = this.isVisible ? this.allPostsData : this.nonOfsPostsData;
        const pageData = data.pages.find(p => p.page_num === this.currentPage);

        if (!pageData) {
            console.error('OFS Toggle: Page data not found for page', this.currentPage);
            return;
        }

        // Find the posts container - try multiple selectors
        let postsContainer = document.querySelector('.entries-list');
        if (!postsContainer) {
            postsContainer = document.querySelector('.list__items');
        }
        if (!postsContainer) {
            // Try to find the parent container that holds all list items
            const firstPost = document.querySelector('.list__item');
            if (firstPost && firstPost.parentElement) {
                postsContainer = firstPost.parentElement;
            }
        }

        if (!postsContainer) {
            console.error('OFS Toggle: Posts container not found');
            return;
        }

        console.log('OFS Toggle: Rendering', pageData.posts.length, 'posts');

        // Clear existing posts
        postsContainer.innerHTML = '';

        // Render posts
        pageData.posts.forEach(post => {
            const postElement = this.createPostElement(post);
            postsContainer.appendChild(postElement);
        });

        // Update pagination
        this.updatePagination(data);
    }

    createPostElement(post) {
        const div = document.createElement('div');
        div.className = 'list__item';

        const coverHtml = post.cover ? `
            <div class="post-cover">
                <img src="${post.cover}" alt="${post.title}">
            </div>
        ` : '';

        div.innerHTML = `
            <article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">
                <h2 class="archive__item-title no_toc" itemprop="headline">
                    <a href="${post.url}" rel="permalink">${post.title}</a>
                </h2>
                <p class="page__meta">
                    <span class="page__meta-date">
                        <i class="far fa-fw fa-calendar-alt" aria-hidden="true"></i>
                        <time datetime="${post.date}">${post.date}</time>
                    </span>
                </p>
                ${coverHtml}
                <p class="archive__item-excerpt" itemprop="description">${post.excerpt}</p>
            </article>
        `;

        return div;
    }

    updatePagination(data) {
        const paginationContainer = document.querySelector('.pagination');
        if (!paginationContainer) {
            return;
        }

        const totalPages = data.total_pages;
        let paginationHtml = '<ul>';

        // Previous link
        if (this.currentPage > 1) {
            const prevPage = this.currentPage === 2 ? '/' : `/page${this.currentPage - 1}/`;
            paginationHtml += `<li><a href="${prevPage}" class="pagination--pager">Previous</a></li>`;
        }

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            const pageUrl = i === 1 ? '/' : `/page${i}/`;
            const activeClass = i === this.currentPage ? ' current' : '';
            paginationHtml += `<li><a href="${pageUrl}" class="${activeClass}">${i}</a></li>`;
        }

        // Next link
        if (this.currentPage < totalPages) {
            const nextPage = `/page${this.currentPage + 1}/`;
            paginationHtml += `<li><a href="${nextPage}" class="pagination--pager">Next</a></li>`;
        }

        paginationHtml += '</ul>';
        paginationContainer.innerHTML = paginationHtml;
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    new OFSToggle();
});

