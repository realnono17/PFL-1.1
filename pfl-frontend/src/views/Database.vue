<template>
  <div class="database-page">
    <h1>Players Database</h1>
    <div v-if="loading" class="loading">Loading players...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Overall Stats</th>
            <th>Country</th>
            <th>Age</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="player in players" :key="player.id">
            <td>{{ player.id }}</td>
            <td>{{ player.name }}</td>
            <td>{{ player.overall_stats }}</td>
            <td>{{ player.country }}</td>
            <td>{{ player.age }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Database",
  data() {
    return {
      players: [],
      loading: true,
      error: null,
    };
  },
  mounted() {
    // Adjust the API URL as necessary (e.g., if using a proxy or different port)
    axios
      .get("http://localhost:8000/players")
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
};
</script>

<style scoped>
.database-page {
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
}

.loading,
.error {
  font-size: 2rem;
  text-align: center;
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 2rem;
}

th,
td {
  padding: 1rem;
  border: 1px solid #ccc;
  text-align: left;
  font-size: 1.8rem;
}

th {
  background-color: #f5f5f5;
}
</style>
