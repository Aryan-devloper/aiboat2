// DOM Elements
const micButton = document.getElementById('micButton');
const textInput = document.getElementById('textInput');
const sendButton = document.getElementById('sendButton');
const responseContainer = document.getElementById('responseContainer');
const typingIndicator = document.getElementById('typingIndicator');
const statusText = document.getElementById('statusText');
const orb = document.querySelector('.orb');

// State
let isListening = false;
let isSpeaking = false;
let recognition = null;
let speechSynthesis = window.speechSynthesis;

// Initialize Speech Recognition
function initSpeechRecognition() {
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.log('Speech recognition not supported');
        updateStatus('આ બ્રાઉઝર વૉઇસ સપોર્ટ કરતું નથી');
        return false;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'gu-IN'; // Gujarati
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
            updateStatus('એરર, ફરી પ્રયાસ કરો');
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

    // Clear input
    textInput.value = '';

    // Show typing indicator
    typingIndicator.style.display = 'flex';

    // Simulate AI processing
    setTimeout(() => {
        const response = generateResponse(text);
        displayResponse(response);
        speakResponse(response);
    }, 1500);
}

// Generate AI Response (Mock)
function generateResponse(input) {
    const lowerInput = input.toLowerCase();

    // Menu responses
    const responses = {
        'નાસ્તો': 'આજે નાસ્તામાં પોહા, ઢોકળા અને ચા છે। સવારે 8 થી 9 વાગ્યા સુધી મળશે।',
        'બપોર': 'બપોરે રોટલી, દાળ, ભાત, શાક અને સલાડ છે। સમય: 12 થી 2 વાગ્યા।',
        'રાત': 'રાત્રિભોજન માટે રોટલી, પરાઠા, સબ્જી અને દહીં છે। સમય: 8 થી 10 વાગ્યા।',
        'મેનૂ': 'આજનું મેનૂ: નાસ્તો - પોહા, બપોરે - દાળ ભાત શાક, રાત - પરાઠા સબ્જી। કઈ વખતનું જોઈએ છે?',
        'સમય': 'નાસ્તો: 8-9 વાગ્યા, બપોર: 12-2 વાગ્યા, રાત: 8-10 વાગ્યા।'
    };

    // Check for keywords
    for (let key in responses) {
        if (lowerInput.includes(key)) {
            return responses[key];
        }
    }

    // Default response
    return 'મને સમજાયું નહીં। કૃપા કરીને "નાસ્તો", "બપોર", "રાત" અથવા "મેનૂ" પૂછો।';
}

// Display Response
function displayResponse(text) {
    // Hide typing indicator
    typingIndicator.style.display = 'none';

    // Create response element
    const messageDiv = document.createElement('div');
    messageDiv.className = 'response-message';
    messageDiv.textContent = text;

    // Add to container
    responseContainer.insertBefore(messageDiv, typingIndicator);

    // Scroll to bottom
    responseContainer.scrollTop = responseContainer.scrollHeight;

    // Update status
    updateStatus('જવાબ મળ્યો');
}

// Speak Response
function speakResponse(text) {
    if (!speechSynthesis) {
        console.log('Speech synthesis not supported');
        return;
    }

    // Stop any ongoing speech
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

// Orb Click - Alternative voice activation
orb.addEventListener('click', () => {
    if (!isListening && !isSpeaking) {
        startListening();
    }
});

// Initialize on load
window.addEventListener('load', () => {
    updateStatus('તૈયાર છું');
    
    // Show welcome message after a delay
    setTimeout(() => {
        const welcomeMsg = 'નમસ્તે! હું તમારો હોસ્ટેલ AI સહાયક છું। મને નાસ્તો, બપોર અથવા રાત્રિભોજન વિશે પૂછો।';
        displayResponse(welcomeMsg);
    }, 1000);
});

// Handle browser back button
window.addEventListener('beforeunload', () => {
    if (recognition && isListening) {
        recognition.stop();
    }
    if (speechSynthesis) {
        speechSynthesis.cancel();
    }
});

// Handle visibility change (tab switching)
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
