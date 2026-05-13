<template>
  <div class="players-page">
    <!-- Page Header & Basic Search -->
    <div class="page-header">
      <h1>Players Database</h1>
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search players by name..."
          class="basic-search"
        />
        <button class="advanced-search-button" @click="toggleAdvanced">
          Advanced Search
        </button>
      </div>
    </div>

    <!-- Advanced Search Panel -->
    <div v-if="showAdvanced" class="advanced-options">
      <div class="advanced-grid">
        <!-- Text Filters Card -->
        <div class="filter-card">
          <h2>Text Filters</h2>
          <div class="filter-buttons">
            <div
              v-for="(filter, index) in advancedTextFilters"
              :key="filter.field"
              class="text-filter-item"
            >
              <button
                :class="{ active: filter.active && filter.text.trim() !== '' }"
                @click.prevent="toggleTextFilter(index)"
              >
                {{ filter.label }}
              </button>
              <div v-if="filter.active" class="input-wrapper">
                <input
                  type="text"
                  v-model="filter.text"
                  :placeholder="filter.placeholder"
                  @input="applyTextFilter"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Position Filter Card -->
        <div class="filter-card">
          <h2>Position Filter</h2>
          <div class="toggle-buttons">
            <button
              v-for="pos in availablePositions"
              :key="pos"
              :class="{ selected: advancedPositions.includes(pos) }"
              @click.prevent="togglePosition(pos)"
            >
              {{ pos }}
            </button>
          </div>
        </div>

        <!-- Numeric Filters Card -->
        <div class="filter-card">
          <h2>Numeric Filters</h2>
          <div class="numeric-filters">
            <div
              v-for="filter in advancedNumericFilters"
              :key="filter.field"
              class="numeric-filter"
            >
              <button
                class="numeric-toggle"
                :class="{ active: numericFilters[filter.field].active }"
                @click.prevent="toggleNumeric(filter.field)"
              >
                {{ filter.label }}
              </button>
              <div v-if="numericFilters[filter.field].active" class="numeric-inputs">
                <input
                  type="number"
                  v-model.number="numericFilters[filter.field].min"
                  placeholder="Min"
                />
                <span class="range-separator">-</span>
                <input
                  type="number"
                  v-model.number="numericFilters[filter.field].max"
                  placeholder="Max"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Boolean Skill Filters Card -->
        <div class="filter-card">
          <h2>Boolean Skill Filters</h2>
          <div class="toggle-buttons">
            <button
              v-for="skill in advancedBooleanFilters"
              :key="skill.field"
              :class="{ selected: advancedBooleans.includes(skill.field) }"
              @click.prevent="toggleBooleanSkill(skill.field)"
            >
              {{ skill.label }}
            </button>
          </div>
        </div>
      </div>
      <div class="clear-row">
        <button class="clear-button" @click="clearFilters">
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Data Table -->
    <div v-if="loading" class="loading">Loading players...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>OVR</th>
            <th>Country</th>
            <th>Age</th>
            <th>Position</th>
            <th>Team</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="player in filteredPlayers"
            :key="player.id"
            @mouseover="hoveredRow = player.id"
            @mouseleave="hoveredRow = null"
            :class="{ hovered: hoveredRow === player.id }"
          >
            <td>{{ player.id }}</td>
            <td>
              <router-link :to="'/players/' + player.id" class="player-link">
                {{ player.name }}
              </router-link>
            </td>
            <td>{{ player.overall_stats }}</td>
            <td>{{ getCountryName(player.country) }}</td>
            <td>{{ player.age }}</td>
            <td>
              <span
                v-for="pos in getPositionsList(player)"
                :key="pos.label"
                :class="['position-badge', pos.type]"
              >
                {{ pos.label }}
              </span>
            </td>
            <td>{{ getTeamName(player) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-controls">
      <button
        v-if="players.length === limit"
        @click="showNext"
        class="pagination-button"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import countryMapping from "@/utils/countryMapping.js";
import advancedNumericFilters from "@/utils/advancedNumericFilters.js";
import advancedBooleanFilters from "@/utils/advancedBooleanFilters.js";

export default {
  name: "Players",
  data() {
    return {
      players: [],
      loading: true,
      error: null,
      hoveredRow: null,
      skip: 0,
      limit: 25,
      searchQuery: "",
      showAdvanced: false,
      // Advanced Text Filters (now including four filters)
      advancedTextFilters: [
        {
          field: "advancedName",
          label: "Name",
          placeholder: "Player name...",
          active: false,
          text: "",
        },
        {
          field: "advancedCountry",
          label: "Country",
          placeholder: "Country name...",
          active: false,
          text: "",
        },
        {
          field: "advancedFoot",
          label: "Foot",
          placeholder: "Left or Right...",
          active: false,
          text: "",
        },
        {
          field: "advancedTeam",
          label: "Team",
          placeholder: "Team name...",
          active: false,
          text: "",
        },
      ],
      advancedNumericFilters,
      numericFilters: {},
      advancedPositions: [],
      availablePositions: [
        "GK",
        "CB",
        "LB",
        "RB",
        "DMF",
        "CMF",
        "LMF",
        "RMF",
        "AMF",
        "LWF",
        "RWF",
        "SS",
        "CF",
      ],
      advancedBooleanFilters,
      advancedBooleans: [],
      countryMapping,
    };
  },
  created() {
    // Initialize numeric filters for each numeric field
    this.advancedNumericFilters.forEach((filter) => {
      this.numericFilters[filter.field] = { min: null, max: null, active: false };
    });
    this.fetchPlayers();
  },
  computed: {
    filteredPlayers() {
      let result = this.players;
      // Basic search (searchQuery)
      result = result.filter((player) =>
        player.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      if (this.showAdvanced) {
        // Apply each text filter if active and has value
        this.advancedTextFilters.forEach((filter) => {
          if (filter.active && filter.text.trim() !== "") {
            if (filter.field === "advancedName") {
              result = result.filter((player) =>
                player.name.toLowerCase().includes(filter.text.toLowerCase())
              );
            } else if (filter.field === "advancedCountry") {
              result = result.filter((player) => {
                const countryName = this.getCountryName(player.country).toLowerCase();
                return countryName.includes(filter.text.toLowerCase());
              });
            } else if (filter.field === "advancedFoot") {
              result = result.filter((player) =>
                player.foot &&
                player.foot.toLowerCase().includes(filter.text.toLowerCase())
              );
            } else if (filter.field === "advancedTeam") {
              result = result.filter((player) => {
                const team = player.club && player.club.name ? player.club.name.toLowerCase() : "";
                return team.includes(filter.text.toLowerCase());
              });
            }
          }
        });
        // Numeric Filters
        this.advancedNumericFilters.forEach((filter) => {
          const { min, max, active } = this.numericFilters[filter.field];
          if (active && (min !== null || max !== null)) {
            result = result.filter((player) => {
              const val = Number(player[filter.field]);
              if (isNaN(val)) return false;
              if (min !== null && max !== null) return val >= min && val <= max;
              if (min !== null) return val >= min;
              if (max !== null) return val <= max;
              return true;
            });
          }
        });
        // Position Filter
        if (this.advancedPositions.length > 0) {
          result = result.filter((player) => {
            const positions = this.getPositionsList(player).map((p) => p.label);
            return this.advancedPositions.some((pos) => positions.includes(pos));
          });
        }
        // Boolean Skill Filters
        if (this.advancedBooleans.length > 0) {
          result = result.filter((player) =>
            this.advancedBooleans.every((skill) => player[skill] === true)
          );
        }
      }
      return result;
    },
  },
  methods: {
    fetchPlayers() {
      this.loading = true;
      this.error = null;
      axios
        .get("http://localhost:8000/players", {
          params: { skip: this.skip, limit: this.limit },
        })
        .then((response) => {
          this.players = response.data;
        })
        .catch((error) => {
          console.error("Error fetching players:", error);
          this.error = "Failed to load players. Please try again later.";
        })
        .finally(() => {
          this.loading = false;
        });
    },
    showNext() {
      this.skip += this.limit;
      this.fetchPlayers();
    },
    toggleAdvanced() {
      this.showAdvanced = !this.showAdvanced;
    },
    toggleTextFilter(index) {
      this.advancedTextFilters[index].active = !this.advancedTextFilters[index].active;
      if (!this.advancedTextFilters[index].active) {
        this.advancedTextFilters[index].text = "";
      }
    },
    applyTextFilter() {
      // Reactive filtering happens automatically.
      console.log("Text filters updated:", this.advancedTextFilters);
    },
    togglePosition(pos) {
      const index = this.advancedPositions.indexOf(pos);
      if (index > -1) {
        this.advancedPositions.splice(index, 1);
      } else {
        this.advancedPositions.push(pos);
      }
    },
    toggleBooleanSkill(skill) {
      const index = this.advancedBooleans.indexOf(skill);
      if (index > -1) {
        this.advancedBooleans.splice(index, 1);
      } else {
        this.advancedBooleans.push(skill);
      }
    },
    toggleNumeric(field) {
      this.numericFilters[field].active = !this.numericFilters[field].active;
      if (!this.numericFilters[field].active) {
        this.numericFilters[field].min = null;
        this.numericFilters[field].max = null;
      }
    },
    clearFilters() {
      // Clear text filters
      this.advancedTextFilters.forEach((filter) => {
        filter.active = false;
        filter.text = "";
      });
      // Clear numeric filters
      this.advancedNumericFilters.forEach((filter) => {
        this.numericFilters[filter.field].min = null;
        this.numericFilters[filter.field].max = null;
        this.numericFilters[filter.field].active = false;
      });
      // Clear positions and boolean filters
      this.advancedPositions = [];
      this.advancedBooleans = [];
    },
    getCountryName(code) {
      return this.countryMapping[code] || code;
    },
    getPositionsList(player) {
      const positions = [
        "gk",
        "cb",
        "lb",
        "rb",
        "dmf",
        "cmf",
        "lmf",
        "rmf",
        "amf",
        "lwf",
        "rwf",
        "ss",
        "cf"
      ];
      const posList = [];
      positions.forEach((pos) => {
        const value = player[pos];
        if (value && value.toLowerCase() !== "hidden") {
          let type = value.toLowerCase(); // expected "natural" or "experienced"
          posList.push({ label: pos.toUpperCase(), type });
        }
      });
      return posList;
    },
    getTeamName(player) {
      return player.club && player.club.name ? player.club.name : "Free Agent";
    },
  },
};
</script>

<style scoped>
/* Overall Layout */
.players-page {
  margin-top: 12rem;
  padding: 2rem;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  color: #fff;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}
.page-header h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #ffcc66, #f6b93b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto 1rem;
}
.basic-search {
  width: 50%;
  padding: 1rem 1.5rem;
  font-size: 1.8rem;
  border: none;
  border-radius: 8px;
  background-color: #fff;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}
.advanced-search-button {
  padding: 1rem 2rem;
  font-size: 1.8rem;
  background-color: #ffcc66;
  color: #161b22;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.advanced-search-button:hover {
  background-color: #e6b84f;
}

/* Advanced Options Panel: Centered with fixed max width */
.advanced-options {
  width: 100%;
  background-color: #20262e;
  padding: 2rem;
  border: 1px solid #2f3b45;
  margin-bottom: 2rem;
  box-sizing: border-box;
}
.advanced-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Filter Card */
.filter-card {
  background-color: #2f3b45;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  width: 100%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  text-align: left;
}
.filter-card h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #ffcc66;
}

/* Text Filters */
.filter-buttons {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}
.text-filter-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.text-filter-item button {
  padding: 0.6rem 1rem;
  font-size: 1.6rem;
  border: 1px solid #ffcc66;
  border-radius: 6px;
  background: transparent;
  color: #ffcc66;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.text-filter-item button.active {
  background-color: red;
  color: #fff;
}
.input-wrapper {
  margin-top: 0.5rem;
}
.input-wrapper input {
  width: 150px;
  padding: 0.5rem;
  font-size: 1.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Numeric Filters */
.numeric-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}
.numeric-filter {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.numeric-toggle {
  padding: 0.6rem 1rem;
  font-size: 1.6rem;
  border: 1px solid #ffcc66;
  border-radius: 6px;
  background: transparent;
  color: #ffcc66;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.numeric-toggle.active {
  background-color: #ffcc66;
  color: #161b22;
}
.numeric-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.numeric-inputs input {
  width: 80px;
  padding: 0.5rem;
  font-size: 1.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.range-separator {
  font-size: 1.6rem;
}

/* Toggle Buttons for Positions & Boolean Skills */
.toggle-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}
.toggle-buttons button {
  padding: 0.6rem 1rem;
  font-size: 1.6rem;
  border: 1px solid #ffcc66;
  border-radius: 6px;
  background: transparent;
  color: #ffcc66;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.toggle-buttons button.selected {
  background-color: #ffcc66;
  color: #161b22;
}

/* Clear Filters Button */
.clear-row {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
.clear-button {
  padding: 1rem 2rem;
  font-size: 1.8rem;
  background-color: #e63946;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.clear-button:hover {
  background-color: #c62828;
}

/* Table Container */
.table-container {
  overflow-x: auto;
  background: #161b22;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(255, 204, 102, 0.2);
  margin-bottom: 2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}
thead {
  background-color: #20262e;
  text-transform: uppercase;
}
th {
  padding: 1rem;
  text-align: left;
  font-size: 1.8rem;
  color: #ffcc66;
  border-bottom: 2px solid #2f3b45;
}
tbody tr {
  transition: background-color 0.2s ease;
}
tbody tr:nth-child(even) {
  background-color: #1c2128;
}
tbody tr:nth-child(odd) {
  background-color: #242b34;
}
td {
  padding: 1rem;
  border-bottom: 1px solid #2f3b45;
  font-size: 1.6rem;
}
.hovered {
  background-color: #2f3b45 !important;
  cursor: pointer;
}
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
}
.pagination-button {
  background-color: #ffcc66;
  color: #161b22;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.6rem;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.pagination-button:hover {
  background-color: #e6b84f;
}
.position-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  margin-right: 0.3rem;
  border-radius: 4px;
  font-size: 1.4rem;
  font-weight: bold;
}
.position-badge.natural {
  background-color: #2ecc71;
  color: #fff;
}
.position-badge.experienced {
  background-color: #f1c40f;
  color: #333;
}
.player-link {
  color: #ffcc66;             /* Match your table’s accent color */
  text-decoration: none;      /* Remove underline */
  font-weight: bold;          /* Make it stand out */
  transition: color 0.3s ease;
}

.player-link:hover {
  color: #ffd580;             /* Slightly lighter or darker on hover */
  text-decoration: underline; /* Or keep it none if you prefer no underline */
}

</style>
