<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const club = ref(null)

onMounted(async () => {
  const res = await fetch(`http://127.0.0.1:8000/clubs/clubs/${route.params.id}`)
  if (res.ok) {
    club.value = await res.json()
  }
})

function goToPlayers() {
  router.push(`/teams/${route.params.id}/players`)
}

function goToFinances() {
  router.push(`/clubs/${route.params.id}/finances`)
}
</script>

    
    <template>
  <div class="club-page">
    <div v-if="club" class="club-box">
      <div class="header">
        <img v-if="club.logo_url" :src="club.logo_url" class="logo" />
        <h1 class="title">{{ club.name }}</h1>
      </div>

      <p class="description">"{{ club.description }}"</p>

      <div class="details">
        <div><strong>League:</strong> {{ club.league }}</div>
        <div><strong>Manager:</strong> {{ club.manager_name || '—' }}</div>
        <div><strong>Founded:</strong> {{ club.founded_year || '—' }}</div>
        <div><strong>Stadium:</strong> {{ club.stadium_name || '—' }}</div>
        <div><strong>Trophies:</strong> 🏆 {{ club.trophies_won }}</div>
        <div><strong>Transfer Budget:</strong> 💰 €{{ club.transfer_budget.toLocaleString() }}</div>
        <div><strong>Wage Budget:</strong> 💸 €{{ club.wage_budget.toLocaleString() }}</div>
      </div>

      <button class="players-btn" @click="goToPlayers">
        View Players
      </button>

      <button class="players-btn" @click="goToFinances">
        View Finances
      </button>
    </div>

    <div v-else class="club-box">
      <p>Loading club data...</p>
    </div>
  </div>
</template>

      
    
    <style scoped>
    .club-page {
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #0D1117;
      padding: 6rem;
    }
    
    .club-box {
      background: #1f1f1f;
      border-radius: 48px;
      padding: 6rem 8rem;
      width: 100%;
      max-width: 1600px;
      box-shadow: 0 0 90px rgba(0, 0, 0, 0.7);
      color: #ffffff;
      text-align: center;
    }
    
    .header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2.5rem;
      margin-bottom: 2.5rem;
    }
    
    .logo {
      width: 120px;
      height: 120px;
      object-fit: contain;
      background: white;
      border-radius: 20px;
      padding: 0.5rem;
    }
    
    .title {
      font-size: 5.5rem;
      color: #ffcc66;
      margin: 0;
    }
    
    .description {
      font-size: 2.2rem;
      color: #cccccc;
      margin-bottom: 4rem;
    }
    
    .details {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      font-size: 2rem;
      gap: 2rem;
      margin-bottom: 3rem;
      text-align: left;
    }
    
    .players-btn {
  background: #ffcc66;
  color: #1f1f1f;
  font-size: 2rem;
  font-weight: bold;
  border: none;
  border-radius: 24px;
  padding: 1.6rem;
  width: 100%;
  max-width: 100%;
  margin-top: 3rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.players-btn:hover {
  background: #e6b84d;
}

    
    .squad {
      list-style: none;
      padding: 0;
      font-size: 1.9rem;
      text-align: left;
      margin-top: 2rem;
    }
    
    .squad li {
      padding: 1rem 0;
      border-bottom: 1px solid #333;
    }
    </style>
    