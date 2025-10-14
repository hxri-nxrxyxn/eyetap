<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    // --- STATE & CONFIG (Menu) ---
    const mainMenuItems = [
        { text: 'Food', href: '/food' },
        { text: 'Greet', href: '/greet' },
        { text: 'X', href: null },
        { text: 'Help', href: '/help' },
        { text: 'Binge', href: '/binge' }
    ];

    let selectedIndex = 0;
    let itemWidth = 0;
    let offset = 0;

    // --- DOM ELEMENT REFERENCES ---
    let menuItemElements = [];

    // --- CORE MENU FUNCTION ---
    function updateMainMenuSelector() {
        if (!menuItemElements[0] || menuItemElements[0].offsetWidth === 0) return;
        itemWidth = menuItemElements[0].offsetWidth;
        const middleIndex = Math.floor(mainMenuItems.length / 2);
        offset = (middleIndex - selectedIndex) * itemWidth;
    }
    
    // --- KEYBOARD EVENT HANDLER (Menu) ---
    function handleKeydown(e) {
        if (['ArrowLeft', 'ArrowRight', 'ArrowDown', 'Enter'].includes(e.key)) {
            e.preventDefault();
        }

        switch (e.key) {
            case 'ArrowRight':
                selectedIndex = (selectedIndex + 1) % mainMenuItems.length;
                break;
            case 'ArrowLeft':
                selectedIndex = (selectedIndex - 1 + mainMenuItems.length) % mainMenuItems.length;
                break;
            case 'ArrowDown':
                const selectedItem = mainMenuItems[selectedIndex];
                if (selectedItem.href) {
                    goto(selectedItem.href);
                }
                break;
        }
        updateMainMenuSelector();
    }

    // --- LIFECYCLE HOOK ---
    onMount(() => {
        // Initialize the main menu
        selectedIndex = Math.floor(mainMenuItems.length / 2);
        updateMainMenuSelector();

        // ---- START: Background Webcam and WebSocket Logic ----
        
        // 1. Create video and canvas elements in memory
        const video = document.createElement('video');
        video.width = 640;
        video.height = 480;
        video.autoplay = true;
        video.muted = true;

        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const context = canvas.getContext("2d");

        // 2. Connect to WebSocket server
        const ws = new WebSocket("ws://localhost:8765");
        let mediaStream = null;

        ws.onopen = () => console.log("Connected to WebSocket server");
        ws.onclose = () => console.log("Disconnected from server");

        // 3. Get webcam stream
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(stream => {
                mediaStream = stream;
                video.srcObject = stream;
                video.play();

                // 4. Capture and send frames periodically
                const sendFrame = () => {
                    if (!mediaStream?.active) return;

                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    if (ws.readyState === WebSocket.OPEN) {
                        // --- MODIFICATION START ---

                        // OLD: Convert to Base64 string
                        // const dataURL = canvas.toDataURL("image/jpeg");
                        // const base64Data = dataURL.split(",")[1];
                        // ws.send(base64Data);

                        // NEW: Convert to binary Blob and send
                        // canvas.toBlob() is asynchronous. The sending logic happens in the callback.
                        canvas.toBlob(blob => {
                            if (blob) {
                                ws.send(blob);
                            }
                        }, 'image/jpeg', 0.8); // 0.8 is the quality (0.0 to 1.0)
                        
                        // --- MODIFICATION END ---
                    }
                    requestAnimationFrame(sendFrame);
                };
                sendFrame();
            })
            .catch(err => {
                console.error("Error accessing webcam:", err);
            });
            
        // 5. Cleanup function
        return () => {
            console.log("Component unmounting: Cleaning up resources.");
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
            }
            if (ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
        };
    });
</script>

<svelte:window on:keydown={handleKeydown} on:resize={updateMainMenuSelector} />

<div class="main-menu">
    <div class="main-menu__container">
        <div class="main-menu__selector-circle"></div>
        <div class="main-menu__options-container" style="transform: translateX({offset}px);">
            {#each mainMenuItems as item, index}
                <div
                    class="main-menu__option"
                    bind:this={menuItemElements[index]}
                    class:main-menu__option--is-active={index === selectedIndex}
                >
                    {#if item.href}
                        <a href={item.href}>{item.text}</a>
                    {:else}
                        {item.text}
                    {/if}
                </div>
            {/each}
        </div>
    </div>
</div>