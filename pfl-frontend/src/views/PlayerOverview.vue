<template>
  <div class="player-dashboard">
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
    <div v-else-if="player" class="dashboard-layout">
      <router-link to="/players" class="back-link">← Back to Players</router-link>

      <!-- ===== TOP HEADER BAR ===== -->
      <div class="top-bar">
        <div class="top-left">
          <div class="photo-area">
            <img
              :src="playerPhoto"
              :alt="player.name"
              @error="handleImageError"
              class="player-img"
            />
            <div class="ovr-badge">{{ player.overall_stats }}</div>
          </div>
          <div class="identity-info">
            <h1 class="player-name">{{ player.name }}</h1>
            <div class="identity-details">
              <span>{{ player.country_name || player.country }}</span>
              <span class="sep">•</span>
              <span>Age {{ player.age }}</span>
              <span class="sep">•</span>
              <span>{{ player.club_name || 'Free Agent' }}</span>
            </div>
            <!-- Positions inline -->
            <div class="positions-inline" v-if="playerPositions.length">
              <span
                v-for="(pos, idx) in playerPositions"
                :key="idx"
                class="pos-chip"
                :class="pos.type"
              >{{ pos.abbr }}</span>
            </div>
          </div>
        </div>

        <div class="top-center">
          <div class="contract-box">
            <div class="contract-item">
              <span class="clabel">Market Value</span>
              <span class="cvalue">{{ formatCurrency(player.market_value) }}</span>
            </div>
            <div class="contract-item">
              <span class="clabel">Wage</span>
              <span class="cvalue">{{ formatCurrency(player.wage) }}/w</span>
            </div>
            <div class="contract-item">
              <span class="clabel">Foot</span>
              <span class="cvalue">{{ player.foot?.toUpperCase() || '—' }}</span>
            </div>
            <div class="contract-item">
              <span class="clabel">Height</span>
              <span class="cvalue">{{ player.height }} cm</span>
            </div>
            <div class="contract-item">
              <span class="clabel">Weight</span>
              <span class="cvalue">{{ player.weight }} kg</span>
            </div>
          </div>
        </div>

        <div class="top-right">
          <div class="bio-specs">
            <div class="spec-item">
              <span class="slabel">Form</span>
              <span class="svalue" :style="{ color: getAttrColor(player.form) }">{{ player.form }}</span>
            </div>
            <div class="spec-item">
              <span class="slabel">Injury Resistance</span>
              <span class="svalue" :style="{ color: getAttrColor(player.injury_resistance) }">{{ player.injury_resistance }}</span>
            </div>
            <div class="spec-item">
              <span class="slabel">Weak Foot Usage</span>
              <span class="svalue">{{ player.weak_foot_usage }}</span>
            </div>
            <div class="spec-item">
              <span class="slabel">Weak Foot Acc.</span>
              <span class="svalue">{{ player.weak_foot_accuracy }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== MAIN DASHBOARD GRID ===== -->
      <div class="dashboard-grid">
        
        <!-- COLUMN 1: Mini Pitch + Traits -->
        <div class="grid-col col-positions">
          <div class="mini-pitch">
            <div class="pitch-zone zone-attack">
              <span class="zone-label">ATT</span>
              <div class="zone-badges">
                <span
                  v-for="pos in getPositionsByZone('attack')"
                  :key="pos.abbr"
                  class="pitch-badge"
                  :class="pos.type"
                >{{ pos.abbr }}</span>
              </div>
            </div>
            <div class="pitch-zone zone-midfield">
              <span class="zone-label">MID</span>
              <div class="zone-badges">
                <span
                  v-for="pos in getPositionsByZone('midfield')"
                  :key="pos.abbr"
                  class="pitch-badge"
                  :class="pos.type"
                >{{ pos.abbr }}</span>
              </div>
            </div>
            <div class="pitch-zone zone-defense">
              <span class="zone-label">DEF</span>
              <div class="zone-badges">
                <span
                  v-for="pos in getPositionsByZone('defense')"
                  :key="pos.abbr"
                  class="pitch-badge"
                  :class="pos.type"
                >{{ pos.abbr }}</span>
              </div>
            </div>
            <div class="pitch-zone zone-gk" v-if="getPositionsByZone('gk').length">
              <span class="zone-label">GK</span>
              <div class="zone-badges">
                <span
                  v-for="pos in getPositionsByZone('gk')"
                  :key="pos.abbr"
                  class="pitch-badge"
                  :class="pos.type"
                >{{ pos.abbr }}</span>
              </div>
            </div>
          </div>

          <div class="traits-block" v-if="activeSkills.length">
            <h3 class="block-title">Traits</h3>
            <div class="traits-list">
              <span v-for="skill in activeSkills" :key="skill.key" class="trait-chip">
                {{ skill.label }}
              </span>
            </div>
          </div>
          <div class="traits-block" v-else>
            <h3 class="block-title">Traits</h3>
            <p class="no-traits">No special traits</p>
          </div>
        </div>

        <!-- COLUMN 2: Technical -->
        <div class="grid-col col-technical">
          <h3 class="block-title">Technical</h3>
          <div class="attr-list">
            <div v-for="attr in attackingAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :class="getValueClass(attr.value)">{{ attr.value }}</span>
            </div>
          </div>
        </div>

        <!-- COLUMN 3: Mental + Defensive -->
        <div class="grid-col col-mental-defensive">
          <h3 class="block-title">Mental</h3>
          <div class="attr-list">
            <div v-for="attr in miscAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :class="getValueClass(attr.value)">{{ attr.value }}</span>
            </div>
          </div>
          <h3 class="block-title sub-title">Defensive</h3>
          <div class="attr-list">
            <div v-for="attr in defensiveAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :class="getValueClass(attr.value)">{{ attr.value }}</span>
            </div>
          </div>
          <div v-if="gkAttrs.length && hasGKValues" class="sub-title-section">
            <h3 class="block-title sub-title">Goalkeeping</h3>
            <div class="attr-list">
              <div v-for="attr in gkAttrs" :key="attr.key" class="attr-row">
                <span class="attr-label">{{ attr.label }}</span>
                <span class="attr-value" :class="getValueClass(attr.value)">{{ attr.value }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- COLUMN 4: Physical -->
        <div class="grid-col col-physical">
          <h3 class="block-title">Physical</h3>
          <div class="attr-list">
            <div v-for="attr in physicalAttrs" :key="attr.key" class="attr-row">
              <span class="attr-label">{{ attr.label }}</span>
              <span class="attr-value" :class="getValueClass(attr.value)">{{ attr.value }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="dashboard-footer">
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
  if (value == null) return '#9ca3af';
  if (value >= 80) return '#4ade80';
  if (value >= 70) return '#facc15';
  return '#f87171';
}

function getValueClass(value) {
  if (value == null) return 'val-none';
  if (value >= 80) return 'val-high';
  if (value >= 70) return 'val-mid';
  return 'val-low';
}

const attackingAttrs = computed(() => {
  if (!player.value) return [];
  const keys = [
    'offensive_awareness', 'ball_control', 'dribbling', 'tight_possession',
    'low_pass', 'lofted_pass', 'finishing', 'heading', 'place_kicking', 'curl'
  ];
  return keys.map(k => ({ key: k, label: formatLabel(k), value: player.value[k] }));
});

const physicalAttrs = computed(() => {
  if (!player.value) return [];
  const keys = ['speed', 'acceleration', 'kicking_power', 'jump', 'physical_contact', 'balance', 'stamina'];
  return keys.map(k => ({ key: k, label: formatLabel(k), value: player.value[k] }));
});

const defensiveAttrs = computed(() => {
  if (!player.value) return [];
  const keys = ['defensive_awareness', 'ball_winning', 'aggression'];
  return keys.map(k => ({ key: k, label: formatLabel(k), value: player.value[k] }));
});

const gkAttrs = computed(() => {
  if (!player.value) return [];
  const keys = ['gk_awareness', 'gk_catching', 'gk_clearing', 'gk_reflexes', 'gk_reach'];
  return keys.map(k => ({ key: k, label: formatLabel(k), value: player.value[k] }));
});

const miscAttrs = computed(() => {
  if (!player.value) return [];
  const keys = ['weak_foot_usage', 'weak_foot_accuracy', 'form', 'injury_resistance'];
  return keys.map(k => ({ key: k, label: formatLabel(k), value: player.value[k] }));
});

const hasGKValues = computed(() => {
  if (!player.value) return false;
  return gkAttrs.value.some(a => a.value > 1);
});

function formatLabel(key) {
  const labels = {
    offensive_awareness: 'Off. Awareness', ball_control: 'Ball Control',
    dribbling: 'Dribbling', tight_possession: 'Tight Possession',
    low_pass: 'Low Pass', lofted_pass: 'Lofted Pass',
    finishing: 'Finishing', heading: 'Heading',
    place_kicking: 'Place Kicking', curl: 'Curl',
    speed: 'Speed', acceleration: 'Acceleration',
    kicking_power: 'Kicking Power', jump: 'Jump',
    physical_contact: 'Physical Contact', balance: 'Balance', stamina: 'Stamina',
    defensive_awareness: 'Def. Awareness', ball_winning: 'Ball Winning', aggression: 'Aggression',
    gk_awareness: 'GK Awareness', gk_catching: 'GK Catching',
    gk_clearing: 'GK Clearing', gk_reflexes: 'GK Reflexes', gk_reach: 'GK Reach',
    weak_foot_usage: 'Weak Foot Usage', weak_foot_accuracy: 'Weak Foot Acc.',
    form: 'Form', injury_resistance: 'Injury Resistance',
  };
  return labels[key] || key;
}

const playerPositions = computed(() => {
  if (!player.value) return [];
  const posMap = player.value.positions;
  if (!posMap) return [];
  const allPositions = [
    { key: 'gk', abbr: 'GK', zone: 'gk' },
    { key: 'cb', abbr: 'CB', zone: 'defense' },
    { key: 'lb', abbr: 'LB', zone: 'defense' },
    { key: 'rb', abbr: 'RB', zone: 'defense' },
    { key: 'dmf', abbr: 'DMF', zone: 'midfield' },
    { key: 'cmf', abbr: 'CMF', zone: 'midfield' },
    { key: 'lmf', abbr: 'LMF', zone: 'midfield' },
    { key: 'rmf', abbr: 'RMF', zone: 'midfield' },
    { key: 'amf', abbr: 'AMF', zone: 'attack' },
    { key: 'lwf', abbr: 'LWF', zone: 'attack' },
    { key: 'rwf', abbr: 'RWF', zone: 'attack' },
    { key: 'ss', abbr: 'SS', zone: 'attack' },
    { key: 'cf', abbr: 'CF', zone: 'attack' },
  ];
  return allPositions
    .filter(pos => posMap[pos.key] !== undefined)
    .map(pos => ({
      abbr: pos.abbr,
      type: posMap[pos.key] ? 'natural' : 'experienced',
      zone: pos.zone,
    }));
});

function getPositionsByZone(zone) {
  return playerPositions.value.filter(p => p.zone === zone);
}

const activeSkills = computed(() => {
  if (!player.value) return [];
  const skillFields = [
    { key: 'trickster', label: 'Trickster' },
    { key: 'gamesmanship', label: 'Gamesmanship' },
    { key: 'fighting_spirit', label: 'Fighting Spirit' },
    { key: 'acrobatic_finishing', label: 'Acrobatic Finishing' },
    { key: 'outside_curler', label: 'Outside Curler' },
    { key: 'long_range_shots', label: 'Long Range Shots' },
    { key: 'early_cross', label: 'Early Cross' },
    { key: 'long_throw', label: 'Long Throw' },
    { key: 'penalty_specialist', label: 'Penalty Specialist' },
    { key: 'chip_shot_control', label: 'Chip Shot Control' },
  ];
  return skillFields.filter(s => player.value[s.key] === true);
});
</script>

<style scoped>
/* ========== BASE ========== */
.player-dashboard {
  min-height: 100vh;
  background: #0d1117;
  color: #c9d1d9;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  font-size: 16px;
  padding: 0 2rem 2rem;
  box-sizing: border-box;
  line-height: 1.5;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  font-size: 1.2rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #21262d;
  border-top: 4px solid #fbbf24;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

.back-link {
  display: inline-block;
  margin: 1rem 0 0.75rem;
  color: #8b949e;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s;
}
.back-link:hover { color: #fbbf24; }

.dashboard-layout {
  width: 100%;
  max-width: 1500px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 120px);
}

/* ========== TOP BAR ========== */
.top-bar {
  display: flex;
  gap: 2rem;
  align-items: stretch;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 10px;
  padding: 1.5rem 2rem;
  margin-bottom: 1.25rem;
  flex-shrink: 0;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1.4;
  min-width: 300px;
}

.photo-area {
  position: relative;
  flex-shrink: 0;
}

.player-img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fbbf24;
}

.ovr-badge {
  position: absolute;
  bottom: -2px;
  right: -6px;
  background: #d97706;
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  padding: 0.2rem 0.7rem;
  border-radius: 14px;
  border: 3px solid #161b22;
}

.identity-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.player-name {
  font-size: 2.2rem;
  font-weight: 800;
  color: #fbbf24;
  margin: 0;
  line-height: 1.1;
}

.identity-details {
  font-size: 1rem;
  color: #8b949e;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
}

.sep {
  color: #30363d;
}

.positions-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.3rem;
}

.pos-chip {
  padding: 0.25rem 0.7rem;
  border-radius: 4px;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.pos-chip.natural {
  background: #166534;
  color: #bbf7d0;
}

.pos-chip.experienced {
  background: #854d0e;
  color: #fef08a;
}

/* Center: Contract */
.top-center {
  flex: 0.9;
  min-width: 200px;
  display: flex;
  align-items: center;
}

.contract-box {
  background: #0d1117;
  border: 1px solid #21262d;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  width: 100%;
}

.contract-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clabel {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #8b949e;
  letter-spacing: 0.5px;
}

.cvalue {
  font-weight: 700;
  font-size: 0.95rem;
  color: #58a6ff;
}

/* Right: Bio specs */
.top-right {
  flex: 0.9;
  min-width: 200px;
  display: flex;
  align-items: center;
}

.bio-specs {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  width: 100%;
  background: #0d1117;
  border: 1px solid #21262d;
  border-radius: 8px;
  padding: 1rem 1.25rem;
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slabel {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #8b949e;
  letter-spacing: 0.5px;
}

.svalue {
  font-weight: 700;
  font-size: 0.95rem;
}

/* ========== DASHBOARD GRID ========== */
.dashboard-grid {
  display: grid;
  grid-template-columns: 220px 1fr 1fr 1fr;
  gap: 1rem;
  flex: 1;
  margin-bottom: 1.25rem;
}

.grid-col {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
}

.block-title {
  font-size: 0.85rem;
  text-transform: uppercase;
  font-weight: 700;
  color: #e2e8f0;
  text-align: center;
  margin: 0 0 0.6rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #21262d;
  letter-spacing: 0.6px;
}

.sub-title {
  margin-top: 1rem;
}

/* ===== Mini Pitch ===== */
.mini-pitch {
  background: linear-gradient(180deg, #1a5c1a 0%, #1f6e1f 50%, #1a5c1a 100%);
  border-radius: 6px;
  border: 1px solid #2d6b2d;
  padding: 0.5rem;
  margin-bottom: 1rem;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.pitch-zone {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.5rem;
  border-radius: 3px;
  position: relative;
  min-height: 36px;
}

.zone-attack { background: rgba(255,255,255,0.06); }
.zone-midfield { background: rgba(255,255,255,0.03); border-top: 1px dashed rgba(255,255,255,0.25); border-bottom: 1px dashed rgba(255,255,255,0.25); }
.zone-defense { background: rgba(255,255,255,0.06); }
.zone-gk { background: rgba(255,200,50,0.12); border-top: 1px solid rgba(255,200,50,0.4); }

.zone-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: rgba(255,255,255,0.55);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  width: 26px;
  flex-shrink: 0;
  text-align: center;
}

.zone-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.pitch-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.pitch-badge.natural {
  background: #166534;
  color: #bbf7d0;
}

.pitch-badge.experienced {
  background: #854d0e;
  color: #fef08a;
}

/* Traits */
.traits-block {
  margin-top: 0.25rem;
}

.traits-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.trait-chip {
  background: #1f2a44;
  color: #c7d2fe;
  font-size: 0.72rem;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  white-space: nowrap;
}

.no-traits {
  font-size: 0.78rem;
  color: #484f58;
  text-align: center;
  font-style: italic;
}

/* ===== Attribute Lists ===== */
.attr-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.attr-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.45rem 0.5rem;
  border-radius: 4px;
  background: rgba(255,255,255,0.018);
}

.attr-row:nth-child(even) {
  background: rgba(255,255,255,0.035);
}

.attr-label {
  font-size: 0.85rem;
  color: #c9d1d9;
}

.attr-value {
  font-weight: 700;
  font-size: 0.9rem;
  min-width: 34px;
  text-align: center;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
}

/* Value background colors */
.val-high {
  background: #166534;
  color: #bbf7d0;
}

.val-mid {
  background: #5c4a0e;
  color: #fde68a;
}

.val-low {
  background: #5c1a1a;
  color: #fca5a5;
}

.val-none {
  background: transparent;
  color: #484f58;
}

/* ========== FOOTER ========== */
.dashboard-footer {
  text-align: center;
  border-top: 1px solid #21262d;
  padding-top: 1rem;
  flex-shrink: 0;
}

.copyright {
  color: #484f58;
  font-size: 0.75rem;
  margin-bottom: 0.3rem;
}

.social-links a {
  color: #58a6ff;
  margin: 0 0.5rem;
  text-decoration: none;
  font-size: 0.8rem;
}

.social-links a:hover {
  color: #fbbf24;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 200px 1fr 1fr;
  }
  .col-physical {
    grid-column: 2 / 4;
  }
}

@media (max-width: 900px) {
  .player-dashboard {
    font-size: 15px;
    padding: 0 1rem 1.5rem;
  }
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
  .col-positions {
    grid-column: 1 / -1;
    flex-direction: row;
    gap: 1rem;
  }
  .mini-pitch {
    flex: 1;
    min-height: 150px;
    flex-direction: row;
  }
  .pitch-zone {
    flex-direction: column;
    min-width: 50px;
    align-items: center;
  }
  .zone-badges {
    flex-direction: column;
    align-items: center;
  }
  .top-bar {
    flex-direction: column;
  }
}

@media (max-width: 600px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .col-positions {
    flex-direction: column;
  }
  .player-img {
    width: 100px;
    height: 100px;
  }
  .player-name {
    font-size: 1.5rem;
  }
}
</style>