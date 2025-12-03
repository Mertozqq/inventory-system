<template>
  <div class="alerts">
    <h3>Скоро истекают сроки годности</h3>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error" class="error">Ошибка: {{ error }}</div>
    <ul v-else>
      <li v-for="item in items" :key="item.name + '-' + item.restaurant_id">
        {{ item.name }} (ресторан #{{ item.restaurant_id }}): до {{ item.expiration_date || '—' }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/analytics/expiring')
    if (!res.ok) throw new Error('Ошибка при получении данных')
    items.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.alerts {
  margin-top: 2rem;
  background: #fff3cd;
  border: 1px solid #ffeeba;
  padding: 1rem;
  border-radius: 8px;
}
.error {
  color: red;
}
ul {
  list-style: none;
  padding-left: 0;
}
li {
  margin-bottom: 0.5rem;
}
</style>
