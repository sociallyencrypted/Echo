

function appendMessage(sender, text, messageType) {
  const messageContainer = document.createElement('div');
  messageContainer.classList.add('message-container', messageType);

  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.textContent = text;

  messageContainer.appendChild(messageElement);
  chatMessages.appendChild(messageContainer);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
