// DOM Elements
const micButton = document.getElementById('micButton');
const textInput = document.getElementById('textInput');
const sendButton = document.getElementById('sendButton');
const responseContainer = document.getElementById('responseContainer');
const typingIndicator = document.getElementById('typingIndicator');
const statusText = document.getElementById('statusText');
const orb = document.querySelector('.orb');
const citySelect = document.getElementById('citySelect');
const boatSelect = document.getElementById('boatSelect');
const selectedBoatInfo = document.getElementById('selectedBoatInfo');
const selectedBoatName = document.getElementById('selectedBoatName');

// State
let isListening = false;
let isSpeaking = false;
let recognition = null;
let speechSynthesis = window.speechSynthesis;
let selectedBoatId = null;

// All boats data (will be populated from template)
const allBoats = [
    {% for boat in boats %}
    {
        id: {{ boat.id }},
        name: "{{ boat.name }}",
        nameGujarati: "{{ boat.name_gujarati }}",
        cityId: {{ boat.city.id }}
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
];

// Get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// City Selection Handler
citySelect.addEventListener('change', (e) => {
    const cityId = parseInt(e.target.value);
    
    if (!cityId) {
        boatSelect.innerHTML = '<option value="">પહેલા શહેર પસંદ કરો</option>';
        boatSelect.disabled = true;
        selectedBoatInfo.style.display = 'none';
        selectedBoatId = null;
        return;
    }
    
    // Filter boats by city
    const cityBoats = allBoats.filter(boat => boat.cityId === cityId);
    
    boatSelect.innerHTML = '<option value="">બોટ પસંદ કરો</option>';
    cityBoats.forEach(boat => {
        const option = document.createElement('option');
        option.value = boat.id;
        option.textContent = boat.nameGujarati || boat.name;
        boatSelect.appendChild(option);
    });
    
    boatSelect.disabled = false;
    selectedBoatInfo.style.display = 'none';
    selectedBoatId = null;
});

// Boat Selection Handler
boatSelect.addEventListener('change', (e) => {
    const boatId = parseInt(e.target.value);
    
    if (!boatId) {
        selectedBoatInfo.style.display = 'none';
        selectedBoatId = null;
        return;
    }
    
    selectedBoatId = boatId;
    const boat = allBoats.find(b => b.id === boatId);
    
    if (boat) {
        selectedBoatName.textContent = boat.nameGujarati || boat.name;
        selectedBoatInfo.style.display = 'flex';
        updateStatus(`${boat.nameGujarati || boat.name} પસંદ કર્યું`);
    }
});

// Initialize Speech Recognition
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.log('Speech recognition not supported');
        updateStatus('આ બ્રાઉઝર વૉઇસ સપોર્ટ કરતું નથી');
        return false;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'gu-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        isListening = true;
        micButton.classList.add('active');
        orb.classList.add('listening');
        updateStatus('સાંભળી રહ્યો છું...');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Recognized:', transcript);
        handleUserInput(transcript);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        stopListening();
        
        if (event.error === 'no-speech') {
            updateStatus('કંઈ સાંભળ્યું નહીં, ફરી પ્રયાસ કરો');
        } else {
            updateStatus('એરર, ફરી 
                query: text,
                boat_id: selectedBoatId
           );
        }
    };

    recognition.onend = () => {
        stopListening();
    };

    return true;
}

// Start Listening
function startListening() {
    if (!recognition) {
        if (!initSpeechRecognition()) {
            return;
        }
    }

    try {
        recognition.start();
    } catch (error) {
        console.error('Error starting recognition:', error);
    }
}

// Stop Listening
function stopListening() {
    isListening = false;
    micButton.classList.remove('active');
    orb.classList.remove('listening');
    updateStatus('તૈયાર છું');
}

// Handle User Input
async function handleUserInput(text) {
    if (!text.trim()) return;

    textInput.value = '';
    typingIndicator.style.display = 'flex';

    try {
        const response = await fetch('/api/query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ query: text })
        });

        const data = await response.json();

        if (data.success) {
            displayResponse(data.response);
            speakResponse(data.response);
        } else {
            displayResponse('માફ કરશો, એરર આવી. ફરી પ્રયાસ કરો.');
        }
    } catch (error) {
        console.error('Error:', error);
        displayResponse('માફ કરશો, એરર આવી. ફરી પ્રયાસ કરો.');
    }

    typingIndicator.style.display = 'none';
}

// Display Response
function displayResponse(text) {
    typingIndicator.style.display = 'none';

    const messageDiv = document.createElement('div');
    messageDiv.className = 'response-message';
    messageDiv.textContent = text;

    responseContainer.insertBefore(messageDiv, typingIndicator);
    responseContainer.scrollTop = responseContainer.scrollHeight;

    updateStatus('જવાબ મળ્યો');
}

// Speak Response
function speakResponse(text) {
    if (!speechSynthesis) {
        console.log('Speech synthesis not supported');
        return;
    }

    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'gu-IN';
    utterance.rate = 0.9;
    utterance.pitch = 1;

    utterance.onstart = () => {
        isSpeaking = true;
        orb.classList.add('speaking');
        updateStatus('બોલી રહ્યો છું...');
    };

    utterance.onend = () => {
        isSpeaking = false;
        orb.classList.remove('speaking');
        updateStatus('તૈયાર છું');
    };

    utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event);
        isSpeaking = false;
        orb.classList.remove('speaking');
        updateStatus('તૈયાર છું');
    };

    speechSynthesis.speak(utterance);
}

// Update Status Text
function updateStatus(text) {
    statusText.textContent = text;
}

// Event Listeners
micButton.addEventListener('click', () => {
    if (isListening) {
        recognition.stop();
    } else {
        startListening();
    }
});

sendButton.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (text) {
        handleUserInput(text);
    }
});

textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = textInput.value.trim();
        if (text) {
            handleUserInput(text);
        }
    }
});

orb.addEventListener('click', () => {
    if (!isListening && !isSpeaking) {
        startListening();
    }
});

// Initialize on load
window.addEventListener('load', () => {
    updateStatus('તૈયાર છું');
    
    setTimeout(() => {
        const welcomeMsg = 'નમસ્તે! હું તમારો હોસ્ટેલ AI સહાયક છું। મને નાસ્તો, બપોર અથવા રાત્રિભોજન વિશે પૂછો।';
        displayResponse(welcomeMsg);
    }, 1000);
});

window.addEventListener('beforeunload', () => {
    if (recognition && isListening) {
        recognition.stop();
    }
    if (speechSynthesis) {
        speechSynthesis.cancel();
    }
});

document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        if (recognition && isListening) {
            recognition.stop();
        }
        if (speechSynthesis) {
            speechSynthesis.cancel();
        }
    }
});
