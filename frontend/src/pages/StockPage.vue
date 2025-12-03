<template>
  <div>
    <h2>Склад ресторана</h2>

    <div class="controls">
      <label for="rest-id">ID ресторана:</label>
      <input id="rest-id" type="number" v-model.number="restaurantId" @change="fetchInventory" />
    </div>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error" class="error">Ошибка: {{ error }}</div>
    <table v-else class="inventory-table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Категория</th>
          <th>Количество</th>
          <th>Ед. изм.</th>
          <th>Мин. остаток</th>
          <th>Срок годности</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in inventory" :key="item.name">
          <td>{{ item.name }}</td>
          <td>{{ item.category }}</td>
          <td :class="{ low: item.amount < item.min_amount }">{{ item.amount }}</td>
          <td>{{ item.unit }}</td>
          <td>{{ item.min_amount }}</td>
          <td>{{ item.expiration_date || '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const restaurantId = ref(1)
const inventory = ref([])
const loading = ref(false)
const error = ref(null)

async function fetchInventory() {
  if (!restaurantId.value) return
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`/api/inventory/${restaurantId.value}`)
    if (!res.ok) throw new Error('Не удалось загрузить данные')
    inventory.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Инициализируем при загрузке
fetchInventory()
</script>

<style scoped>
.controls {
  margin-bottom: 1rem;
}
input {
  margin-left: 0.5rem;
  padding: 0.3rem;
}
.inventory-table {
  width: 100%;
  border-collapse: collapse;
}
.inventory-table th,
.inventory-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: left;
}
.low {
  color: red;
  font-weight: bold;
}
.error {
  color: red;
}
</style>
