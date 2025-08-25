<template>
  <main class="container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <img class="hero-image" :src="heroImage" alt="Pirate Football" />
        <h1>Pirate Football League ⚓</h1>
        <p class="subheading">
          Lead your crew, master your tactics, and rule the seas of football!
        </p>
        <div class="cta-buttons">
          <router-link to="/login" class="cta-button">⚓ Join the Crew</router-link>
          <router-link to="/discord" class="discord-button">
            <img class="discord-icon" :src="discordIcon" alt="Discord" />
            Discord
          </router-link>
        </div>
      </div>
    </section>

    <!-- Unique Selling Points -->
    <section class="usp">
      <h2>🔥 Why Join PFL?</h2>
      <div class="usp-container">
        <article class="usp-item" v-for="(usp, index) in uspList" :key="index">
          <h3>{{ usp.icon }} {{ usp.title }}</h3>
          <p>{{ usp.description }}</p>
        </article>
      </div>
    </section>

    <!-- League Overview -->
    <section class="league-overview">
      <div class="grid">
        <!-- PFL 1 Standings -->
        <article class="league-card">
          <h2>🏆 PFL 1 Standings</h2>
          <ul>
            <li v-for="(team, index) in pfl1Standings" :key="team.club_id">
              <span class="rank">{{ index + 1 }}</span>
              <span class="team-name">{{ team.club_name }}</span>
              <span class="points">{{ team.points }} pts</span>
            </li>
          </ul>
        </article>

        <!-- PFL 2 Standings -->
        <article class="league-card">
          <h2>🏆 PFL 2 Standings</h2>
          <ul>
            <li v-for="(team, index) in pfl2Standings" :key="team.club_id">
              <span class="rank">{{ index + 1 }}</span>
              <span class="team-name">{{ team.club_name }}</span>
              <span class="points">{{ team.points }} pts</span>
            </li>
          </ul>
        </article>

        <!-- Match Calendar -->
        <article class="league-card">
          <h2>📅 Match Calendar</h2>
          <ul>
            <template v-for="(match, index) in matchCalendar" :key="match.id">
              <hr v-if="index === 5" class="calendar-separator" />
              <li>
                <span class="match-date">Matchday {{ match.matchday_number }}</span>
                <span class="match-teams">{{ match.home_club_name }} vs {{ match.away_club_name }}</span>
                <span class="match-status">{{ match.status }}</span>
              </li>
            </template>
          </ul>
        </article>
      </div>
    </section>
  </main>
</template>

<script>
import axios from "axios";
import heroImage from "@/assets/hero.png";
import discordIcon from "@/assets/discord.png";

export default {
  data() {
    return {
      heroImage,
      discordIcon,
      pfl1Standings: [],
      pfl2Standings: [],
      matchCalendar: [],
      uspList: [
        { icon: "⚔️", title: "Tactical Warfare", description: "Build strategies, set formations, and outthink rival captains." },
        { icon: "🏴‍☠️", title: "Fully Automated League", description: "The game runs itself—so you focus on managing, not admin work." },
        { icon: "📺", title: "Live Match Simulations", description: "Watch your tactics play out in **real-time** on Twitch!" },
        { icon: "💰", title: "Finance & Transfers", description: "Manage your budget, sign new players, and build your legacy." },
        { icon: "⚡", title: "Player Data & Statistics", description: "Keep track of player performances through detailed game statistics." },
        { icon: "🎭", title: "Legendary Customization", description: "Design your club, choose your crest, and leave a legacy." },
      ]
    };
  },
  async mounted() {
    const base = import.meta.env.VITE_API_URL || "http://localhost:8000";

    try {
      const [pfl1Res, pfl2Res, matchRes] = await Promise.all([
        axios.get("/league-standings/competition/1"),
        axios.get("/league-standings/competition/2"),
        axios.get("/matches/upcoming")
      ]);

      this.pfl1Standings = pfl1Res.data;
      this.pfl2Standings = pfl2Res.data;
      this.matchCalendar = matchRes.data.map(m => ({
        ...m,
        status: m.home_score !== null ? `${m.home_score} - ${m.away_score}` : "Upcoming"
      }));

    } catch (error) {
      console.error("Failed to load homepage data:", error);
    }
  }
};
</script>

<style scoped>
/* HERO SECTION (scaled to 1.5× original) */
.hero {
  text-align: center;
  padding: 4.5rem 1.5rem 3rem;
  gap: 1.5rem;
}
.hero-content {
  max-width: 1800px;
  margin: 0 auto;
}
.hero-image {
  max-width: 25%;
  height: auto;
  margin-bottom: 2rem;
}
.hero h1 {
  font-size: 7.95rem; /* ~8rem */
  font-weight: 700;
  margin: 0;
  color: #ffcc66;
}
.subheading {
  font-size: 4.05rem; /* ~4rem */
  white-space: nowrap;
  margin: 0 auto;
  color: #ffffff;
}
.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
}
.cta-button,
.discord-button {
  display: inline-block;
  padding: 45px 90px;
  text-decoration: none;
  border-radius: 5px;
  font-size: 3.375rem; /* ~3.4rem */
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.cta-button {
  background-color: #ffcc66;
  color: #161b22;
}
.cta-button:hover {
  background-color: #e6b84f;
}
.discord-button {
  background-color: #7289da;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.discord-button:hover {
  background-color: #5b6eae;
}
.discord-icon {
  height: 4rem;
  margin-right: 1rem;
}

/* USP SECTION (1×6 horizontal row, wider) */
.usp {
  text-align: center;
  padding: 2rem 1rem;
}
.usp h2 {
  font-size: 6rem;
  color: #ffcc66;
  margin-bottom: 2rem;
}
.usp-container {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  justify-content: center;
  flex-wrap: nowrap;
  max-width: 1800px;
  margin: 0 auto;
}
.usp-item {
  flex: 1;
  background: #161b22;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(255, 204, 102, 0.5);
  box-sizing: border-box;
  min-width: 600px;
}
.usp-item h3 {
  font-size: 3.6rem;
  margin-bottom: 1rem;
  color: #ffcc66;
}
.usp-item p {
  font-size: 2.6rem;
  color: #ffffff;
  line-height: 1.4;
  margin: 0;
}

/* LEAGUE OVERVIEW (adapted to same width as USP section) */
.league-overview {
  padding: 4rem 2rem;
}
.grid {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 1800px;
  margin: 0 auto;
}
.league-card {
  background: #161b22;
  padding: 2rem;
  border-radius: 12px;
  width: 30%;
  min-height: 400px;
  box-shadow: 0 0 10px rgba(255, 204, 102, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.league-card h2 {
  font-size: 3rem;
  color: #ffcc66;
  text-align: center;
  margin-bottom: 1rem;
}
.league-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.league-card li {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #444;
  font-size: 2rem;
}
.rank {
  font-weight: bold;
  color: #ffcc66;
}
.team-name {
  flex-grow: 1;
  text-align: left;
  margin-left: 20px;
  color: #fff;
}
.points {
  font-weight: bold;
  color: #fff;
}
.match-date {
  font-weight: bold;
  color: #ffcc66;
  font-size: 2rem;
}
.match-teams {
  flex-grow: 1;
  text-align: center;
  color: #fff;
  font-size: 2rem;
}
.match-status {
  font-weight: bold;
  color: #fff;
  font-size: 2rem;
}

/* CALENDAR SEPARATOR */
.calendar-separator {
  border: none;
  border-top: 2px dashed #444;
  margin: 1rem 0;
}
</style>
