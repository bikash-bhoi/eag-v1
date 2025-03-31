document.getElementById('saveEmail').addEventListener('click', () => {
    const email = document.getElementById('email').value;
    chrome.storage.sync.set({ email: email }, () => {
        console.log('Email saved: ' + email);
    });
});

document.getElementById('analyzeLink').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTab = tabs[0];
        const link = currentTab.url;

        chrome.storage.sync.get('email', (data) => {
            const email = data.email;
            if (!email) {
                alert('Please save your email address first.');
                return;
            }

            chrome.runtime.sendMessage({
                action: "analyzeLink",
                link: link,
                email: email
            });
        });
    });
}); 