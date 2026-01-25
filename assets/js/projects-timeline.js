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

        this.createModal();
        this.checkResponsive();
        this.render();
        this.attachEventListeners();

        window.addEventListener('resize', () => {
            this.checkResponsive();
            this.render();
            this.attachEventListeners();
        });
    }

    createModal() {
        // Create modal for project details
        const modal = document.createElement('div');
        modal.id = 'project-detail-modal';
        modal.className = 'project-detail-modal hidden';
        modal.innerHTML = `
            <div class="project-detail-content">
                <div class="project-detail-header">
                    <h3 id="project-modal-title"></h3>
                    <button class="project-detail-close">&times;</button>
                </div>
                <div class="project-detail-body">
                    <div id="project-modal-image"></div>
                    <p id="project-modal-description"></p>
                    <div id="project-modal-links"></div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Close modal handlers
        modal.querySelector('.project-detail-close').addEventListener('click', () => {
            this.closeModal();
        });

        modal.addEventListener('click', (e) => {
            if (e.target.id === 'project-detail-modal') {
                this.closeModal();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
                this.closeModal();
            }
        });
    }

    openModal(project) {
        const modal = document.getElementById('project-detail-modal');
        document.getElementById('project-modal-title').textContent = project.name;
        document.getElementById('project-modal-description').textContent = project.description;

        const imageContainer = document.getElementById('project-modal-image');
        if (project.image) {
            imageContainer.innerHTML = `<img src="${project.image}" alt="${project.name}" class="project-modal-image" />`;
        } else {
            imageContainer.innerHTML = '';
        }

        const linksContainer = document.getElementById('project-modal-links');
        if (project.links && project.links.length > 0) {
            linksContainer.innerHTML = project.links.map(link =>
                `<a href="${link.url}" target="_blank" rel="noopener" class="project-modal-link">${link.label}</a>`
            ).join('');
        } else {
            linksContainer.innerHTML = '';
        }

        modal.classList.remove('hidden');
    }

    closeModal() {
        document.getElementById('project-detail-modal').classList.add('hidden');
    }

    checkResponsive() {
        this.currentView = window.innerWidth <= 768 ? 'vertical' : 'horizontal';
    }

    getVisibleProjects() {
        if (this.viewMonths === Infinity) {
            return this.projects;
        }
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

        // Spacing units based on time gaps (increased for better visibility)
        if (monthsDiff <= 2) return 80;      // 0-2 months: unit 1
        if (monthsDiff <= 6) return 150;     // 3-6 months: unit 2
        if (monthsDiff <= 12) return 220;    // 7-12 months: unit 3
        return 300;                          // >1 year: unit 4
    }

    // Generate S-curve SVG path
    generateSCurve(isAbove) {
        const height = 40;
        const width = 2;  // Very narrow, just vertical

        if (isAbove) {
            // S-curve going up from marker (bottom) to box (top)
            return `M ${width/2},${height} L ${width/2},0`;
        } else {
            // S-curve going down from marker (top) to box (bottom)
            return `M ${width/2},0 L ${width/2},${height}`;
        }
    }

    render() {
        const visibleProjects = this.getVisibleProjects();

        this.container.innerHTML = `
            <div class="timeline-controls">
                <button id="timeline-zoom-out" class="timeline-btn ${this.viewMonths === Infinity ? 'active' : ''}">Show All</button>
                <button id="timeline-zoom-in" class="timeline-btn ${this.viewMonths === 6 ? 'active' : ''}">Last 6 Months</button>
                <button id="timeline-scroll-start" class="timeline-btn">← First</button>
                <button id="timeline-scroll-end" class="timeline-btn">Last →</button>
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

        // Calculate spacing from previous project
        const spacing = index > 0 ? this.calculateSpacing(allProjects[index - 1], project) : 0;
        const spacingStyle = this.currentView === 'horizontal'
            ? `margin-left: ${spacing}px;`
            : `margin-top: ${spacing}px;`;

        // Determine if this item is above or below (for horizontal)
        const isAbove = index % 2 === 0;

        // S-curve connector for horizontal layout
        const connectorHtml = this.currentView === 'horizontal'
            ? `<svg class="timeline-connector" width="2" height="40" viewBox="0 0 2 40">
                 <path d="${this.generateSCurve(isAbove)}"
                       stroke="#4a5f7a"
                       stroke-width="1.5"
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
                    <div class="timeline-box" data-project-index="${index}">
                        <div class="timeline-date">${this.formatDate(project.date)}</div>
                        <div class="timeline-title">${project.name}</div>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const zoomOut = document.getElementById('timeline-zoom-out');
        const zoomIn = document.getElementById('timeline-zoom-in');
        const scrollStart = document.getElementById('timeline-scroll-start');
        const scrollEnd = document.getElementById('timeline-scroll-end');

        if (zoomOut) {
            zoomOut.addEventListener('click', () => {
                this.viewMonths = Infinity;
                this.render();
                this.attachEventListeners();

                // Scroll to the right end after showing all
                setTimeout(() => {
                    const wrapper = this.container.querySelector('.timeline-wrapper');
                    const track = this.container.querySelector('.timeline-track');
                    if (wrapper && track && this.currentView === 'horizontal') {
                        wrapper.scrollTo({ left: track.scrollWidth, behavior: 'smooth' });
                    }
                }, 100);
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
                const wrapper = this.container.querySelector('.timeline-wrapper');
                if (wrapper) {
                    if (this.currentView === 'horizontal') {
                        wrapper.scrollTo({ left: 0, behavior: 'smooth' });
                    } else {
                        wrapper.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                }
            });
        }

        if (scrollEnd) {
            scrollEnd.addEventListener('click', () => {
                const wrapper = this.container.querySelector('.timeline-wrapper');
                const track = this.container.querySelector('.timeline-track');
                if (wrapper && track) {
                    if (this.currentView === 'horizontal') {
                        wrapper.scrollTo({ left: track.scrollWidth, behavior: 'smooth' });
                    } else {
                        wrapper.scrollTo({ top: track.scrollHeight, behavior: 'smooth' });
                    }
                }
            });
        }

        // Add drag-to-scroll for horizontal timeline
        const wrapper = this.container.querySelector('.timeline-wrapper');
        if (wrapper && this.currentView === 'horizontal') {
            let isDown = false;
            let startX;
            let scrollLeft;

            const handleMouseDown = (e) => {
                if (e.target.closest('.timeline-box')) return;
                isDown = true;
                startX = e.pageX - wrapper.offsetLeft;
                scrollLeft = wrapper.scrollLeft;
                wrapper.style.cursor = 'grabbing';
            };

            const handleMouseLeave = () => {
                isDown = false;
                wrapper.style.cursor = 'grab';
            };

            const handleMouseUp = () => {
                isDown = false;
                wrapper.style.cursor = 'grab';
            };

            const handleMouseMove = (e) => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - wrapper.offsetLeft;
                const walk = (x - startX) * 2;
                wrapper.scrollLeft = scrollLeft - walk;
            };

            wrapper.addEventListener('mousedown', handleMouseDown);
            wrapper.addEventListener('mouseleave', handleMouseLeave);
            wrapper.addEventListener('mouseup', handleMouseUp);
            wrapper.addEventListener('mousemove', handleMouseMove);
        }

        // Add click handlers to open modal
        const boxes = this.container.querySelectorAll('.timeline-box');
        const visibleProjects = this.getVisibleProjects();

        boxes.forEach(box => {
            box.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const projectIndex = parseInt(box.dataset.projectIndex);
                const project = visibleProjects[projectIndex];
                if (project) {
                    this.openModal(project);
                }
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

