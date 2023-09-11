class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];

    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input')
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })

        let msg0 = {name: "Ren", message: "Hello! How may I help you today?"}
        this.messages.push(msg0)
        this.updateChatText(chatBox)
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = {name: "User", message: text1}
        this.messages.push(msg1)
        this.updateChatText(chatbox)
        textField.value = ''

        fetch($SCRIPT_ROOT + '/chat', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = {name: "Ren", message: r.answer};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    updateChatText(chatbox) {

        var html = '';
        this.messages.slice().reverse().forEach(function(item) {
            if (item.name === "Ren")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

    }

    setupResize() {
        let startX, startY, startWidth, startHeight;
    
        // Helper function to disable text selection
        const disableTextSelection = () => {
            document.body.style.userSelect = 'none';
        };
    
        // Helper function to re-enable text selection
        const enableTextSelection = () => {
            document.body.style.userSelect = '';
        };
    
        // Create the resizing handle
        const resizeHandle = document.createElement('div');
        resizeHandle.style.width = '10px';
        resizeHandle.style.height = '10px';
        resizeHandle.style.background = 'black';
        resizeHandle.style.position = 'absolute';
        resizeHandle.style.top = '0';
        resizeHandle.style.left = '0';
        resizeHandle.style.cursor = 'nw-resize';
        this.args.chatBox.appendChild(resizeHandle);
    
        let animationFrameId;

        const onMouseMove = (event) => {
            if (!this.resizing) return;
        
            // Cancel the previous frame to avoid stacking
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        
            animationFrameId = requestAnimationFrame(() => {
                const dx = startX - event.clientX;
                const dy = startY - event.clientY;
        
                const newWidth = startWidth + dx;
                const newHeight = startHeight + dy;
        
                // Define minimum and maximum dimensions
                const minWidth = 300;
                const minHeight = 300;
                const maxWidth = 800;
                const maxHeight = 800;
        
                // Batch style changes to reduce reflows
                const styles = {};
        
                if (newWidth >= minWidth && newWidth <= maxWidth) {
                    styles.width = `${newWidth}px`;
                }
                if (newHeight >= minHeight && newHeight <= maxHeight) {
                    styles.height = `${newHeight}px`;
                }
        
                // Apply the styles in one go
                Object.assign(this.args.chatBox.style, styles);
            });
        };        
    
        const onMouseUp = () => {
            this.resizing = false;
            enableTextSelection();  // Re-enable text selection
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        };
    
        resizeHandle.addEventListener('mousedown', (event) => {
            this.resizing = true;
    
            disableTextSelection();  // Disable text selection
    
            startX = event.clientX;
            startY = event.clientY;
            startWidth = this.args.chatBox.offsetWidth;
            startHeight = this.args.chatBox.offsetHeight;
    
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }    
}

const chatbox = new Chatbox();
chatbox.display();
chatbox.setupResize();