// Create a debug function for the service worker context
function debugLog(component, action, data = null) {
    const timestamp = new Date().toISOString();
    console.log(`[UpgradeMyPrompt][${timestamp}][${component}][ServiceWorker] ${action}`, data || '');
}

// Initialize Gemini API
const CONSTANTS = {
    MODEL: "gemini-2.0-flash",
    PROMPT_TEMPLATE: "Enhance this prompt to be more specific and effective. Include placeholders for customization where relevant. Return only the enhanced prompt without any explanations or header: ",
    GEMINI_URL: "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyCxAOJr0aqQcx_ZF7oajt-DQYy5SOybqV4"
};

// Log when the service worker starts
debugLog('ServiceWorker', 'Starting service worker');

async function loadGeminiAPI() {
    debugLog('API', 'Initializing Gemini API');
    try {
        const response = await fetch(CONSTANTS.GEMINI_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: ''
                    }]
                }]
            })
        });
        debugLog('API', 'Initialization response', {
            status: response.status,
            ok: response.ok,
            statusText: response.statusText
        });
        return response.ok;
    } catch (error) {
        debugLog('API', 'Initialization failed', {
            error: error.message,
            stack: error.stack
        });
        return false;
    }
}

// Create context menu
chrome.runtime.onInstalled.addListener(async () => {
    debugLog('Extension', 'Installing extension');
    const apiInitialized = await loadGeminiAPI();
    debugLog('Extension', 'API initialization result', { success: apiInitialized });

    chrome.contextMenus.create({
        id: "enhancePrompt",
        title: "Upgrade My Prompt",
        contexts: ["editable"]
    });
    debugLog('Extension', 'Context menu created');
});

async function enhancePrompt(prompt) {
    debugLog('Prompt', 'Enhancing prompt', { original: prompt });
    try {
        const response = await fetch(CONSTANTS.GEMINI_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: CONSTANTS.PROMPT_TEMPLATE + prompt
                    }]
                }]
            })
        });

        debugLog('API', 'Enhancement response status', { status: response.status });
        const data = await response.json();
        debugLog('API', 'Enhancement response data', data);

        if (data.candidates && data.candidates[0].content) {
            const enhancedPrompt = data.candidates[0].content.parts[0].text;
            debugLog('Prompt', 'Enhancement successful', { enhanced: enhancedPrompt });
            return enhancedPrompt;
        }
        throw new Error('Invalid response from Gemini API');
    } catch (error) {
        debugLog('Prompt', 'Enhancement failed', error);
        throw new Error(`Failed to enhance prompt: ${error.message}`);
    }
}

async function handlePromptEnhancement(tabId) {
    debugLog('Handler', 'Starting prompt enhancement', { tabId });
    try {
        const result = await chrome.tabs.sendMessage(tabId, { action: 'getPrompt' });
        debugLog('Handler', 'Got prompt from tab', result);

        if (!result.prompt) {
            debugLog('Handler', 'No prompt found');
            return;
        }

        const enhancedPrompt = await enhancePrompt(result.prompt);
        debugLog('Handler', 'Sending enhanced prompt to tab');
        chrome.tabs.sendMessage(tabId, {
            action: 'showEnhancedPrompt',
            prompt: enhancedPrompt
        });
    } catch (error) {
        debugLog('Handler', 'Error in enhancement process', error);
        chrome.tabs.sendMessage(tabId, {
            action: 'showError',
            error: error.message
        });
    }
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
    debugLog('Menu', 'Context menu clicked', info);
    if (info.menuItemId === "enhancePrompt") {
        handlePromptEnhancement(tab.id);
    }
});

chrome.commands.onCommand.addListener((command, tab) => {
    debugLog('Shortcut', 'Keyboard shortcut triggered', { command });
    if (command === "enhance-prompt") {
        handlePromptEnhancement(tab.id);
    }
});