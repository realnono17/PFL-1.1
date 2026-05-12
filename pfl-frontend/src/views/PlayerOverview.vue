<template>
  <div class="player-profile">
    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading player profile...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-container">
      <h2>Error loading player</h2>
      <p>{{ error }}</p>
      <router-link to="/players" class="back-link">← Back to Players</router-link>
    </div>

    <!-- Player loaded -->
    <div v-else-if="player" class="profile-layout">
      <!-- Back link -->
      <router-link to="/players" class="back-link">← Back to Players</router-link>

      <!-- Full-width header section -->
      <div class="header-row">
        <div class="photo-area">
          <img
            :src="playerPhoto"
            :alt="player.name"
            @error="handleImageError"
            class="player-img"
          />
        </div>

        <div class="identity-area">
          <div class="name-ovr-row">
            <h1 class="player-name">{{ player.name }}</h1>
            <div class="ovr-badge">{{ player.overall_stats }}</div>
          </div>

          <div v-if="player.market_value" class="market-badge">
            MARKET VALUE {{ formatCurrency(player.market_value) }}
          </div>

          <div class="bio-grid">
            <div class="bio-item">
              <span class="label">Age</span>
              <span class="value">{{ player.age }}</span>
            </div>
            <div class="bio-item">
              <span class="label">Nationality</span>
              <span class="value">{{ player.country_name || player.country }}</span>
            </div>
            <div class="bio-item">
              <span class="label">Club</span>
              <span class="value">{{ player.club_name || 'Free Agent' }}</span>
            </div>
            <div class="bio-item">
              <span class="label">Height</span>
              <span class="value">{{ player.height }} cm</span>
            </div>
            <div class="bio-item">
              <span class="label">Weight</span>
              <span class="value">{{ player.weight }} kg</span>
            </div>
            <div class="bio-item">
              <span class="label">Foot</span>
              <span class="value">{{ player.foot?.toUpperCase() }}</span>
            </div>
          </div>

          <div v-if="playerPositions.length" class="positions-area">
            <span class="positions-label">Positions</span>
            <div class="positions-list">
              <span
                v-for="(pos, idx) in playerPositions"
                :key="idx"
                class="position-chip"
                :class="pos.type"
              >{{ pos.abbr }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Full-width attributes grid -->
      <div class="attributes-grid">
        <div class="attr-column" v-if="attackingAttrs.length">
          <h2 class="col-title">Technical</h2>
          <ul class="attr-list">
            <li v-for="attr in attackingAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :style="{ color: getAttrColor(attr.value) }">
                {{ attr.value }}
              </span>
            </li>
          </ul>
        </div>

        <div class="attr-column" v-if="physicalAttrs.length || miscAttrs.length">
          <h2 class="col-title">Physical</h2>
          <ul class="attr-list" v-if="physicalAttrs.length">
            <li v-for="attr in physicalAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :style="{ color: getAttrColor(attr.value) }">
                {{ attr.value }}
              </span>
            </li>
          </ul>
          <div v-if="miscAttrs.length" class="sub-block">
            <h2 class="col-title">Mental</h2>
            <ul class="attr-list">
              <li v-for="attr in miscAttrs" :key="attr.key" class="attr-row">
                <span class="attr-label">{{ attr.label }}</span>
                <span class="attr-value" :style="{ color: getAttrColor(attr.value) }">
                  {{ attr.value }}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div class="attr-column" v-if="defensiveAttrs.length || gkAttrs.length">
          <h2 class="col-title">Defensive</h2>
          <ul class="attr-list" v-if="defensiveAttrs.length">
            <li v-for="attr in defensiveAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :style="{ color: getAttrColor(attr.value) }">
                {{ attr.value }}
              </span>
            </li>
          </ul>
          <div v-if="gkAttrs.length" class="sub-block">
            <h2 class="col-title">Goalkeeping</h2>
            <ul class="attr-list">
              <li v-for="attr in gkAttrs" :key="attr.key" class="attr-row">
                <span class="attr-label">{{ attr.label }}</span>
                <span class="attr-value" :style="{ color: getAttrColor(attr.value) }">
                  {{ attr.value }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Traits -->
      <div v-if="activeSkills.length" class="skills-section">
        <h2 class="col-title">Traits</h2>
        <div class="skills-container">
          <span v-for="skill in activeSkills" :key="skill.key" class="skill-badge">
            {{ skill.label }}
          </span>
        </div>
      </div>

      <!-- Footer -->
      <div class="footer">
        <p class="copyright">© 2025 Pirate Football League</p>
        <p class="social-links">
          <a href="#">Twitter</a>
          <a href="#">Twitch</a>
          <a href="#">About</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getPlayerById } from '@/api';
import countryMapping from '@/utils/countryMapping';

const route = useRoute();
const player = ref(null);
const loading = ref(true);
const error = ref(null);
const imageError = ref(false);

const playerPhoto = computed(() => {
  if (imageError.value || !player.value) return '/players/default.png';
  return `/players/${player.value.id}.png`;
});

function handleImageError() {
  imageError.value = true;
}

async function fetchPlayer(id) {
  loading.value = true;
  error.value = null;
  try {
    const data = await getPlayerById(id);
    player.value = data;
    if (player.value.country != null) {
      const code = String(player.value.country);
      player.value.country_name = countryMapping[code] || player.value.country;
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

function formatCurrency(value) {
  if (value == null) return '–';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value);
}

function getAttrColor(value) {
  if (value >= 80) return '#4ade80';
  if (value >= 70) return '#facc15';
  return '#f87171';
}

const attackingAttrs = computed(() => {
  if (!player.value) return [];
  return [
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
  ];
});

const physicalAttrs = computed(() => {
  if (!player.value) return [];
  return [
    { key: 'speed', label: 'Speed', value: player.value.speed },
    { key: 'acceleration', label: 'Acceleration', value: player.value.acceleration },
    { key: 'kicking_power', label: 'Kicking Power', value: player.value.kicking_power },
    { key: 'jump', label: 'Jump', value: player.value.jump },
    { key: 'physical_contact', label: 'Physical Contact', value: player.value.physical_contact },
    { key: 'balance', label: 'Balance', value: player.value.balance },
    { key: 'stamina', label: 'Stamina', value: player.value.stamina },
  ];
});

const defensiveAttrs = computed(() => {
  if (!player.value) return [];
  return [
    { key: 'defensive_awareness', label: 'Def. Awareness', value: player.value.defensive_awareness },
    { key: 'ball_winning', label: 'Ball Winning', value: player.value.ball_winning },
    { key: 'aggression', label: 'Aggression', value: player.value.aggression },
  ];
});

const gkAttrs = computed(() => {
  if (!player.value) return [];
  return [
    { key: 'gk_awareness', label: 'GK Awareness', value: player.value.gk_awareness },
    { key: 'gk_catching', label: 'GK Catching', value: player.value.gk_catching },
    { key: 'gk_clearing', label: 'GK Clearing', value: player.value.gk_clearing },
    { key: 'gk_reflexes', label: 'GK Reflexes', value: player.value.gk_reflexes },
    { key: 'gk_reach', label: 'GK Reach', value: player.value.gk_reach },
  ];
});

const miscAttrs = computed(() => {
  if (!player.value) return [];
  return [
    { key: 'weak_foot_usage', label: 'Weak Foot Usage', value: player.value.weak_foot_usage },
    { key: 'weak_foot_accuracy', label: 'Weak Foot Acc.', value: player.value.weak_foot_accuracy },
    { key: 'form', label: 'Form', value: player.value.form },
    { key: 'injury_resistance', label: 'Injury Resistance', value: player.value.injury_resistance },
  ];
});

const playerPositions = computed(() => {
  if (!player.value) return [];
  const posMap = player.value.positions;
  if (!posMap) return [];
  const allPositions = [
    { key: 'gk', abbr: 'GK' }, { key: 'cb', abbr: 'CB' },
    { key: 'lb', abbr: 'LB' }, { key: 'rb', abbr: 'RB' },
    { key: 'dmf', abbr: 'DMF' }, { key: 'cmf', abbr: 'CMF' },
    { key: 'lmf', abbr: 'LMF' }, { key: 'rmf', abbr: 'RMF' },
    { key: 'amf', abbr: 'AMF' }, { key: 'lwf', abbr: 'LWF' },
    { key: 'rwf', abbr: 'RWF' }, { key: 'ss', abbr: 'SS' },
    { key: 'cf', abbr: 'CF' },
  ];
  return allPositions
    .filter(pos => posMap[pos.key] !== undefined)
    .map(pos => ({
      abbr: pos.abbr,
      type: posMap[pos.key] ? 'natural' : 'experienced',
    }));
});

const activeSkills = computed(() => {
  if (!player.value) return [];
  const skillFields = [
    { key: 'trickster', label: 'Trickster' },
    { key: 'gamesmanship', label: 'Gamesmanship' },
    { key: 'fighting_spirit', label: 'Fighting Spirit' },
  ];
  return skillFields.filter(s => player.value[s.key] === true);
});
</script>

<style scoped>
/* ===== Base & Layout ===== */
.player-profile {
  min-height: 100vh;
  background: #0f1115;
  color: #e2e8f0;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  display: flex;
  justify-content: center;
  padding: 1rem 1.5rem 2rem;
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
  width: 48px;
  height: 48px;
  border: 4px solid #2d3748;
  border-top: 4px solid #fbbf24;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #94a3b8;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.back-link:hover { color: #fbbf24; }

/* ===== Main container ===== */
.profile-layout {
  width: 100%;
  max-width: 1500px;
}

/* ===== Header Row ===== */
.header-row {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  background: #1a1d24;
  border-radius: 12px;
  padding: 2rem;
}

.photo-area {
  flex-shrink: 0;
}
.player-img {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fbbf24;
}

.identity-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 0;
}

.name-ovr-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.player-name {
  font-size: 2.8rem;
  font-weight: 800;
  color: #fbbf24;
  margin: 0;
  line-height: 1.1;
}

.ovr-badge {
  background: #d97706;
  color: white;
  padding: 0.3rem 1.5rem;
  border-radius: 24px;
  font-weight: 700;
  font-size: 1.6rem;
  flex-shrink: 0;
}

.market-badge {
  background: #166534;
  color: white;
  padding: 0.4rem 1.2rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1rem;
  align-self: flex-start;
}

/* Bio grid */
.bio-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.6rem 1.5rem;
  margin-top: 0.25rem;
}
.bio-item .label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #9ca3af;
  letter-spacing: 0.3px;
}
.bio-item .value {
  font-weight: 600;
  font-size: 1rem;
}

/* Positions */
.positions-area {
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.positions-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #9ca3af;
  flex-shrink: 0;
}
.positions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.position-chip {
  padding: 0.25rem 0.8rem;
  border-radius: 4px;
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
}
.position-chip.natural {
  background: #166534;
  color: #bbf7d0;
}
.position-chip.experienced {
  background: #854d0e;
  color: #fef08a;
}

/* ===== Attributes Grid ===== */
.attributes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.attr-column {
  background: #1e222b;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
}

.sub-block {
  margin-top: 1.5rem;
}

.col-title {
  font-size: 1.1rem;
  text-transform: uppercase;
  font-weight: 700;
  color: white;
  text-align: center;
  border-bottom: 1px solid #2d3748;
  padding-bottom: 0.5rem;
  margin: 0 0 0.75rem 0;
}

.attr-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.attr-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.35rem 0;
  border-bottom: 1px solid #2d3340;
}
.attr-row:last-child {
  border-bottom: none;
}

