chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.action === "analyzeLink") {
            const link = request.link;
            const email = request.email;

            analyzeAndSendEmail(link, email);
        }
    }
);

async function analyzeAndSendEmail(link, email) {
    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link: link, email: email })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Analysis result:', result);

        // Optionally, display a notification to the user
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icon.png', // Replace with your icon
            title: 'Link Analysis Complete',
            message: 'Email sent with link analysis.'
        });

    } catch (error) {
        console.error('Error analyzing link:', error);
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icon.png', // Replace with your icon
            title: 'Link Analysis Failed',
            message: 'Error analyzing link. See console for details.'
        });
    }
} 