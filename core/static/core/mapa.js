// Vue 3 Initialization for Level Map

const { createApp, ref } = Vue;

const mapApp = createApp({
    setup() {
        // State variables
        const currentPlayer = ref("Juan");
        const starsCollected = ref(15);
        const levelsCompleted = ref(3);
        const totalLevels = ref(16);
        const activeLetter = ref("B");

        // Methods
        const goBack = () => {
            console.log('Navigating back to main menu...');
            window.location.href = "/"; // Simulate back button returning to lobby
        };

        const continueLetter = () => {
            console.log(`Starting level for letter ${activeLetter.value}`);
            // Logic to launch the mini-game component
            alert("This will open the mini-game for letter B!");
        };

        return {
            currentPlayer,
            starsCollected,
            levelsCompleted,
            totalLevels,
            activeLetter,
            goBack,
            continueLetter
        };
    }
});

mapApp.mount('#map-app');
