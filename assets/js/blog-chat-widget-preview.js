// Blog Chat Widget - Preview Implementation
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
        this.init();
    }

    init() {
        this.createWidget();
        this.attachEventListeners();
    }

    createWidget() {
        // Create floating button
        const button = document.createElement('div');
        button.id = 'blog-chat-button';
        button.innerHTML = '💬 Ask about my blog';
        button.className = 'blog-chat-button';
        
        // Create modal
        const modal = document.createElement('div');
        modal.id = 'blog-chat-modal';
        modal.className = 'blog-chat-modal hidden';
        modal.innerHTML = `
            <div class="blog-chat-content">
                <div class="blog-chat-header">
                    <h3>🤖 Blog Assistant</h3>
                    <button class="blog-chat-close">✕</button>
                </div>
                <div class="blog-chat-body">
                    <div class="blog-chat-input-section">
                        <textarea id="blog-chat-input" 
                                placeholder="What would you like to know about my blog?"
                                rows="3"></textarea>
                        <button id="blog-chat-ask" class="blog-chat-ask-btn">Ask 🔍</button>
                    </div>
                    <div id="blog-chat-response" class="blog-chat-response hidden">
                        <div class="response-content"></div>
                        <div class="response-sources"></div>
                        <button id="blog-chat-reset" class="blog-chat-reset-btn">Ask Another 🔄</button>
                    </div>
                    <div id="blog-chat-loading" class="blog-chat-loading hidden">
                        <div class="spinner"></div>
                        <p>Searching through blog posts...</p>
                    </div>
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
    }

    openModal() {
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
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: question,
                context_limit: 3
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();
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

        let html = '<h4>📚 Sources:</h4>';
        
        contextUsed.forEach((source, index) => {
            const relevance = Math.round((1 - source.distance) * 100);
            const title = source.metadata.title || 'Unknown Post';
            const url = source.metadata.url || '#';
            
            html += `
                <div class="source-item">
                    <div class="source-header">
                        <span class="source-title">📄 ${title}</span>
                        <span class="source-relevance">Relevance: ${relevance}%</span>
                    </div>
                    <div class="source-actions">
                        <a href="${url}" target="_blank" class="source-link">View Post →</a>
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
                <h4>❌ Sorry, something went wrong</h4>
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
