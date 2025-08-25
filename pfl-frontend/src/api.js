// src/api.js
import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Adjust to your backend URL

export const getFixtures = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/fixtures`);
    return response.data;
  } catch (error) {
    console.error("Error fetching fixtures:", error);
    return [];
  }
};

export const getLeagueStandings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/clubs`);
    return response.data;
  } catch (error) {
    console.error("Error fetching league standings:", error);
    return [];
  }
};
