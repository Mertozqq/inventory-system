<template>
  <div>
    <h2>Список ресторанов</h2>

    <div v-if="loading">Загрузка...</div>

    <div v-else-if="error" class="error">
      Ошибка: {{ error }}
    </div>

    <table v-else class="restaurant-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Адрес</th>
          <th>Активен</th>
          <th>Кол-во позиций</th>
          <th>Последняя поставка</th>
          <th>Открыть</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="r in restaurants" :key="r.id">
          <td>{{ r.id }}</td>

          <!-- Кликабельное имя ресторана -->
          <td>
            <a :href="'#/restaurants/' + r.id">
              {{ r.name }}
            </a>
          </td>

          <td>{{ r.address }}</td>
          <td>{{ r.is_active ? "Да" : "Нет" }}</td>
          <td>{{ r.stock_count }}</td>
          <td>{{ r.last_delivery_date || "—" }}</td>

          <!-- Кнопка открыть -->
          <td>
            <button @click="openRestaurant(r.id)">
              Открыть
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

const restaurants = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const res = await fetch("/api/restaurants");
    if (!res.ok) throw new Error("Не удалось загрузить список ресторанов");

    restaurants.value = await res.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

function openRestaurant(id) {
  window.location.hash = "#/restaurants/" + id;
}
</script>


<style scoped>
.restaurant-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.restaurant-table th,
.restaurant-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}

a {
  color: #0366d6;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  padding: 4px 10px;
  cursor: pointer;
}

.error {
  color: red;
}
</style>
