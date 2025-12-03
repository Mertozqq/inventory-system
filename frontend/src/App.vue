<template>
  <div class="app-container">
    <header>
      <h1>Система управления запасами</h1>
      <nav>
        <a href="#/">Сводка</a>
        <a href="#/inventory">Склад</a>
        <a href="#/restaurants">Рестораны</a>
      </nav>
    </header>

    <main>
      <component :is="currentView" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dashboard from './pages/Dashboard.vue'
import StockPage from './pages/StockPage.vue'
import RestaurantList from './pages/RestaurantList.vue'
import NotFound from './pages/NotFound.vue'

// Простая hash-навигация
const route = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  route.value = window.location.hash
})

const currentView = computed(() => {
  switch (route.value) {
    case '#/':
    case '':
      return Dashboard
    case '#/inventory':
      return StockPage
    case '#/restaurants':
      return RestaurantList
    default:
      return NotFound
  }
})
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
.app-container {
  padding: 1rem;
}
header {
  background-color: #f8f8f8;
  padding: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
}
nav a {
  margin-right: 1rem;
  text-decoration: none;
  color: #333;
}
nav a:hover {
  text-decoration: underline;
}
</style>
