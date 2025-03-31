window.UpgradeMyPromptDebug = {
    log: function (component, action, data = null) {
        const timestamp = new Date().toISOString();
        const message = `[UpgradeMyPrompt][${timestamp}][${component}] ${action}`;

        // Log to console with different colors for better visibility
        console.log(
            `%c${message}`,
            'background: #f0f0f0; color: #2196F3; padding: 2px 5px; border-radius: 3px;',
            data || ''
        );
    },

    error: function (component, action, error) {
        const timestamp = new Date().toISOString();
        const message = `[UpgradeMyPrompt][${timestamp}][${component}] ${action}`;

        console.error(
            `%c${message}`,
            'background: #fff0f0; color: #f44336; padding: 2px 5px; border-radius: 3px;',
            error
        );
    }
}; 