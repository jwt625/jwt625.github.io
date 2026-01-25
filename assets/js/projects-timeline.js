// Projects Timeline Component
class ProjectsTimeline {
    constructor(containerId, projects) {
        this.container = document.getElementById(containerId);
        this.projects = projects.sort((a, b) => new Date(a.date) - new Date(b.date));
        this.currentView = 'horizontal';
        this.viewMonths = 6; // Default to last 6 months
        this.init();
    }

    init() {
        if (!this.container) return;
        
        this.checkResponsive();
        this.render();
        this.attachEventListeners();
        
        window.addEventListener('resize', () => {
            this.checkResponsive();
            this.render();
        });
    }

    checkResponsive() {
        this.currentView = window.innerWidth <= 768 ? 'vertical' : 'horizontal';
    }

    getVisibleProjects() {
        const now = new Date();
        const cutoffDate = new Date(now.getFullYear(), now.getMonth() - this.viewMonths, 1);
        return this.projects.filter(p => new Date(p.date) >= cutoffDate);
    }

    formatDate(dateStr) {
        const date = new Date(dateStr);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        return `${year}-${month}`;
    }

    render() {
        const visibleProjects = this.viewMonths === Infinity ? this.projects : this.getVisibleProjects();
        
        this.container.innerHTML = `
            <div class="timeline-controls">
                <button id="timeline-zoom-out" class="timeline-btn">Show All</button>
                <button id="timeline-zoom-in" class="timeline-btn">Last 6 Months</button>
                <button id="timeline-scroll-start" class="timeline-btn">← First Project</button>
            </div>
            <div class="timeline-wrapper ${this.currentView}">
                <div class="timeline-track">
                    ${visibleProjects.map((project, index) => this.renderProject(project, index)).join('')}
                </div>
            </div>
        `;
    }

    renderProject(project, index) {
        const categoryClass = `category-${project.category}`;
        const linksHtml = project.links.map(link => 
            `<a href="${link.url}" target="_blank" rel="noopener">${link.label}</a>`
        ).join(' | ');
        
        const imageHtml = project.image ? 
            `<img src="${project.image}" alt="${project.name}" class="project-image" />` : '';

        return `
            <div class="timeline-item ${categoryClass}" data-index="${index}">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="timeline-date">${this.formatDate(project.date)}</div>
                    <div class="timeline-title">${project.name}</div>
                    <div class="timeline-detail">
                        ${imageHtml}
                        <p class="timeline-description">${project.description}</p>
                        ${linksHtml ? `<div class="timeline-links">${linksHtml}</div>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const zoomOut = document.getElementById('timeline-zoom-out');
        const zoomIn = document.getElementById('timeline-zoom-in');
        const scrollStart = document.getElementById('timeline-scroll-start');

        if (zoomOut) {
            zoomOut.addEventListener('click', () => {
                this.viewMonths = Infinity;
                this.render();
                this.attachEventListeners();
            });
        }

        if (zoomIn) {
            zoomIn.addEventListener('click', () => {
                this.viewMonths = 6;
                this.render();
                this.attachEventListeners();
            });
        }

        if (scrollStart) {
            scrollStart.addEventListener('click', () => {
                const firstItem = this.container.querySelector('.timeline-item');
                if (firstItem) {
                    firstItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        }

        // Add hover effects for detail cards
        const items = this.container.querySelectorAll('.timeline-item');
        items.forEach(item => {
            item.addEventListener('mouseenter', () => {
                item.classList.add('active');
            });
            item.addEventListener('mouseleave', () => {
                item.classList.remove('active');
            });
        });
    }
}

// Initialize timeline when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch projects data from Jekyll data file
        const response = await fetch('/data/projects.json');
        if (!response.ok) {
            console.error('Failed to load projects data');
            return;
        }
        const projects = await response.json();
        new ProjectsTimeline('projects-timeline', projects);
    } catch (error) {
        console.error('Error initializing timeline:', error);
    }
});

