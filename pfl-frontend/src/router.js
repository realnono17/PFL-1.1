import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue"; // Homepage
import Players from "@/views/Players.vue"; // List of players
import PlayerOverview from "@/views/PlayerOverview.vue"; // Player details page
import Teams from "@/views/Teams.vue"; // Teams page
import ClubOverview from "@/views/ClubOverview.vue";
import ClubPlayers from "@/views/ClubPlayers.vue";
import ClubFinances from "@/views/ClubFinances.vue";
import NotFound from "@/views/NotFound.vue"; // Optional: 404 Page

const routes = [
  { path: "/", component: Home },
  { path: "/players", component: Players },
  { path: "/players/:id", component: PlayerOverview, props: true },
  { path: "/clubs/:id", component: ClubOverview, props: true },
  { path: '/teams/:id/players', component: ClubPlayers, props: true },
  { path: "/teams", component: Teams },  // Added teams route
  { path: "/clubs/:id/finances", component: ClubFinances },
  { path: "/:pathMatch(.*)*", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
