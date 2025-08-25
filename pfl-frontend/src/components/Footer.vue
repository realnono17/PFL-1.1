<template>
  <footer>
    <p>&copy; 2025 Pirate Football League</p>
    <nav>
      <a href="https://twitter.com/pfl" target="_blank">Twitter</a>
      <a href="https://twitch.tv/pfl" target="_blank">Twitch</a>
      <a href="/about">About</a>
    </nav>
  </footer>
</template>

<style scoped>
footer {
  background: #161b22;
  color: gray;
  position: fixed;
  bottom: 0;
  width: 100%;
  /* Use Flexbox to center content both horizontally & vertically */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /* Increase padding & font size for a bigger look */
  padding: 2rem 0;
  font-size: 2rem; /* Increase font size */
  text-align: center;
}

/* Remove default margins to keep things tightly spaced */
footer p {
  margin: 0;
}

/* Add a bit of space between the text and the nav links */
footer nav {
  margin-top: 1rem;
}

/* Style links with increased spacing and color */
footer a {
  color: white;
  margin: 0 1.5rem; /* Increase horizontal spacing */
  text-decoration: none;
}

/* Hover effect for links */
footer a:hover {
  color: #fbbf24;
}
</style>