.attr-label {
  font-size: 0.9rem;
}

.attr-value {
  font-weight: 700;
  font-size: 1rem;
  min-width: 2rem;
  text-align: right;
}

/* ===== Skills ===== */
.skills-section {
  margin-bottom: 1.5rem;
}
.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.skill-badge {
  background: #1f2a44;
  color: #c7d2fe;
  padding: 0.3rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

/* ===== Footer ===== */
.footer {
  text-align: center;
  border-top: 1px solid #2d3748;
  padding-top: 1rem;
  margin-top: 1.5rem;
}
.copyright {
  color: #6b7280;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}
.social-links a {
  color: #60a5fa;
  margin: 0 0.5rem;
  text-decoration: none;
  font-size: 0.9rem;
}
.social-links a:hover {
  color: #fbbf24;
}

/* ===== Mobile ===== */
@media (max-width: 768px) {
  .player-profile {
    padding: 0.75rem;
  }
  .header-row {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.25rem;
  }
  .name-ovr-row {
    justify-content: center;
  }
  .player-name {
    font-size: 2rem;
  }
  .bio-grid {
    grid-template-columns: 1fr 1fr;
  }
  .attributes-grid {
    grid-template-columns: 1fr;
  }
}

/* ===== Large screens ===== */
@media (min-width: 1600px) {
  .profile-layout {
    max-width: 1600px;
  }
  .attributes-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  .player-name {
    font-size: 3rem;
  }
}
</style>