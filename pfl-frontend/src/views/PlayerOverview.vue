<template>
  <div class="player-overview-fm">
    <!-- Loading & Error States -->
    <div v-if="loading" class="loading">Loading player details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="player" class="fm-content">
      <!-- Floating box effect added here -->
      <div class="floating-box">
        <!-- Header: Photo & Basic Info (vertical layout) -->
        <div class="fm-header">
          <div class="fm-player-photo">
            <img
              :src="playerPhoto"
              alt="Player Photo"
              @error="onPhotoError"
            />
          </div>
          <div class="fm-player-info">
            <h1 class="fm-player-name">
              {{ player.name }}
              <span v-if="player.overall_stats" class="fm-player-ovr">
                (OVR: {{ player.overall_stats }})
              </span>
            </h1>



            <div class="fm-player-details">
              <p>Age: <strong>{{ player.age }}</strong></p>
              <p>Nationality: <strong>{{ getCountryName(player.country) }}</strong></p>
              <p>
  <strong>Club:</strong>
  <span v-if="player.club">{{ player.club.name }}</span>
  <span v-else class="text-gray-500 italic">Free Agent</span>
</p>
              <p>
                Height: <strong>{{ player.height }} cm</strong>
                &nbsp;&nbsp; Weight: <strong>{{ player.weight }} kg</strong>
              </p>
              <p>Foot: <strong>{{ player.foot }}</strong></p>
              <!-- Positions (only show those defined) -->
              <p v-if="positionsList.length">
                Positions:
                <span
                  v-for="(pos, index) in positionsList"
                  :key="index"
                  class="position-badge"
                  :class="pos.type"
                >
                  {{ pos.label }}
                </span>
              </p>
              <!-- Market Value and Wage (placed right under positions) -->
<div v-if="player.market_value" class="market-value-box" :class="marketValueTier">
  <span class="market-label">Market Value</span>
  <span class="market-amount">€{{ formatMoney(player.market_value) }}</span>
</div>

<div v-if="player.wage" class="wage-box tooltip-container">
  <span class="wage-label">Wage (per season)</span>
  <span class="wage-amount">€{{ formatMoney(player.wage) }}</span>
</div>
            </div>
          </div>
        </div>

        <!-- Attributes Group (vertical layout) -->
        <div class="fm-attributes">
          <!-- Attacking Attributes -->
          <div class="attribute-group">
            <h2>Attacking</h2>
            <ul>
              <li v-for="(val, key) in attackingAttributes" :key="key">
                <span class="attr-label">{{ formatKey(key) }}</span>
                <span class="attr-value" :class="getAttributeColorClass(key, val)">
                  {{ val }}
                </span>
              </li>
            </ul>
          </div>

          <!-- Defensive Attributes -->
          <div class="attribute-group">
            <h2>Defensive</h2>
            <ul>
              <li v-for="(val, key) in defensiveAttributes" :key="key">
                <span class="attr-label">{{ formatKey(key) }}</span>
                <span class="attr-value" :class="getAttributeColorClass(key, val)">
                  {{ val }}
                </span>
              </li>
            </ul>
          </div>

          <!-- Physical Attributes -->
          <div class="attribute-group">
            <h2>Physical</h2>
            <ul>
              <li v-for="(val, key) in physicalAttributes" :key="key">
                <span class="attr-label">{{ formatKey(key) }}</span>
                <span class="attr-value" :class="getAttributeColorClass(key, val)">
                  {{ val }}
                </span>
              </li>
            </ul>
          </div>

          <!-- Goalkeeping Attributes (if available) -->
          <div v-if="Object.keys(gkAttributes).length" class="attribute-group">
            <h2>Goalkeeping</h2>
            <ul>
              <li v-for="(val, key) in gkAttributes" :key="key">
                <span class="attr-label">{{ formatKey(key) }}</span>
                <span class="attr-value" :class="getAttributeColorClass(key, val)">
                  {{ val }}
                </span>
              </li>
            </ul>
          </div>

          <!-- Misc Attributes -->
          <div v-if="Object.keys(miscAttributes).length" class="attribute-group">
            <h2>Misc</h2>
            <ul>
              <li v-for="(val, key) in miscAttributes" :key="key">
                <span class="attr-label">{{ formatKey(key) }}</span>
                <span class="attr-value" :class="getAttributeColorClass(key, val)">
                  {{ val }}
                </span>
              </li>
            </ul>
          </div>

          <!-- Special Abilities (only true) in their own box under Misc -->
          <div v-if="trueSpecialAbilities.length" class="attribute-group">
            <h2>Special Abilities</h2>
            <ul>
              <li v-for="ability in trueSpecialAbilities" :key="ability.key">
                <span class="position-badge special">
                  {{ ability.label }}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Season Stats (placed under attributes) -->
        <div class="fm-bottom">
          <h2>Season Stats</h2>
          <div class="fm-season-stats">
            <p>No matches played yet</p>
          </div>
        </div>

        <!-- Back to Players Link -->
        <div class="back-link">
          <router-link to="/players">← Back to Players</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import countryMapping from "@/utils/countryMapping.js";

