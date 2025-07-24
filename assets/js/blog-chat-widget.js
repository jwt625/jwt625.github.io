// Blog Chat Widget - Production Implementation
class BlogChatWidget {
    constructor() {
        // Check if API URL is configured
        if (!window.CHAT_CONFIG?.apiUrl) {
            console.warn('Chat widget: No API URL configured');
            return; // Don't initialize if no API URL
        }

        this.apiUrl = window.CHAT_CONFIG.apiUrl + '/rag/generate-test';
        this.lastRequestTime = 0;
        this.rateLimitMs = 30000; // 30 seconds between requests

        // Sample questions based on actual blog content
        this.sampleQuestions = [
            "How do you wirebond microwave circuits?",
            "What are the key parameters for thermal mass flow controllers?",
            "How do you get light onto a photonic chip?",
            "What's the difference between Coriolis and thermal flow meters?",
            "What's the de Broglie wavelength of 10 kV electrons in e-beam lithography?",
            "How do you calculate the flux quantum threading for superconducting resonator tuning?",
            "Why do wavelength-scale acoustic waveguides need large transducers for efficient coupling?",
            "What's the Schwinger limit for dielectric breakdown in perfect vacuum?",
            "How does kinetic inductance in NbTiN change with magnetic flux threading?"
        ];

        console.log('Chat widget initialized with API URL:', this.apiUrl);

        // Check for potential mixed content issues
        const isHttps = window.location.protocol === 'https:';
        const isApiHttp = this.apiUrl.startsWith('http://');
        if (isHttps && isApiHttp) {
            console.warn('Mixed Content Error: HTTPS site cannot access HTTP API. Chat widget will be disabled.');
            this.showMixedContentError();
            return; // Don't initialize the widget
        }

        this.init();
    }

