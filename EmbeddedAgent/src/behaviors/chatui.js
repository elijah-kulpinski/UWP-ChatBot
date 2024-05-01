/**
 * Controls the behavior of the chat UI, scrolling, button toggling, and advanced settings popup window.
 * 
 * @author Christopher Mata
 */

// GitHub popup menu to keep track of the state
let githubMenu = null; 

/**
 * Toggles the chat UI on and off. And makes sure that everything is cloesed when the website is initially loaded.
 */
function toggleChat() {
    var chatBox = document.querySelector('.chatui');
    chatBox.style.display = (chatBox.style.display === 'none' || chatBox.style.display === '') ? 'block' : 'none';

    // Close GitHub popup when chat is toggled
    closeGitHubPopup();
}

/**
 * Updates the chat box position on scroll.
 * This function is called every time the user scrolls the page. It ensures that the chat UI remains at the bottom of the page.
 * It also updates the position of elements when the user scrolls.
 */
window.addEventListener('scroll', function () {
    var chatBox = document.querySelector('.chatui');
    var githubButton = document.getElementById('github-link-btn');
    var githubButtonRect = githubButton.getBoundingClientRect();

    chatBox.style.bottom = '50px'; // Ensure it stays at the bottom
    chatBox.style.top = ''; // Remove top positioning

    // Close GitHub popup when user scrolls
    if (githubMenu) {
        // Check if the GitHub button is in the view
        if (githubButtonRect.top > window.innerHeight || githubButtonRect.bottom < 0) {
            closeGitHubPopup();
        }
    }
});

/**
 * Toggels and sets the properties of the advanced settings popup window.
 * It also throws an event that is caught by simple_chat.ts
 * 
 * @returns exits the function to not waste resources
 */
function openGitHubPopup() {
    // Check if the menu is already open and close it
    if (githubMenu) {
        closeGitHubPopup();
        return;
    }

    // Create a menu for inserting a GitHub link
    githubMenu = document.createElement('div');
    githubMenu.className = 'github-menu';

    // Add text above the input field and submit button
    const infoText = document.createElement('p');
    infoText.textContent = 'Follow the instructions on https://llm.mlc.ai/docs/deploy/javascript.html ' + 
        ' Refresh before adding a model. Scroll to the subtitle "Bring Your Own Model" and follow the instructions untill you finish step 3.' +
        ' Copy the link you generate and paste it. MAKE SURE YOU NAME GITHUB REPOSITORY CONTAINING THE WORDS "Mistral-7B" and that it ends in .wasm' +
        ' If something messes up, please refresh the page and try the process again. Please base the model off of Mistral-7B-Instruct!';
    infoText.style.color = 'white'; // Set text color to white
    githubMenu.appendChild(infoText);
    
    // Input field for GitHub link
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Enter GitHub link';
    
    // Button to submit the GitHub link
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.onclick = function() {
        const githubLink = inputField.value;
        // Handle the GitHub link, you can replace the alert with your logic
        const event = new CustomEvent('githubLinkSubmitted', { detail: githubLink });
        document.dispatchEvent(event);
        // Close the menu
        closeGitHubPopup();
    };
    
    // Append elements to the menu
    githubMenu.appendChild(inputField);
    githubMenu.appendChild(submitButton);

    // Get the position of the GitHub button
    const githubButton = document.getElementById('github-link-btn');
    const buttonRect = githubButton.getBoundingClientRect();

    // Set the position and styling of the menu
    githubMenu.style.position = 'fixed';
    githubMenu.style.top = buttonRect.bottom + 'px';
    githubMenu.style.left = buttonRect.left + 'px';

    // Append the menu to the body
    document.body.appendChild(githubMenu);
}

/**
 * Closes the GitHub popup menu.
 */
function closeGitHubPopup() {
    if (githubMenu) {
        githubMenu.remove();
        githubMenu = null; // Reset the variable
    }
}

// Update GitHub popup position on window resize
window.addEventListener('resize', function () {
    if (githubMenu) {
        // Get the position of the GitHub button
        const githubButton = document.getElementById('github-link-btn');
        const buttonRect = githubButton.getBoundingClientRect();

        // Set the position of the menu
        githubMenu.style.top = buttonRect.bottom + 'px';
        githubMenu.style.left = buttonRect.left + 'px';
    }
});