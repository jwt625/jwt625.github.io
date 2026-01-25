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

    // Calculate time-proportional spacing
    calculateSpacing(project1, project2) {
        const date1 = new Date(project1.date);
        const date2 = new Date(project2.date);
        const monthsDiff = (date2.getFullYear() - date1.getFullYear()) * 12 +
                          (date2.getMonth() - date1.getMonth());

        // Spacing units based on time gaps
        if (monthsDiff <= 2) return 50;      // 0-2 months: unit 1
        if (monthsDiff <= 6) return 100;     // 3-6 months: unit 2
        if (monthsDiff <= 12) return 150;    // 7-12 months: unit 3
        return 200;                          // >1 year: unit 4
    }

    // Generate S-curve SVG path
    generateSCurve(isAbove) {
        const height = 40;
        const width = 20;

        if (isAbove) {
            // S-curve going up
            return `M 0,${height} C ${width/2},${height} ${width/2},0 ${width},0`;
        } else {
            // S-curve going down
            return `M 0,0 C ${width/2},0 ${width/2},${height} ${width},${height}`;
        }
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
                    ${visibleProjects.map((project, index) =>
                        this.renderProject(project, index, visibleProjects)).join('')}
                </div>
            </div>
        `;
    }

    renderProject(project, index, allProjects) {
        const categoryClass = `category-${project.category}`;
        const linksHtml = project.links.map(link =>
            `<a href="${link.url}" target="_blank" rel="noopener">${link.label}</a>`
        ).join(' | ');

        const imageHtml = project.image ?
            `<img src="${project.image}" alt="${project.name}" class="project-image" />` : '';

        // Calculate spacing from previous project
        const spacing = index > 0 ? this.calculateSpacing(allProjects[index - 1], project) : 0;
        const spacingStyle = this.currentView === 'horizontal'
            ? `margin-left: ${spacing}px;`
            : `margin-top: ${spacing}px;`;

        // Determine if this item is above or below (for horizontal)
        const isAbove = index % 2 === 0;

        // S-curve connector for horizontal layout
        const connectorHtml = this.currentView === 'horizontal'
            ? `<svg class="timeline-connector" width="20" height="40" viewBox="0 0 20 40">
                 <path d="${this.generateSCurve(isAbove)}"
                       stroke="#4a5f7a"
                       stroke-width="2"
                       fill="none"/>
               </svg>`
            : `<svg class="timeline-connector" width="30" height="2" viewBox="0 0 30 2">
                 <line x1="0" y1="1" x2="30" y2="1"
                       stroke="#4a5f7a"
                       stroke-width="2"/>
               </svg>`;

        return `
            <div class="timeline-item ${categoryClass}" data-index="${index}" style="${spacingStyle}">
                <div class="timeline-marker"></div>
                ${connectorHtml}
                <div class="timeline-content">
                    <div class="timeline-box">
                        <div class="timeline-date">${this.formatDate(project.date)}</div>
                        <div class="timeline-title">${project.name}</div>
                    </div>
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

