<script setup>
    import { ref, onMounted } from 'vue'
    import { useRoute } from 'vue-router'
    
    const players = ref([])
    const route = useRoute()
    
    onMounted(async () => {
      const clubId = route.params.id
      const res = await fetch(`http://127.0.0.1:8000/clubs/clubs/${clubId}/players`)
      if (res.ok) {
        players.value = await res.json()
      }
    })
    
    function getPositionsList(player) {
      const positions = [
        "gk", "cb", "lb", "rb", "dmf", "cmf", "lmf", "rmf", "amf", "lwf", "rwf", "ss", "cf"
      ]
      const posList = []
      positions.forEach(pos => {
        const val = player[pos]
        if (val && val.toLowerCase() !== "hidden") {
          posList.push({ label: pos.toUpperCase(), type: val.toLowerCase() })
        }
      })
      return posList
    }
    </script>
    
    <template>
      <div class="players-page">
        <h1 class="page-title">Club Players</h1>
    
        <div v-if="players.length === 0" class="empty-msg">This club has no players.</div>
    
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>OVR</th>
                <th>Age</th>
                <th>Position</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="player in players"
                :key="player.id"
              >
                <td>{{ player.id }}</td>
                <td>
                  <router-link :to="'/players/' + player.id" class="player-link">
                    {{ player.name }}
                  </router-link>
                </td>
                <td>{{ player.overall_stats || '—' }}</td>
                <td>{{ player.age || '—' }}</td>
                <td>
                  <span
                    v-for="pos in getPositionsList(player)"
                    :key="pos.label"
                    :class="['position-badge', pos.type]"
                  >
                    {{ pos.label }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
    
    <style scoped>
    .players-page {
      margin-top: 10rem;
      padding: 2rem;
      max-width: 1200px;
      margin-left: auto;
      margin-right: auto;
      color: #fff;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    .page-title {
      font-size: 3.5rem;
      color: #ffcc66;
      margin-bottom: 2rem;
      text-align: center;
    }
    
    .empty-msg {
      text-align: center;
      color: #ccc;
      font-size: 1.8rem;
    }
    
    .table-container {
      overflow-x: auto;
      background: #161b22;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(255, 204, 102, 0.2);
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 800px;
    }
    thead {
      background-color: #20262e;
      text-transform: uppercase;
    }
    th {
      padding: 1rem;
      text-align: left;
      font-size: 1.6rem;
      color: #ffcc66;
      border-bottom: 2px solid #2f3b45;
    }
    td {
      padding: 1rem;
      font-size: 1.6rem;
      border-bottom: 1px solid #2f3b45;
    }
    tbody tr:nth-child(even) {
      background-color: #1c2128;
    }
    tbody tr:nth-child(odd) {
      background-color: #242b34;
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
      color: #ffcc66;
      text-decoration: none;
      font-weight: bold;
      transition: color 0.3s ease;
    }
    .player-link:hover {
      color: #ffd580;
      text-decoration: underline;
    }
    </style>
    