export default {
  name: "PlayerOverviewFM",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      player: null,
      loading: false,
      error: null,
      defaultPhoto: "https://www.fmsite.net/applications/downloads/interface/legacy/screenshot.php?path=/monthly_2019_11/player.png.0ecd34de36fceb1d0261db9daccf69e3.png",
      countryMapping,
    };
  },
  created() {
    this.fetchPlayer();
  },
  computed: {
    playerPhoto() {
      if (this.player && this.player.id) {
        return `/players/${this.player.id}.png`;
      }
      return this.defaultPhoto;
    },
    positionsList() {
      if (!this.player) return [];
      const positions = ["gk", "cb", "lb", "rb", "dmf", "cmf", "lmf", "rmf", "amf", "lwf", "rwf", "ss", "cf"];
      return positions
        .filter((pos) => this.player[pos] && this.player[pos].toLowerCase() !== "hidden")
        .map((pos) => ({
          label: pos.toUpperCase(),
          type: this.player[pos].toLowerCase(),
        }));
    },
    marketValueTier() {
      const val = this.player?.market_value || 0;
      if (val >= 100_000_000) return "mv-purple";
      if (val >= 20_000_000) return "mv-green";
      if (val >= 5_000_000) return "mv-yellow";
      return "mv-gray";
    },
    attackingAttributes() {
      const p = this.player || {};
      return this.pickDefined({
        offensive_awareness: p.offensive_awareness,
        ball_control: p.ball_control,
        dribbling: p.dribbling,
        tight_possession: p.tight_possession,
        low_pass: p.low_pass,
        lofted_pass: p.lofted_pass,
        finishing: p.finishing,
        heading: p.heading,
        place_kicking: p.place_kicking,
        curl: p.curl,
      });
    },
    defensiveAttributes() {
      const p = this.player || {};
      return this.pickDefined({
        defensive_awareness: p.defensive_awareness,
        ball_winning: p.ball_winning,
        aggression: p.aggression,
      });
    },
    physicalAttributes() {
      const p = this.player || {};
      return this.pickDefined({
        speed: p.speed,
        stamina: p.stamina,
        kicking_power: p.kicking_power,
        jump: p.jump,
        physical_contact: p.physical_contact,
        balance: p.balance,
        acceleration: p.acceleration,
      });
    },
    gkAttributes() {
      const p = this.player || {};
      return this.pickDefined({
        gk_awareness: p.gk_awareness,
        gk_catching: p.gk_catching,
        gk_clearing: p.gk_clearing,
        gk_reflexes: p.gk_reflexes,
        gk_reach: p.gk_reach,
      });
    },
    miscAttributes() {
      const p = this.player || {};
      return this.pickDefined({
        weak_foot_usage: p.weak_foot_usage,
        weak_foot_accuracy: p.weak_foot_accuracy,
        form: p.form,
        injury_resistance: p.injury_resistance,
      });
    },
    trueSpecialAbilities() {
      if (!this.player) return [];
      const keys = [ /* same as before */ ];
      return keys
        .filter((key) => this.player[key] === true)
        .map((key) => ({ key, label: this.formatKey(key) }));
    }
  },
  methods: {
  async fetchPlayer() {
    this.loading = true;
    try {
      const response = await axios.get(`http://localhost:8000/players/players/${this.id}`);
      this.player = response.data;
    } catch (error) {
      console.error("Error fetching player:", error);
      this.error = "Failed to load player details.";
    } finally {
      this.loading = false;
    }
  },
  formatKey(key) {
    return key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
  },
  formatMoney(value) {
  if (isNaN(value)) return value;
  if (value >= 1_000_000_000) return (value / 1_000_000_000).toFixed(1) + "B";
  if (value >= 1_000_000) return (value / 1_000_000).toFixed(1) + "M";
  if (value >= 1_000) return (value / 1_000).toFixed(1) + "K";
  return value.toLocaleString();
}
,
  estimateWage(value) {
    if (value < 5_000_000) return 3000 + Math.floor(value / 500_000) * 250;
    if (value < 20_000_000) return 7000 + Math.floor(value / 1_000_000) * 350;
    if (value < 100_000_000) return 20000 + Math.floor(value / 2_000_000) * 450;
    return 100000 + Math.floor(value / 10_000_000) * 1500;
  },
  pickDefined(obj) {
    const result = {};
    Object.entries(obj).forEach(([k, v]) => {
      if (v !== undefined && v !== null) {
        result[k] = v;
      }
    });
    return result;
  },
  onPhotoError(event) {
    event.target.src = this.defaultPhoto;
  },
  getCountryName(code) {
    return this.countryMapping[code] || "Unknown";
  },
  getClubName(player) {
    return player.club?.name || "Free Agent";
  },
  getAttributeColorClass(key, value) {
    if (isNaN(value)) return "";
    if (key === "weak_foot_usage" || key === "weak_foot_accuracy") {
      return this.colorForScale(value, 4);
    }
    if (key === "form") {
      const val = Number(value);
      const ratio = val / 8;
      if (ratio >= 0.75) return "attr-green";
      if (ratio >= 0.5) return "attr-yellow";
      return "attr-red";
    }
    return this.colorForScale(value, 99);
  },
  colorForScale(value, max) {
    const val = Number(value);
    if (isNaN(val)) return "";
    const ratio = val / max;
    if (ratio >= 0.85) return "attr-green";
    if (ratio >= 0.65) return "attr-yellow";
    return "attr-red";
  }
  }
};
</script>



