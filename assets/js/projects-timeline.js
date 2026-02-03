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
        this.initToggle();
        this.checkResponsive();
        this.render();
        this.attachEventListeners();

        window.addEventListener('resize', () => {
            this.checkResponsive();
            this.render();
            this.attachEventListeners();
        });
    }

    initToggle() {
        const toggleBtn = document.getElementById('timeline-toggle-btn');
        if (!toggleBtn) return;

        // Default to hidden on all devices
        const defaultVisible = false;

        // Check localStorage for saved preference
        const savedState = localStorage.getItem('timeline_visible');
        const isVisible = savedState !== null ? savedState === 'true' : defaultVisible;

        // Set initial state
        this.setTimelineVisibility(isVisible);

        // Add click handler
        toggleBtn.addEventListener('click', () => {
            const currentlyVisible = !this.container.classList.contains('hidden');
            this.setTimelineVisibility(!currentlyVisible);
            localStorage.setItem('timeline_visible', !currentlyVisible);
        });
    }

    setTimelineVisibility(visible) {
        const toggleBtn = document.getElementById('timeline-toggle-btn');
        if (visible) {
            this.container.classList.remove('hidden');
            toggleBtn.classList.remove('collapsed');
        } else {
            this.container.classList.add('hidden');
            toggleBtn.classList.add('collapsed');
        }
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

        // Check if project has an embed_url for iframe
        if (project.embed_url && project.embed_url.trim() !== '') {
            imageContainer.innerHTML = `
                <iframe
                    src="${project.embed_url}"
                    width="100%"
                    height="600">
                </iframe>
            `;
        } else {
            // Support both single 'image' (string) and multiple 'images' (array)
            let imagesToDisplay = [];
            if (project.images && Array.isArray(project.images) && project.images.length > 0) {
                // Filter out empty strings
                imagesToDisplay = project.images.filter(img => img && img.trim() !== '');
            } else if (project.image && project.image.trim() !== '') {
                imagesToDisplay = [project.image];
            }

            if (imagesToDisplay.length > 0) {
                if (imagesToDisplay.length === 1) {
                    // Single image - display as before
                    imageContainer.innerHTML = `<img src="${imagesToDisplay[0]}" alt="${project.name}" class="project-modal-image" />`;
                } else {
                    // Multiple images - display as gallery
                    imageContainer.innerHTML = `
                        <div class="project-modal-image-gallery">
                            ${imagesToDisplay.map((img, idx) =>
                                `<img src="${img}" alt="${project.name} - Image ${idx + 1}" class="project-modal-image gallery-image" />`
                            ).join('')}
                        </div>
                    `;
                }
            } else {
                imageContainer.innerHTML = '';
            }
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
        // Use end_date if available, otherwise use start date
        const date1 = project1.end_date ? new Date(project1.end_date) : new Date(project1.date);
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

        // Calculate duration segment if end_date exists
        let durationSegment = '';
        if (project.end_date) {
            const startDate = new Date(project.date);
            const endDate = new Date(project.end_date);
            const durationMonths = (endDate.getFullYear() - startDate.getFullYear()) * 12 +
                                   (endDate.getMonth() - startDate.getMonth());

            // Calculate width based on duration
            const segmentWidth = this.calculateDurationWidth(durationMonths);

            if (this.currentView === 'horizontal') {
                durationSegment = `<div class="timeline-duration-segment" style="width: ${segmentWidth}px;"></div>`;
            } else {
                durationSegment = `<div class="timeline-duration-segment vertical" style="height: ${segmentWidth}px;"></div>`;
            }
        }

        // S-curve connector for horizontal layout
        const connectorHtml = this.currentView === 'horizontal'
            ? `<svg class="timeline-connector" width="2" height="40" viewBox="0 0 2 40">
                 <path d="${this.generateSCurve(isAbove)}"
                       stroke="#4a5f7a"
                       stroke-width="1.5"
                       fill="none"/>
               </svg>`
            : `<svg class="timeline-connector" width="18" height="2" viewBox="0 0 18 2">
                 <line x1="0" y1="1" x2="18" y2="1"
                       stroke="#4a5f7a"
                       stroke-width="2"/>
               </svg>`;

        // Render icon if available, and background image if image exists
        const hasIcon = project.icon && project.icon.trim() !== '';

        // Get first image from either 'image' (string) or 'images' (array)
        let projectImage = '';
        if (project.image && project.image.trim() !== '') {
            projectImage = project.image;
        } else if (project.images && Array.isArray(project.images) && project.images.length > 0) {
            projectImage = project.images[0];
        }
        const hasImage = projectImage !== '';

        const iconHtml = hasIcon
            ? `<img src="${project.icon}" alt="${project.name} icon" class="timeline-icon" />`
            : '';

        // Always show background image if available (even when icon exists)
        const bgImageHtml = hasImage
            ? `<div class="timeline-bg-image" style="background-image: url('${projectImage}');"></div>`
            : '';

        const boxClass = hasImage ? 'has-bg-image' : '';

        return `
            <div class="timeline-item ${categoryClass} ${project.end_date ? 'has-duration' : ''}" data-index="${index}" style="${spacingStyle}">
                <div class="timeline-marker"></div>
                ${durationSegment}
                ${connectorHtml}
                <div class="timeline-content">
                    <div class="timeline-box ${boxClass}" data-project-index="${index}">
                        ${bgImageHtml}
                        <div class="timeline-box-content">
                            <div class="timeline-date">${this.formatDate(project.date)}${project.end_date ? ' - ' + this.formatDate(project.end_date) : ''}</div>
                            <div class="timeline-title">${project.name}</div>
                            ${iconHtml}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    calculateDurationWidth(months) {
        // Use similar spacing logic as calculateSpacing
        if (months <= 2) return months * 40;
        if (months <= 6) return 80 + (months - 2) * 37.5;
        if (months <= 12) return 230 + (months - 6) * 36.67;
        return 450 + (months - 12) * 25;
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

