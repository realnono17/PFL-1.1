<template>
  <div class="player-profile">
    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading player profile...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <h2>Error loading player</h2>
      <p>{{ error }}</p>
      <router-link to="/players" class="back-link">← Back to Players</router-link>
    </div>

    <!-- Player loaded -->
    <div v-else-if="player" class="profile-content">
      <!-- Back navigation -->
      <router-link to="/players" class="back-link">← Back to Players</router-link>

      <!-- Hero card -->
      <div class="hero-card">
        <div class="player-photo">
          <img
            :src="playerPhoto"
            :alt="player.name"
            @error="handleImageError"
          />
        </div>
        <div class="player-info">
          <h1 class="player-name">{{ player.name }}</h1>
          <div class="ovr-badge">{{ player.overall_stats }}</div>
          <div class="meta-grid">
            <div class="meta-item">
              <span class="label">Nationality</span>
              <span class="value">{{ player.country_name || player.country }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Age</span>
              <span class="value">{{ player.age }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Club</span>
              <span class="value">{{ player.club_name || 'Unattached' }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Height</span>
              <span class="value">{{ player.height }} cm</span>
            </div>
            <div class="meta-item">
              <span class="label">Weight</span>
              <span class="value">{{ player.weight }} kg</span>
            </div>
            <div class="meta-item">
              <span class="label">Foot</span>
              <span class="value">{{ player.foot?.toUpperCase() }}</span>
            </div>
          </div>
          <div class="financials">
            <div v-if="player.market_value" class="finance-item">
              <span class="label">Market Value</span>
              <span class="value">{{ formatCurrency(player.market_value) }}</span>
            </div>
            <div v-if="player.wage" class="finance-item">
              <span class="label">Wage</span>
              <span class="value">{{ formatCurrency(player.wage) }}/w</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Attribute categories -->
      <div class="attributes-section">
        <h2>Attributes</h2>
        <div class="categories-grid">
          <div v-for="(cat, index) in attributeCategories" :key="index" class="category-card">
            <h3 class="category-title">{{ cat.name }}</h3>
            <ul class="attr-list">
              <li v-for="attr in cat.attrs" :key="attr.key" class="attr-row">
                <span class="attr-name">{{ attr.label }}</span>
                <span class="attr-value">{{ attr.value }}</span>
                <div class="attr-bar">
                  <div class="bar-fill" :style="{ width: (attr.value / 99) * 100 + '%' }"></div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Positions -->
      <div class="positions-section">
        <h2>Positions</h2>
        <div class="positions-grid">
          <div
            v-for="(pos, idx) in playerPositions"
            :key="idx"
            class="position-badge"
            :class="pos.type"
          >
            {{ pos.abbr }}
          </div>
        </div>
      </div>

      <!-- Skills & Traits -->
      <div class="skills-section" v-if="activeSkills.length">
        <h2>Skills & Traits</h2>
        <div class="skills-grid">
          <span v-for="skill in activeSkills" :key="skill.key" class="skill-badge">
            {{ skill.label }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getPlayerById } from '@/api'; // adjust path if necessary
import { countryNameFromCode } from '@/utils/countryMapping'; // if you have this

const route = useRoute();
const player = ref(null);
const loading = ref(true);
const error = ref(null);
const imageError = ref(false);

// Compute player photo path (assumes player ID matches filename)
const playerPhoto = computed(() => {
  if (imageError.value || !player.value) return '/players/default.png'; // fallback image
  return `/players/${player.value.id}.png`;
});

function handleImageError() {
  imageError.value = true;
}

// Fetch player data by ID from route
async function fetchPlayer(id) {
  loading.value = true;
  error.value = null;
  try {
    const data = await getPlayerById(id);
    player.value = data;
    // Ensure country name mapping if you have the utility
    if (player.value.country && countryNameFromCode) {
      player.value.country_name = countryNameFromCode(player.value.country);
    }
  } catch (e) {
    error.value = 'Player not found or network error.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  const id = route.params.id;
  if (id) fetchPlayer(id);
});

watch(() => route.params.id, (newId) => {
  if (newId) fetchPlayer(newId);
});

// Helper to format currency
function formatCurrency(value) {
  if (value == null) return '–';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value);
}

// Define attribute categories mapping from actual DB fields
const attributeCategories = computed(() => {
  if (!player.value) return [];
  return [
    {
      name: 'Attacking',
      attrs: [
        { key: 'offensive_awareness', label: 'Off. Awareness', value: player.value.offensive_awareness },
        { key: 'ball_control', label: 'Ball Control', value: player.value.ball_control },
        { key: 'dribbling', label: 'Dribbling', value: player.value.dribbling },
        { key: 'tight_possession', label: 'Tight Possession', value: player.value.tight_possession },
        { key: 'low_pass', label: 'Low Pass', value: player.value.low_pass },
        { key: 'lofted_pass', label: 'Lofted Pass', value: player.value.lofted_pass },
        { key: 'finishing', label: 'Finishing', value: player.value.finishing },
        { key: 'heading', label: 'Heading', value: player.value.heading },
        { key: 'place_kicking', label: 'Place Kicking', value: player.value.place_kicking },
        { key: 'curl', label: 'Curl', value: player.value.curl },
      ],
    },
    {
      name: 'Physical',
      attrs: [
        { key: 'speed', label: 'Speed', value: player.value.speed },
        { key: 'acceleration', label: 'Acceleration', value: player.value.acceleration },
        { key: 'kicking_power', label: 'Kicking Power', value: player.value.kicking_power },
        { key: 'jump', label: 'Jump', value: player.value.jump },
        { key: 'physical_contact', label: 'Physical Contact', value: player.value.physical_contact },
        { key: 'balance', label: 'Balance', value: player.value.balance },
        { key: 'stamina', label: 'Stamina', value: player.value.stamina },
      ],
    },
    {
      name: 'Defensive',
      attrs: [
        { key: 'defensive_awareness', label: 'Def. Awareness', value: player.value.defensive_awareness },
        { key: 'ball_winning', label: 'Ball Winning', value: player.value.ball_winning },
        { key: 'aggression', label: 'Aggression', value: player.value.aggression },
      ],
    },
    {
      name: 'Goalkeeping',
      attrs: [
        { key: 'gk_awareness', label: 'GK Awareness', value: player.value.gk_awareness },
        { key: 'gk_catching', label: 'GK Catching', value: player.value.gk_catching },
        { key: 'gk_clearing', label: 'GK Clearing', value: player.value.gk_clearing },
        { key: 'gk_reflexes', label: 'GK Reflexes', value: player.value.gk_reflexes },
        { key: 'gk_reach', label: 'GK Reach', value: player.value.gk_reach },
      ],
    },
    {
      name: 'Misc',
      attrs: [
        { key: 'weak_foot_usage', label: 'Weak Foot Usage', value: player.value.weak_foot_usage },
        { key: 'weak_foot_accuracy', label: 'Weak Foot Acc.', value: player.value.weak_foot_accuracy },
        { key: 'form', label: 'Form', value: player.value.form },
        { key: 'injury_resistance', label: 'Injury Resistance', value: player.value.injury_resistance },
      ],
    },
  ];
});

// Process positions from DB (assuming player.positions contains e.g., { gk: true/false, ... })
const playerPositions = computed(() => {
  if (!player.value) return [];
  const posMap = player.value.positions;
  if (!posMap) return [];
  // Map of abbreviation and type (natural or experienced)
  const allPositions = [
    { key: 'gk', abbr: 'GK' },
    { key: 'cb', abbr: 'CB' },
    { key: 'lb', abbr: 'LB' },
    { key: 'rb', abbr: 'RB' },
    { key: 'dmf', abbr: 'DMF' },
    { key: 'cmf', abbr: 'CMF' },
    { key: 'lmf', abbr: 'LMF' },
    { key: 'rmf', abbr: 'RMF' },
    { key: 'amf', abbr: 'AMF' },
    { key: 'lwf', abbr: 'LWF' },
    { key: 'rwf', abbr: 'RWF' },
    { key: 'ss', abbr: 'SS' },
    { key: 'cf', abbr: 'CF' },
  ];
  return allPositions
    .filter(pos => posMap[pos.key] !== undefined)
    .map(pos => ({
      abbr: pos.abbr,
      type: posMap[pos.key] ? 'natural' : 'experienced',
    }));
});

// Skills (boolean traits)
const activeSkills = computed(() => {
  if (!player.value) return [];
  const skillFields = [
    { key: 'trickster', label: 'Trickster' },
    { key: 'gamesmanship', label: 'Gamesmanship' },
    { key: 'fighting_spirit', label: 'Fighting Spirit' },
    // add all other boolean fields you have
    // check player_schema.py for the full list
  ];
  return skillFields.filter(s => player.value[s.key] === true);
});
</script>

<style scoped>
/* Global reset & dark theme (tailwind or custom?) – using scoped styles for now */
.player-profile {
  min-height: 100vh;
  background: #0f172a;
  color: #e2e8f0;
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #334155;
  border-top: 4px solid #38bdf8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

.back-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  color: #94a3b8;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.back-link:hover {
  color: #38bdf8;
}

.hero-card {
  display: flex;
  gap: 2rem;
  background: #1e293b;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

.player-photo img {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #38bdf8;
}

.player-name {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 0.5rem;
}

.ovr-badge {
  background: #f97316;
  color: #fff;
  display: inline-block;
  padding: 0.25rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin: 1rem 0;
}

.meta-item .label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #94a3b8;
}

.meta-item .value {
  font-weight: 600;
}

.financials {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.finance-item .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #94a3b8;
}

.finance-item .value {
  font-weight: 700;
  color: #38bdf8;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #334155;
  padding-bottom: 0.5rem;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.category-card {
  background: #1e293b;
  border-radius: 8px;
  padding: 1rem;
}

.category-title {
  font-size: 1rem;
  text-transform: uppercase;
  color: #38bdf8;
  margin-bottom: 0.75rem;
}

.attr-list {
  list-style: none;
  padding: 0;
}

.attr-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.attr-name {
  flex: 1;
  font-size: 0.85rem;
}

.attr-value {
  font-weight: 700;
  width: 2rem;
  text-align: right;
  margin-right: 0.75rem;
}

.attr-bar {
  width: 80px;
  height: 6px;
  background: #334155;
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #38bdf8;
  border-radius: 3px;
}

.positions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.position-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.position-badge.natural {
  background: #166534;
  color: #bbf7d0;
}

.position-badge.experienced {
  background: #854d0e;
  color: #fef08a;
}

.skills-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-badge {
  background: #312e81;
  color: #e0e7ff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}
</style>