<script>
	import { onMount } from 'svelte';

	let selectedIndex = 0;
	let menuVisible = true;
	let greetingText = '';
	let showGreeting = false;

	const menuItems = [
		{ text: 'Hi', greeting: 'Hi' },
		{ text: 'Good Morning', greeting: 'Good morning' },
		{ text: 'X', link: 'index.html' },
		{ text: 'Hello', greeting: 'Hello' },
		{ text: 'Bye', greeting: 'Bye' }
	];

	let itemWidth = 0;
	let optionContainer;

	function updateMenuSelector() {
		if (!optionContainer) return;

		const middleIndex = Math.floor(menuItems.length / 2);
		const offset = (middleIndex - selectedIndex) * itemWidth;
		optionContainer.style.transform = `translateX(${offset}px)`;
	}

	function handleKeyDown(e) {
		if (['ArrowLeft', 'ArrowRight', 'Enter', 'ArrowDown'].includes(e.key)) {
			e.preventDefault();
		}

		switch (e.key) {
			case 'ArrowRight':
				selectedIndex = (selectedIndex + 1) % menuItems.length;
				updateMenuSelector();
				break;

			case 'ArrowLeft':
				selectedIndex = (selectedIndex - 1 + menuItems.length) % menuItems.length;
				updateMenuSelector();
				break;

			case 'ArrowDown':
				const selectedItem = menuItems[selectedIndex];

				if (selectedItem.greeting) {
					menuVisible = false;
					greetingText = selectedItem.greeting;
					showGreeting = true;

					setTimeout(() => {
						window.location.href = 'index.html';
					}, 3000);
				} else if (selectedItem.link) {
					window.location.href = selectedItem.link;
				}
				break;

			case 'Enter':
				// Do nothing
				break;
		}
	}

	onMount(() => {
		selectedIndex = Math.floor(menuItems.length / 2);
		
		// Get item width after DOM is ready
		const firstItem = document.querySelector('.menu-option');
		if (firstItem) {
			itemWidth = firstItem.offsetWidth;
			updateMenuSelector();
		}

		window.addEventListener('keydown', handleKeyDown);
		window.addEventListener('resize', updateMenuSelector);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('resize', updateMenuSelector);
		};
	});
</script>

<svelte:window on:resize={updateMenuSelector} />

{#if menuVisible}
	<div class="main-menu">
		<div class="main-menu__container">
			<div class="main-menu__selector-circle"></div>
			<div class="main-menu__options-container" bind:this={optionContainer}>
				{#each menuItems as item, index}
					<div
						class="main-menu__option"
						class:main-menu__option--is-active={index === selectedIndex}
					>
						{#if item.link}
							<a href={item.link}>{item.text}</a>
						{:else}
							{item.text}
						{/if}
					</div>
				{/each}
			</div>
		</div>
	</div>
{/if}

{#if showGreeting}
	<div class="greeting-message">
		{greetingText}
	</div>
{/if}

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background-color: #000;
		color: white;
		font-family: sans-serif;
	}

	.main-menu {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100vh;
	}

	.main-menu__container {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.main-menu__selector-circle {
		position: absolute;
		width: 60px;
		height: 60px;
		border: 3px solid white;
		border-radius: 50%;
		pointer-events: none;
		z-index: 10;
	}

	.main-menu__options-container {
		display: flex;
		gap: 40px;
		transition: transform 0.3s ease-out;
	}

	.main-menu__option {
		width: 120px;
		height: 120px;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.2rem;
		font-weight: bold;
		text-transform: uppercase;
		opacity: 0.5;
		transition: opacity 0.2s;
	}

	.main-menu__option--is-active {
		opacity: 1;
	}

	.main-menu__option a {
		color: inherit;
		text-decoration: none;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
	}

	.greeting-message {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		color: white;
		font-size: 5rem;
		font-weight: bold;
		text-transform: uppercase;
		background-color: #000;
		z-index: 1000;
	}
</style>