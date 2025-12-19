/**
 * Background Service Worker
 *
 * This runs in the background and can:
 * - Listen for messages from content script and popup
 * - Capture screenshots using chrome.tabs.captureVisibleTab()
 * - Communicate with the Python backend
 *
 * Key APIs you'll use:
 * - chrome.runtime.onMessage.addListener() - receive messages
 * - chrome.tabs.captureVisibleTab() - screenshot the page
 * - fetch() - call your Python backend at localhost:5000
 */

// TODO: Implement message handling
