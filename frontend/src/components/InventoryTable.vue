<template>
  <table class="inventory-table">
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
      <tr v-for="item in inventory" :key="item.name + '-' + item.expiration_date">
        <td>{{ item.name }}</td>
        <td>{{ item.category }}</td>
        <td :class="{ low: item.amount < item.min_amount }">{{ item.amount }}</td>
        <td>{{ item.unit }}</td>
        <td>{{ item.min_amount }}</td>
        <td>{{ item.expiration_date || '—' }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({
  inventory: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.inventory-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
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
</style>
