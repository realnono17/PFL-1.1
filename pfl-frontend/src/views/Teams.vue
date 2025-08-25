<template>
  <div class="teams-page">
    <!-- Box for PFL1 -->
    <div class="floating-box">
      <h1 class="page-title">PFL1 (10 Teams)</h1>
      <div class="team-grid">
        <router-link
          v-for="team in pfl1Teams"
          :key="team.id"
          :to="'/clubs/' + team.id"
          class="team-cell"
        >
          <span class="team-number">{{ team.id.toString().padStart(2, '0') }}</span>
          <span class="team-name">{{ team.name }}</span>
        </router-link>
      </div>
    </div>

    <!-- Box for PFL2 -->
    <div class="floating-box">
      <h1 class="page-title">PFL2 (10 Teams)</h1>
      <div class="team-grid">
        <router-link
          v-for="team in pfl2Teams"
          :key="team.id"
          :to="'/clubs/' + team.id"
          class="team-cell"
        >
          <span class="team-number">{{ team.id.toString().padStart(2, '0') }}</span>
          <span class="team-name">{{ team.name }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Teams",
  data() {
    return {
      // PFL1 teams
      pfl1Teams: [
        { id: 1,  name: "Blackbeard Strikers" },
        { id: 2,  name: "Ghost Ship Raiders" },
        { id: 3,  name: "Kraken FC" },
        { id: 4,  name: "Storm Reapers" },
        { id: 5,  name: "Corsair Warriors" },
        { id: 6,  name: "Dreadnoughts" },
        { id: 7,  name: "Buccaneer Brigade" },
        { id: 8,  name: "Seadog United" },
        { id: 9,  name: "Marauder Mariners" },
        { id: 10, name: "Plunder Pioneers" },
      ],
      // PFL2 teams
      pfl2Teams: [
        { id: 11, name: "Sea Wolves" },
        { id: 12, name: "Rogue Buccaneers" },
        { id: 13, name: "War Reavers" },
        { id: 14, name: "Tempest Titans" },
        { id: 15, name: "Leviathan Legends" },
        { id: 16, name: "Ocean Outlaws" },
        { id: 17, name: "Wave Warriors" },
        { id: 18, name: "Coral Crusaders" },
        { id: 19, name: "Deepwater Drifters" },
        { id: 20, name: "Maritime Marauders" },
      ],
    };
  },
};
</script>

<style scoped>
.teams-page {
  /* Centers both floating boxes horizontally, with some gap between them */
  min-height: 100vh;
  display: flex;
  gap: 4rem;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  overflow-y: hidden; /* Added to prevent vertical scrolling */
}

.floating-box {
  background-color: #2a2a2a;
  border-radius: 40px;
  padding: 6rem;
  width: 100%;
  max-width: 2400px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.4);
  text-align: center;
}

.page-title {
  text-align: center;
  color: #ffcc66;
  font-size: 4.5rem;
  margin-bottom: 4.5rem;
  letter-spacing: 1px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(2, auto);
  gap: 1rem;
}

.team-cell {
  background-color: #1f1f1f;
  padding: 2rem;
  border-radius: 16px;
  color: #f0f0f0;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: background 0.3s;
}

.team-cell:hover {
  background-color: #1f1f1f;
}

.team-number {
  font-size: 2.8rem;
  color: #3498db;
  font-weight: bold;
  margin-bottom: 1rem;
}

.team-name {
  text-align: center;
  font-size: 2.4rem;
}

@media (max-width: 1024px) {
  .floating-box {
    padding: 3rem;
    border-radius: 20px;
  }
}

@media (max-width: 2400px) {
  .page-title {
    font-size: 3rem;
  }
  .team-number {
    font-size: 1.9rem;
  }
  .team-name {
    font-size: 1.6rem;
  }
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
  .team-cell {
    padding: 1.2rem;
  }
}
</style>