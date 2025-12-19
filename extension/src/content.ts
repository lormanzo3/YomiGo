/**
 * Content Script
 *
 * This is injected into every page and can:
 * - Access and modify the page DOM
 * - Create selection overlays for capturing regions
 * - Send messages to background script
 *
 * Key APIs you'll use:
 * - chrome.runtime.sendMessage() - send to background
 * - document.createElement() - create overlay UI
 * - canvas.toDataURL() - convert selections to base64
 */

// TODO: Implement region selection and capture
