import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// ---------- Existing functions (unchanged) ----------
export const getFixtures = async () => {
  const res = await API.get('/matches/fixtures/');
  return res.data;
};

export const getLeagueStandings = async (seasonId) => {
  const res = await API.get(`/league-standings/season/${seasonId}`);
  return res.data;
};

// ---------- New player functions ----------
export const getPlayers = async (params = {}) => {
  const res = await API.get('/players/', { params });
  return res.data;
};

export const getPlayerById = async (id) => {
  const res = await API.get(`/players/${id}`);
  return res.data;
};