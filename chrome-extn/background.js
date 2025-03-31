// Initialize the extension
chrome.runtime.onInstalled.addListener(() => {
    console.log('Form Filler Extension installed');

    // Create parent menu item
    chrome.contextMenus.create({
        id: 'formFiller',
        title: 'Form Filler',
        contexts: ['page', 'editable']
    });

    // Create child menu items
    chrome.contextMenus.create({
        id: 'fillForm',
        parentId: 'formFiller',
        title: 'Fill Form with Random Data',
        contexts: ['page', 'editable']
    });

    chrome.contextMenus.create({
        id: 'clearForm',
        parentId: 'formFiller',
        title: 'Clear Form',
        contexts: ['page', 'editable']
    });

    // Add separator
    chrome.contextMenus.create({
        id: 'separator',
        parentId: 'formFiller',
        type: 'separator',
        contexts: ['page', 'editable']
    });

    // Add fill single field option
    chrome.contextMenus.create({
        id: 'fillField',
        parentId: 'formFiller',
        title: 'Fill This Field Only',
        contexts: ['editable']
    });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    try {
        switch (info.menuItemId) {
            case 'fillForm':
                await chrome.tabs.sendMessage(tab.id, { action: "fillForm" });
                break;
            case 'clearForm':
                await chrome.tabs.sendMessage(tab.id, { action: "clearForm" });
                break;
            case 'fillField':
                await chrome.tabs.sendMessage(tab.id, {
                    action: "fillField",
                    targetElementId: info.targetElementId
                });
                break;
        }
    } catch (error) {
        console.error('Error handling context menu click:', error);
    }
});

// Handle icon click
chrome.action.onClicked.addListener(async (tab) => {
    try {
        await chrome.tabs.sendMessage(tab.id, { action: "fillForm" });
    } catch (error) {
        console.error('Error sending message:', error);
    }
});

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener(async (command, tab) => {
    try {
        if (command === "fill-form") {
            await chrome.tabs.sendMessage(tab.id, { action: "fillForm" });
        } else if (command === "clear-form") {
            await chrome.tabs.sendMessage(tab.id, { action: "clearForm" });
        }
    } catch (error) {
        console.error('Error handling command:', error);
    }
});

// Add error handling for messaging
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Message received:', message);
    sendResponse({ received: true });
    return true;
}); 