<style>
html, body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: #1f1f1f;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
body {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px 20px;
}
.player-overview-fm {
  width: 90%;
  max-width: 2400px;
  margin: 2rem auto;
  perspective: 1000px;
}
/* Floating box effect styles */
.floating-box {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 4rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  color: #f0f0f0;
  transform-style: preserve-3d;
  animation: none;
  position: relative;
  z-index: 1;
}
@keyframes float {
  0%, 100% {
    transform: translateY(0) rotateX(0.5deg) rotateY(0.5deg);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  }
  50% {
    transform: translateY(-20px) rotateX(-0.5deg) rotateY(-0.5deg);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
  }
}
/* Rest of your existing CSS remains unchanged */
.fm-content {
  display: block;
}
.fm-header {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 4rem;
  text-align: center;
}
.fm-player-photo img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 50%;
  border: 5px solid #ffcc66;
}
.fm-player-name {
  font-size: 4rem;
  margin: 0 0 1rem 0;
  color: #ffcc66;
}
.fm-player-ovr {
  font-size: 3rem;
  color: #fff;
}
.fm-player-details p {
  font-size: 2rem;
  margin: 0.5rem 0;
}
.position-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 1.8rem;
  display: inline-block;
  margin-right: 4px;
  margin-bottom: 4px;
}
.position-badge.natural {
  background-color: #2ecc71;
  color: #fff;
}
.position-badge.experienced {
  background-color: #f1c40f;
  color: #333;
}
.fm-attributes {
  display: block;
  margin-bottom: 4rem;
}
.attribute-group {
  background-color: #2f2f2f;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.attribute-group h2 {
  font-size: 2.4rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.attribute-group ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.attribute-group li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.attr-label {
  font-size: 1.8rem;
  flex: 1;
}
.attr-value {
  font-size: 1.8rem;
  font-weight: bold;
}
.attr-green, .attr-green .attr-value { color: #27ae60; }
.attr-yellow, .attr-yellow .attr-value { color: #f1c40f; }
.attr-red, .attr-red .attr-value { color: #c0392b; }
.attribute-group.special-abilities h2 {
  font-size: 2.4rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.attribute-group.special-abilities ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}
.position-badge.special {
  font-size: 1.8rem;
  padding: 6px 12px;
  background-color: #3498db;
  color: #fff;
  border-radius: 4px;
}
.fm-bottom {
  text-align: center;
  margin-top: 4rem;
  padding-top: 3rem;
  border-top: 1px solid #444;
}
.fm-season-stats {
  font-size: 1.8rem;
  margin-top: 1rem;
}
.back-link {
  margin-top: 4rem;
  text-align: center;
}
.tooltip-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.tooltip-content {
  display: none;
  position: absolute;
  top: 130%;
  left: 0;
  z-index: 999;
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 10px 14px;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 1.6rem;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.tooltip-container:hover .tooltip-content {
  display: block;
  opacity: 1;
}

.market-value-box {
  display: inline-block;
  font-size: 1.8rem;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 8px;
  margin-top: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s;
}

.wage-box {
  display: inline-block;
  font-size: 1.8rem;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 8px;
  margin-top: 1rem;
  margin-left: 1rem;
  background-color: #34495e;
  color: #ecf0f1;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s;
}

.wage-label {
  margin-right: 12px;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.wage-amount {
  font-size: 2rem;
}

.market-label {
  margin-right: 12px;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.market-amount {
  font-size: 2rem;
}

/* Tier-based colors */
.mv-gray   { background-color: #7f8c8d; color: white; }
.mv-yellow { background-color: #f1c40f; color: #333; }
.mv-green  { background-color: #27ae60; color: white; }
.mv-purple { background-color: #8e44ad; color: white; }

.back-link a {
  font-size: 2rem;
  color: #3498db;
  text-decoration: none;
  transition: color 0.2s;
  padding: 1rem 2rem;
  border-radius: 5px;
}
.back-link a:hover {
  color: #2980b9;
  background: rgba(52, 152, 219, 0.1);
}
@media (max-width: 1600px) {
  .player-overview-fm {
    max-width: 1800px;
    padding: 3rem;
  }
  .fm-player-photo img {
    width: 200px;
    height: 200px;
  }
}
@media (max-width: 1200px) {
  .fm-header {
    gap: 1rem;
  }
  .fm-player-name {
    font-size: 3.5rem;
  }
}
@media (max-width: 768px) {
  .player-overview-fm {
    padding: 2rem;
  }
  .attribute-group {
    margin-bottom: 1.5rem;
  }
  .position-badge {
    font-size: 1.6rem;
    padding: 4px 8px;
  }
}
</style>