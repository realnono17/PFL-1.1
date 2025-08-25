<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    
    const route = useRoute()
    const router = useRouter()
    
    const logs = ref([])
    const club = ref(null)
    
    const rawClubId = route.params.id
    const clubId = parseInt(Array.isArray(rawClubId) ? rawClubId[0] : rawClubId || '0', 10)
    
    onMounted(async () => {
      const [clubRes, logsRes] = await Promise.all([
        fetch(`http://127.0.0.1:8000/clubs/clubs/${clubId}`),
        fetch(`http://127.0.0.1:8000/logs/club/${clubId}`)
      ])
    
      if (clubRes.ok) club.value = await clubRes.json()
      if (logsRes.ok) logs.value = await logsRes.json()
    })
    
    function goBack() {
      router.push(`/clubs/${clubId}`)
    }
    </script>
    
    <template>
      <div class="finance-page">
        <div class="finance-box">
          <h1>💼 Club Finances</h1>
    
          <div v-if="club" class="budget-info">
            <p><strong>Transfer Budget:</strong> 💰 €{{ club.transfer_budget.toLocaleString() }}</p>
            <p><strong>Wage Budget:</strong> 💸 €{{ club.wage_budget.toLocaleString() }}</p>
          </div>
    
          <div v-if="logs.length">
            <div v-for="log in logs" :key="log.id" class="log-entry">
              <div class="log-header">
                <span class="timestamp">
                  {{ log.timestamp ? new Date(log.timestamp).toLocaleString() : '—' }}
                </span>
                <span
                  class="amount"
                  :class="{ income: log.amount > 0, expense: log.amount < 0 }"
                >
                  €{{ log.amount.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 }) }}
                </span>
              </div>
              <div class="log-meta">
                <span class="type">{{ log.type }}</span>
                <span class="desc">{{ log.description }}</span>
              </div>
            </div>
          </div>
          <p v-else>No financial logs found for this club.</p>
        </div>
    
        <a class="back-link" @click="goBack">← Back to Club</a>
      </div>
    </template>
    
    <style scoped>
    .finance-page {
  min-height: 100vh;
  background: #0D1117;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 6rem 2rem;
}

.finance-box {
  background: #1f1f1f;
  border-radius: 32px;
  padding: 6rem 8rem; /* Increased padding */
  width: 100%;
  max-width: 1200px; /* Wider box */
  color: #ffffff;
  box-shadow: 0 0 90px rgba(0, 0, 0, 0.65);
}

h1 {
  font-size: 4rem; /* Bigger title */
  margin-bottom: 1.5rem;
  color: #ffcc66;
}

.budget-info {
  font-size: 2rem;
  color: #ccc;
  margin-bottom: 3rem;
  text-align: left;
  line-height: 1.6;
}

.back-link {
  display: inline-block;
  margin-top: 5rem;
  color: #a379ff;
  font-size: 1.9rem;
  cursor: pointer;
  text-decoration: none;
}

.back-link:hover {
  color: #c2a3ff;
}

.log-entry {
  border-bottom: 1px solid #333;
  padding: 2rem 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 2rem;
  margin-bottom: 0.7rem;
}

.timestamp {
  color: #ccc;
}

.amount {
  font-weight: bold;
}

.income {
  color: #4ade80;
}

.expense {
  color: #f87171;
}

.log-meta {
  font-size: 1.8rem;
  color: #aaa;
  display: flex;
  gap: 1.5rem;
}

.type {
  background: #333;
  padding: 0.4rem 1.2rem;
  border-radius: 12px;
  color: #ffcc66;
  font-weight: bold;
}

.desc {
  color: #999;
  font-style: italic;
}

    </style>