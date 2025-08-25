<template>
  <header class="navbar">
    <div class="logo">
      <router-link to="/">
        <img src="@/assets/logo.png" alt="PFL Logo" />
      </router-link>
    </div>
    <nav class="nav-links">
      <router-link to="/players">Players</router-link>
      <router-link to="/teams">Teams</router-link>
      <router-link to="/matches">Matches</router-link>
      <router-link to="/login" class="cta-button">Login</router-link>
    </nav>
  </header>
</template>

<script>
export default {};
</script>

<style scoped>
.navbar {
  background: #161b22;
  width: 100%;
  padding: 3rem 6rem; /* Increased padding */
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  height: 160px; /* Doubled height */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.logo img {
  height: 120px; /* Increased logo size */
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 5rem; /* More spacing */
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 2.4rem; /* Doubled font size */
  font-weight: bold;
  transition: color 0.3s ease-in-out;
}

.nav-links a:hover {
  color: #fbbf24; /* Gold hover effect */
}

.cta-button {
  background: #ffcc66;
  color: #111;
  padding: 18px 36px; /* Doubled padding */
  border-radius: 8px;
  text-decoration: none;
  font-size: 2.4rem; /* Doubled font size */
  font-weight: bold;
  transition: background 0.3s ease-in-out;
}

.cta-button:hover {
  background: #e6b800;
}

/* Responsive Styles */
@media (max-width: 1440px) {
  .navbar {
    height: 140px;
    padding: 2.5rem 5rem;
  }
  .logo img {
    height: 100px;
  }
  .nav-links {
    gap: 4rem;
  }
  .nav-links a {
    font-size: 2rem;
  }
  .cta-button {
    padding: 16px 32px;
    font-size: 2rem;
  }
}

@media (max-width: 1024px) {
  .navbar {
    height: 120px;
    padding: 2rem 4rem;
  }
  .logo img {
    height: 90px;
  }
  .nav-links {
    gap: 3rem;
  }
  .nav-links a {
    font-size: 1.8rem;
  }
  .cta-button {
    padding: 14px 28px;
    font-size: 1.8rem;
  }
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 2rem;
  }
  .logo img {
    height: 80px;
  }
  .nav-links {
    margin-top: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  .nav-links a {
    font-size: 1.6rem;
  }
  .cta-button {
    padding: 12px 24px;
    font-size: 1.6rem;
  }
}
</style>
