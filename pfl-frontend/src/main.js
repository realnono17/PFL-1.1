import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // ✅ Ensure this is correct
import "./style.css";

const app = createApp(App);
app.use(router); // ✅ Attach router

// 🚀 Confirm Router is Loaded
router.isReady().then(() => {
  console.log("✅ Vue Router is READY!");
});

app.mount("#app");

console.log("✅ Vue App Loaded!");
