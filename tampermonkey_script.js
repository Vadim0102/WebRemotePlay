// ==UserScript==
// @name         WebRemotePlay
// @namespace    https://github.com/Vadim0102/WebRemotePlay/blob/main/tampermonkey_script.js
// @version      2024-07-27
// @description  Play PC browser games from your phone as a controller (TamperMonkey script)
// @author       Vadim0102
// @match        http://*/*
// @match        https://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

let socket;
let reconnectInterval = 1000;

function connect() {
    socket = new WebSocket('ws://localhost:8080/ws');

    socket.onopen = function(event) {
        console.log('WebSocket connection established');
        reconnectInterval = 1000;
    };

    socket.onmessage = function(event) {
        const messages = JSON.parse(event.data);
        if (Array.isArray(messages)) {
            messages.forEach(message => {
                if (message.type === 'keyPress') {
                    simulateKeyPress(message.key);
                }
                if (message.type === 'keyDown') {
                    simulateKeyDown(message.key);
                }
                if (message.type === 'keyUp') {
                    simulateKeyUp(message.key);
                }
            });
        }
        console.log('Message from server:', event.data);
    };

    socket.onerror = function(event) {
        console.error('WebSocket error:', event);
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed. Attempting to reconnect...');
        setTimeout(connect, reconnectInterval);
        reconnectInterval = Math.min(reconnectInterval * 2, 30000);
    };
}

function simulateKeyEvent(type, key) {
    key = Number(key);
    const event = new KeyboardEvent(type, {
        key: key,
        code: key,
        keyCode: key,
        which: key,
        bubbles: true,
        cancelable: true
    });
    document.dispatchEvent(event);
}

function simulateKeyPress(key) {
    simulateKeyEvent('keydown', key);
    simulateKeyEvent('keypress', key);
    simulateKeyEvent('keyup', key);
}

function simulateKeyDown(key) {
    simulateKeyEvent('keydown', key);
}

function simulateKeyUp(key) {
    simulateKeyEvent('keyup', key);
}

connect();
