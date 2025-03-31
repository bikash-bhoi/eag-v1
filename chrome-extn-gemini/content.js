// Debug logger
function debugLog(component, action, data = null) {
    const timestamp = new Date().toISOString();
    console.log(`[UpgradeMyPrompt][${timestamp}][${component}] ${action}`, data || '');
}

function createOverlay() {
    debugLog('UI', 'Creating overlay');
    const overlay = document.createElement('div');
    overlay.className = 'upgrade-prompt-overlay';
    overlay.innerHTML = `
    <div class="upgrade-prompt-container">
      <h2>✨ Enhanced Prompt</h2>
      <div class="upgrade-prompt-content">
        <div class="loading-spinner"></div>
        <textarea 
          class="upgrade-prompt-textarea" 
          style="display: none;"
          placeholder="Your enhanced prompt will appear here..."
          spellcheck="false"
        ></textarea>
      </div>
      <div class="upgrade-prompt-buttons">
        <button class="upgrade-prompt-button upgrade-prompt-accept">
          Apply Enhancement
        </button>
        <button class="upgrade-prompt-button upgrade-prompt-cancel">
          Cancel
        </button>
      </div>
    </div>
  `;
    document.body.appendChild(overlay);
    return overlay;
}

function findAIEditorInput() {
    const selectors = [
        '[contenteditable="true"]'            // Generic
    ];

    for (const selector of selectors) {
        const element = document.querySelector(selector);
        debugLog("Find prompt element", element)
        if (element) return element;
    }
    return null;
}

function updateEditorContent(content) {
    const editor = findAIEditorInput();
    if (!editor) return;

    if (editor.isContentEditable) {
        editor.textContent = content;
    } else {
        editor.value = content;
    }
    editor.dispatchEvent(new Event('input', { bubbles: true }));
}

function showCopyFeedback() {
    const feedback = document.createElement('div');
    feedback.className = 'copy-feedback';
    feedback.textContent = '✓ Prompt enhanced successfully!';
    document.body.appendChild(feedback);

    setTimeout(() => {
        feedback.classList.add('show');
        setTimeout(() => {
            feedback.classList.remove('show');
            setTimeout(() => feedback.remove(), 300);
        }, 2000);
    }, 100);
}

let currentOverlay = null;

// Add this function to handle textarea auto-resize
function adjustTextareaHeight(textarea) {
    const maxHeight = window.innerHeight * 0.6 - 120; // 60vh - 120px
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px';
}

// Update the showEnhancedPrompt function
function showEnhancedPrompt(prompt) {
    if (currentOverlay) {
        currentOverlay.remove();
    }

    currentOverlay = createOverlay();
    const textarea = currentOverlay.querySelector('.upgrade-prompt-textarea');
    const spinner = currentOverlay.querySelector('.loading-spinner');

    setTimeout(() => {
        currentOverlay.classList.add('active');
        spinner.style.display = 'none';
        textarea.style.display = 'block';
        textarea.value = prompt;
        adjustTextareaHeight(textarea);
    }, 1000);

    // Add resize event listener
    window.addEventListener('resize', () => {
        if (textarea.style.display !== 'none') {
            adjustTextareaHeight(textarea);
        }
    });

    currentOverlay.querySelector('.upgrade-prompt-accept').addEventListener('click', () => {
        updateEditorContent(textarea.value);
        currentOverlay.classList.remove('active');
        setTimeout(() => currentOverlay.remove(), 300);
        showCopyFeedback();
    });

    currentOverlay.querySelector('.upgrade-prompt-cancel').addEventListener('click', () => {
        currentOverlay.classList.remove('active');
        setTimeout(() => currentOverlay.remove(), 300);
    });

    currentOverlay.addEventListener('click', (e) => {
        if (e.target === currentOverlay) {
            currentOverlay.classList.remove('active');
            setTimeout(() => currentOverlay.remove(), 300);
        }
    });
}

function showError(message) {
    if (currentOverlay) {
        const content = currentOverlay.querySelector('.upgrade-prompt-content');
        content.innerHTML = `
          <div class="upgrade-prompt-error">
            <strong>Error:</strong> ${message}
          </div>
        `;
    }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    switch (request.action) {
        case 'getPrompt':
            debugLog('switch', 'getPrompt');
            const editor = findAIEditorInput();
            const text = editor ? (editor.value || editor.textContent) : '';
            debugLog("get prompt", text)
            sendResponse({ prompt: text });
            break;

        case 'showEnhancedPrompt':
            debugLog('switch', 'showEnhancedPrompt');
            showEnhancedPrompt(request.prompt);
            sendResponse({ success: true });
            break;

        case 'showError':
            debugLog('switch', 'showError');
            showError(request.error);
            sendResponse({ success: true });
            break;
    }
    return true;
}); 