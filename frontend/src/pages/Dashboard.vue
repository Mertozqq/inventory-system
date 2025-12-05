<template>
  <div>
    <h2>Сводная аналитика</h2>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error" class="error">Ошибка: {{ error }}</div>
    <div v-else class="summary-cards">
      <div class="card">
        <h3>Всего позиций</h3>
        <p>{{ summary.total_items }}</p>
      </div>
      <div class="card">
        <h3>Критических остатков</h3>
        <p>{{ summary.critical_items }}</p>
      </div>
      <div class="card">
        <h3>Активных ресторанов</h3>
        <p>{{ summary.active_restaurants }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const summary = ref({})
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/analytics/summary')
    if (!res.ok) throw new Error('Ошибка загрузки данных')
    summary.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.summary-cards {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}
.card {
  flex: 1 1 200px;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  background-color: #fafafa;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}
.error {
  color: red;
}
</style>