    showMixedContentError() {
        // Create a simple error message instead of the full widget
        const errorDiv = document.createElement('div');
        errorDiv.id = 'blog-chat-error';
        errorDiv.className = 'blog-chat-error';
        errorDiv.innerHTML = `
            <div class="blog-chat-error-content">
                <h4>Chat Widget Unavailable</h4>
                <p>The chat widget requires HTTPS API access but the server only supports HTTP.</p>
                <p>This is a security limitation of modern browsers (Mixed Content Policy).</p>
                <details>
                    <summary>Technical Details</summary>
                    <p>Site: ${window.location.protocol}//${window.location.host} (HTTPS)</p>
                    <p>API: ${this.apiUrl} (HTTP)</p>
                    <p>Solution: Enable HTTPS on the API server</p>
                </details>
            </div>
        `;

        // Add some basic styling
        errorDiv.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 15px;
            max-width: 300px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        `;

        document.body.appendChild(errorDiv);

        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 10000);
    }

    init() {
        this.createWidget();
        this.attachEventListeners();
    }

    createWidget() {
        // Create floating button
        const button = document.createElement('div');
        button.id = 'blog-chat-button';
        button.innerHTML = 'RAG my blog';
        button.className = 'blog-chat-button';

        // Get random sample question for placeholder
        const randomQuestion = this.sampleQuestions[Math.floor(Math.random() * this.sampleQuestions.length)];

        // Create modal
        const modal = document.createElement('div');
        modal.id = 'blog-chat-modal';
        modal.className = 'blog-chat-modal hidden';
        modal.innerHTML = `
            <div class="blog-chat-content">
                <div class="blog-chat-header">
                    <h3>Let's RAG!</h3>
                    <button class="blog-chat-close">&times;</button>
                </div>
                <div class="blog-chat-body">
                    <div class="blog-chat-input-section">
                        <textarea id="blog-chat-input"
                                placeholder="${randomQuestion}"
                                rows="3"></textarea>
                        <button id="blog-chat-ask" class="blog-chat-ask-btn">Show me what you got</button>
                    </div>
                    <div id="blog-chat-response" class="blog-chat-response hidden">
                        <div class="response-content"></div>
                        <div class="response-sources"></div>
                        <button id="blog-chat-reset" class="blog-chat-reset-btn">Ask Another</button>
                    </div>
                    <div id="blog-chat-loading" class="blog-chat-loading hidden">
                        <div class="spinner"></div>
                        <p>Searching through blog posts...</p>
                    </div>
                </div>
                <div class="blog-chat-privacy-notice">
                    <p><strong>Privacy Notice:</strong> Your questions are logged for system improvement. By using this chat, you consent to data collection as described in our <a href="/privacy-policy/" target="_blank">Privacy Policy</a>.</p>
                </div>
            </div>
        `;

        document.body.appendChild(button);
        document.body.appendChild(modal);
    }

    attachEventListeners() {
        // Open modal
        document.getElementById('blog-chat-button').addEventListener('click', () => {
            this.openModal();
        });

        // Close modal
        document.querySelector('.blog-chat-close').addEventListener('click', () => {
            this.closeModal();
        });

        // Ask question
        document.getElementById('blog-chat-ask').addEventListener('click', () => {
            this.askQuestion();
        });

        // Reset for new question
        document.getElementById('blog-chat-reset').addEventListener('click', () => {
            this.resetChat();
        });

        // Enter key to ask
        document.getElementById('blog-chat-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.askQuestion();
            }
        });

        // Close on outside click
        document.getElementById('blog-chat-modal').addEventListener('click', (e) => {
            if (e.target.id === 'blog-chat-modal') {
                this.closeModal();
            }
        });

        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !document.getElementById('blog-chat-modal').classList.contains('hidden')) {
                this.closeModal();
            }
        });
    }

    openModal() {
        // Update placeholder with a new random question each time
        const randomQuestion = this.sampleQuestions[Math.floor(Math.random() * this.sampleQuestions.length)];
        document.getElementById('blog-chat-input').placeholder = randomQuestion;

        document.getElementById('blog-chat-modal').classList.remove('hidden');
        document.getElementById('blog-chat-input').focus();
    }

    closeModal() {
        document.getElementById('blog-chat-modal').classList.add('hidden');
    }

    resetChat() {
        document.getElementById('blog-chat-input').value = '';
        document.getElementById('blog-chat-response').classList.add('hidden');
        document.getElementById('blog-chat-input').focus();
    }

    async askQuestion() {
        const input = document.getElementById('blog-chat-input');
        const question = input.value.trim();
        
        if (!question) return;

        // Rate limiting check
        const now = Date.now();
        if (now - this.lastRequestTime < this.rateLimitMs) {
            const waitTime = Math.ceil((this.rateLimitMs - (now - this.lastRequestTime)) / 1000);
            alert(`Please wait ${waitTime} seconds before asking another question.`);
            return;
        }

        this.showLoading();
        
        try {
            const response = await this.callAPI(question);
            this.displayResponse(response);
            this.lastRequestTime = now;
        } catch (error) {
            this.displayError(error);
        }
    }

    async callAPI(question) {
        console.log('Making API request to:', this.apiUrl);
        console.log('Request payload:', { query: question, context_limit: 3 });

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({
                    query: question,
                    context_limit: 3
                })
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API Error Response:', errorText);
                throw new Error(`API Error: ${response.status} - ${response.statusText}`);
            }

            const data = await response.json();
            console.log('API Response:', data);
            return data;
        } catch (error) {
            console.error('Fetch error:', error);
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                const isHttps = window.location.protocol === 'https:';
                const isApiHttp = this.apiUrl.startsWith('http://');

                if (isHttps && isApiHttp) {
                    throw new Error(`Mixed Content Error: Cannot access HTTP API (${this.apiUrl}) from HTTPS site. Please access the site via HTTP (http://127.0.0.1:4000) or use an HTTPS API endpoint.`);
                } else {
                    throw new Error(`Network Error: Cannot reach API at ${this.apiUrl}. Please check if the API server is running and accessible.`);
                }
            }
            throw error;
        }
    }

    showLoading() {
        document.getElementById('blog-chat-loading').classList.remove('hidden');
        document.getElementById('blog-chat-response').classList.add('hidden');
    }

    displayResponse(data) {
        document.getElementById('blog-chat-loading').classList.add('hidden');
        
        const responseDiv = document.getElementById('blog-chat-response');
        const contentDiv = responseDiv.querySelector('.response-content');
        const sourcesDiv = responseDiv.querySelector('.response-sources');

        // Render main answer as markdown
        contentDiv.innerHTML = this.renderMarkdown(data.answer);

        // Render sources
        sourcesDiv.innerHTML = this.renderSources(data.context_used);

        responseDiv.classList.remove('hidden');
    }

    renderMarkdown(text) {
        // Simple markdown rendering (you'd use a proper library in production)
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
    }

    renderSources(contextUsed) {
        if (!contextUsed || contextUsed.length === 0) {
            return '<p>No sources found.</p>';
        }

        let html = '<h4>Sources:</h4>';
        
        contextUsed.forEach((source) => {
            const relevance = Math.round((1 - source.distance) * 100);
            const title = source.metadata.title || 'Unknown Post';
            const url = source.metadata.url || '#';
            
            html += `
                <div class="source-item">
                    <div class="source-header">
                        <span class="source-title">${title}</span>
                        <span class="source-relevance">Relevance: ${relevance}%</span>
                    </div>
                    <div class="source-actions">
                        <a href="${url}" target="_blank" class="source-link">View Post &rarr;</a>
                    </div>
                </div>
            `;
        });

        return html;
    }

    displayError(error) {
        document.getElementById('blog-chat-loading').classList.add('hidden');
        
        const responseDiv = document.getElementById('blog-chat-response');
        const contentDiv = responseDiv.querySelector('.response-content');
        
        contentDiv.innerHTML = `
            <div class="error-message">
                <h4>Sorry, something went wrong</h4>
                <p>Unable to get a response from the blog assistant. Please try again later.</p>
                <details>
                    <summary>Error details</summary>
                    <code>${error.message}</code>
                </details>
            </div>
        `;
        
        responseDiv.querySelector('.response-sources').innerHTML = '';
        responseDiv.classList.remove('hidden');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new BlogChatWidget();
});
