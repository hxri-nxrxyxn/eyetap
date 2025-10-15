<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    // --- CAPACITOR CAMERA IMPORTS ---
    import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

    // --- STATE & CONFIG (Menu) ---
    const mainMenuItems = [
        { text: 'Greet', href: '/greet' },
        { text: 'X', href: null },
        { text: 'Help', href: '/help' }
    ];

    let selectedIndex = 0;
    let itemWidth = 0;
    let offset = 0;
    let menuItemElements = [];
    let activationTimer = null;

    // A flag to control our camera capture loop
    let isCameraActive = true;

    // --- CORE MENU FUNCTION ---
    function updateMainMenuSelector() {
        if (!menuItemElements[0] || menuItemElements[0].offsetWidth === 0) return;
        itemWidth = menuItemElements[0].offsetWidth;
        const middleIndex = Math.floor(mainMenuItems.length / 2);
        offset = (middleIndex - selectedIndex) * itemWidth;
    }

    function resetActivationTimer() {
        if (activationTimer) {
            clearTimeout(activationTimer);
        }
        console.log(`⏳ Starting 3s timer for "${mainMenuItems[selectedIndex].text}"`);
        activationTimer = setTimeout(() => {
            console.log(`✅ Timer finished! Activating "${mainMenuItems[selectedIndex].text}"`);
            activateSelected();
        }, 3000);
    }

    function moveLeft() {
        selectedIndex = (selectedIndex - 1 + mainMenuItems.length) % mainMenuItems.length;
        updateMainMenuSelector();
        resetActivationTimer();
    }

    function moveRight() {
        selectedIndex = (selectedIndex + 1) % mainMenuItems.length;
        updateMainMenuSelector();
        resetActivationTimer();
    }

    function activateSelected() {
        const selectedItem = mainMenuItems[selectedIndex];
        if (selectedItem.href) {
            goto(selectedItem.href);
        }
    }

    // --- KEYBOARD EVENT HANDLER ---
    function handleKeydown(e) {
        if (['ArrowLeft', 'ArrowRight', 'ArrowDown', 'Enter'].includes(e.key)) {
            e.preventDefault();
        }
        switch (e.key) {
            case 'ArrowRight': moveRight(); break;
            case 'ArrowLeft': moveLeft(); break;
        }
    }

    // --- MODIFIED LIFECYCLE HOOK ---
    onMount(() => {
        selectedIndex = Math.floor(mainMenuItems.length / 2);
        updateMainMenuSelector();
        resetActivationTimer();

        // --- CAPACITOR CAMERA & WEBSOCKET SETUP ---
        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const context = canvas.getContext("2d");

        const ws = new WebSocket("ws://192.168.14.127:8765");
        ws.onopen = () => console.log("✅ Connected to WebSocket server");
        ws.onclose = () => console.log("❌ Disconnected from server");
        ws.onmessage = (event) => {
            if (typeof event.data === "string") {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === "gaze_event") {
                        console.log("👁️ Gaze event:", data.direction);
                        switch (data.direction) {
                            case "signal_left": moveLeft(); break;
                            case "signal_right": moveRight(); break;
                            case "signal_center": break; // Do nothing
                        }
                    }
                } catch (err) {
                    console.error("Error parsing WebSocket message:", err);
                }
            }
        };

        const targetFPS = 15;
        const frameInterval = 1000 / targetFPS;

        // NEW: Function to capture frames using Capacitor Camera
        const captureAndSendFrame = async () => {
            try {
                // 1. Capture a photo using the device's front camera
                const photo = await Camera.getPhoto({
                    quality: 40, // Low quality for faster transfer
                    allowEditing: false,
                    resultType: CameraResultType.Base64, // Get image as a base64 string
                    source: CameraSource.Front, // Use the front camera
                    width: 640,
                    height: 480
                });

                if (!photo || !photo.base64String) return;

                // 2. Draw the captured image onto the canvas
                const image = new Image();
                // We need to wait for the image to load before drawing it
                await new Promise(resolve => {
                    image.onload = resolve;
                    image.src = `data:image/jpeg;base64,${photo.base64String}`;
                });
                context.drawImage(image, 0, 0, canvas.width, canvas.height);

                // 3. Send the canvas content over the WebSocket
                if (ws.readyState === WebSocket.OPEN) {
                    canvas.toBlob(blob => {
                        if (blob) {
                            ws.send(blob);
                        }
                    }, 'image/jpeg', 0.4);
                }

            } catch (error) {
                console.error("📸 Camera Error:", error);
                // Stop the loop if the user cancels or there's an error
                isCameraActive = false;
            }
        };


        // NEW: Main setup function
        const setupCamera = async () => {
            // 1. Check for camera permissions
            const permissions = await Camera.checkPermissions();
            if (permissions.camera !== 'granted') {
                const permissionResult = await Camera.requestPermissions();
                if (permissionResult.camera !== 'granted') {
                    console.error("Camera permission not granted.");
                    alert("Camera permission is required to use this feature.");
                    return;
                }
            }

            // 2. Start the frame capture loop
            while (isCameraActive) {
                const startTime = performance.now();
                await captureAndSendFrame();
                const endTime = performance.now();
                
                const processTime = endTime - startTime;
                const delay = Math.max(0, frameInterval - processTime);
                
                if(isCameraActive) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        };

        // Start the process
        setupCamera();

        // Cleanup
        return () => {
            console.log("🧹 Cleaning up...");
            isCameraActive = false; // Stop the camera loop
            if (activationTimer) {
                clearTimeout(activationTimer);
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