<script>
    import { goto } from '$app/navigation';

    /**
     * Handles keydown events on the window.
     * Navigates to the home page if the ArrowDown key is pressed.
     * @param {KeyboardEvent} e - The keyboard event object.
     */
    function handleKeydown(e) {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            // Use SvelteKit's goto for client-side navigation
            goto('/');
        }
    }
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="calling-screen">
    <div>
        <div class="calling-text">Calling</div>
        <div class="exit-button">X</div>
    </div>
</div>

<style>
    /*
      These styles are moved from the `body` tag to a wrapper div
      to make the component self-contained and avoid global styles.
    */
    .calling-screen {
        width: 100vw;
        height: 100vh;
        background-color: darkred;
        color: white;
        display: grid;
        place-content: center;
        font-family: sans-serif;
        text-align: center;
    }

    .calling-text {
        font-size: 12vw;
        font-weight: bold;
        text-transform: uppercase;
        animation: pulse 1.5s infinite ease-in-out;
    }

    .exit-button {
        font-size: 4vw;
        font-weight: bold;
        margin-top: 4rem;
        color: #ffffff33;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>