// Vue 3 Initialization for K_MALABAN App

const { createApp, ref } = Vue;

const app = createApp({
    setup() {
        // State variables can be added here
        // const isPlaying = ref(false);

        // Methods
        const playGame = () => {
            console.log('Navigating to Map Level Select...');
            window.location.href = "/mapa/";
        };

        const signIn = () => {
            console.log('Vue Action Triggered: Mag-sign In');
            // Add auth logic here
        };

        const showHelp = () => {
            console.log('Vue Action Triggered: Tulong / Help');
            // Add help modal rendering logic here
        };

        return {
            playGame,
            signIn,
            showHelp
        };
    }
});

// Mount the app to the #app div in index.html
app.mount('#app');
