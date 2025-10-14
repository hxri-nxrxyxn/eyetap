<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'; // SvelteKit's programmatic navigation

    // --- STATE & CONFIG ---
    // The menu items are updated, and links are converted to SvelteKit paths
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

    // --- DOM ELEMENT REFERENCES (Svelte's `bind:this`) ---
    let menuItemElements = [];

    // --- CORE FUNCTION ---
    // This function calculates the necessary offset to center the selected item.
    function updateMainMenuSelector() {
        // Ensure the element has been rendered and has a width
        if (!menuItemElements[0] || menuItemElements[0].offsetWidth === 0) return;

        itemWidth = menuItemElements[0].offsetWidth;
        const middleIndex = Math.floor(mainMenuItems.length / 2);
        offset = (middleIndex - selectedIndex) * itemWidth;
    }
    
    // --- KEYBOARD EVENT HANDLER ---
    function handleKeydown(e) {
        // Prevent default browser actions for navigation keys
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
                // Navigate if the selected item has a link
                if (selectedItem.href) {
                    goto(selectedItem.href);
                }
                break;
            // The 'Enter' case remains empty as in the original code.
        }
        updateMainMenuSelector();
    }

    // --- LIFECYCLE & REACTIVITY ---
    // onMount is Svelte's equivalent of window.onload
    onMount(() => {
        selectedIndex = Math.floor(mainMenuItems.length / 2);
        updateMainMenuSelector();
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