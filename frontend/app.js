// frontend/app.js

/*document.getElementById('analyzeButton').addEventListener('click', () => {
    const inputText = document.getElementById('inputText').value.trim();
    if (!inputText) {
        alert('Please enter some text or a URL to analyze.');
        return;
    }

    const data = { text: inputText }; // Adjust as necessary if supporting URLs

    fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        displayResults(result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});*/

// frontend/index.js

const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkModeToggle = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkModeToggle.querySelector('span:nth-child(1)').classList.toggle('active');
    darkModeToggle.querySelector('span:nth-child(2)').classList.toggle('active');
});

// Event listener for the Analyze button
document.getElementById('analyzeButton').addEventListener('click', () => {
    const inputText = document.getElementById('inputText').value.trim();
    if (!inputText) {
        alert('Please enter some text or a URL to analyze.');
        return;
    }

    const data = { text: inputText };

    fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        displayResults(result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    const evidenceLinksDiv = document.getElementById('evidence-links');
    resultsDiv.innerHTML = '';
    evidenceLinksDiv.innerHTML = '';

    if (result.message) {
        resultsDiv.innerText = result.message;
        return;
    }

    if (result.results) {
        result.results.forEach(item => {
            // Result Item
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');

            // Info Section
            const infoDiv = document.createElement('div');
            infoDiv.classList.add('info');
            const claimH3 = document.createElement('h3');
            claimH3.textContent = `Claim: ${item.claim}`;
            const classificationP = document.createElement('p');
            classificationP.innerHTML = `<strong>Classification:</strong> ${item.classification}`;
            const confidenceP = document.createElement('p');
            confidenceP.innerHTML = `<strong>Confidence:</strong> ${(item.confidence * 100).toFixed(2)}%`;

            infoDiv.appendChild(claimH3);
            infoDiv.appendChild(classificationP);
            infoDiv.appendChild(confidenceP);

            resultItem.appendChild(infoDiv);
            resultsDiv.appendChild(resultItem);

            // Evidence Links for this claim
            if (item.evidence_links && item.evidence_links.length > 0) {
                const evidenceHeader = document.createElement('h4');
                evidenceHeader.textContent = 'Evidence Links:';
                evidenceLinksDiv.appendChild(evidenceHeader);

                item.evidence_links.forEach(link => {
                    const linkItem = document.createElement('div');
                    linkItem.classList.add('link-item');
                    const linkAnchor = document.createElement('a');
                    linkAnchor.href = link;
                    linkAnchor.target = '_blank';
                    linkAnchor.textContent = link;
                    linkItem.appendChild(linkAnchor);
                    evidenceLinksDiv.appendChild(linkItem);
                });
            }
        });
    }
}
/*
// Function to display the results
function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (result.message) {
        resultsDiv.innerText = result.message;
        return;
    }

    if (result.results) {
        result.results.forEach(item => {
            // Result Item
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');

            // Info Section
            const infoDiv = document.createElement('div');
            infoDiv.classList.add('info');
            const claimH3 = document.createElement('h3');
            claimH3.textContent = `Claim: ${item.claim}`;
            const classificationP = document.createElement('p');
            classificationP.innerHTML = `<strong>Classification:</strong> ${item.classification}`;
            const confidenceP = document.createElement('p');
            confidenceP.innerHTML = `<strong>Confidence:</strong> ${(item.confidence * 100).toFixed(2)}%`;

            infoDiv.appendChild(claimH3);
            infoDiv.appendChild(classificationP);
            infoDiv.appendChild(confidenceP);

            resultItem.appendChild(infoDiv);

            // Evidence Links for this claim
            if (item.evidence_links && item.evidence_links.length > 0) {
                const evidenceHeader = document.createElement('h4');
                evidenceHeader.textContent = 'Evidence Links:';
                infoDiv.appendChild(evidenceHeader);

                const evidenceList = document.createElement('ul');
                item.evidence_links.forEach(link => {
                    const linkItem = document.createElement('li');
                    const linkAnchor = document.createElement('a');
                    linkAnchor.href = link;
                    linkAnchor.target = '_blank';
                    linkAnchor.textContent = link;
                    linkItem.appendChild(linkAnchor);
                    evidenceList.appendChild(linkItem);
                });
                infoDiv.appendChild(evidenceList);
            }

            resultsDiv.appendChild(resultItem);
        });
    }
}
*/