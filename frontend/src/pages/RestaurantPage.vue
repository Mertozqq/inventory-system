<template>
  <div>
    <h2>Ресторан №{{ restaurantId }}</h2>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error" class="error">
      Ошибка: {{ error }}
    </div>

    <!-- Таблица остатков -->
    <InventoryTable
      v-else
      :inventory="inventory"
      :restaurant-id="restaurantId"
      @updated="loadInventory"
    />

    <h3>Оформить операцию</h3>

    <form @submit.prevent="submitOperation" class="op-form">
      <label>
        Ингредиент:
        <select v-model="form.ingredient_id" required>
          <option
            v-for="item in inventory"
            :key="item.ingredient_id"
            :value="item.ingredient_id"
          >
            {{ item.name }}
          </option>
        </select>
      </label>

      <label>
        Тип:
        <select v-model="form.op_type">
          <option value="IN">Приход</option>
          <option value="OUT">Расход</option>
        </select>
      </label>

      <label>
        Количество:
        <input
          type="number"
          v-model.number="form.amount"
          min="0.1"
          step="0.1"
          required
        />
      </label>

      <label>
        Комментарий:
        <input type="text" v-model="form.comment" />
      </label>

      <button type="submit">Записать операцию</button>
    </form>

    <div v-if="operationMessage" class="message">
      {{ operationMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import InventoryTable from "../components/InventoryTable.vue";

const restaurantId = Number(window.location.hash.split("/")[2]);

const inventory = ref([]);
const loading = ref(true);
const error = ref(null);
const operationMessage = ref("");

// Форма операции
const form = ref({
  ingredient_id: null,
  op_type: "IN",   // 👈 по умолчанию ПРИХОД, в верхнем регистре
  amount: 1,
  comment: ""
});

// Загрузка склада ресторана
async function loadInventory() {
  try {
    loading.value = true;
    const res = await fetch(`/api/inventory/${restaurantId}`);
    if (!res.ok) throw new Error("Не удалось загрузить склад");

    const data = await res.json();
    inventory.value = data;

    if (!form.value.ingredient_id && data.length > 0) {
      form.value.ingredient_id = data[0].ingredient_id;
    }
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

// Отправка операции
async function submitOperation() {
  const payload = {
    restaurant_id: restaurantId,
    ingredient_id: form.value.ingredient_id,
    op_type: form.value.op_type,  // уже "IN" или "OUT"
    amount: form.value.amount,
    comment: form.value.comment
  };

  const res = await fetch("/api/operations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const txt = await res.text();
    console.error("Ошибка операции:", txt);
    operationMessage.value = "Ошибка выполнения операции";
    return;
  }

  operationMessage.value = "Операция выполнена успешно!";
  form.value.comment = "";
  await loadInventory();
}
  
onMounted(loadInventory);
</script>

<style scoped>
.error {
  color: red;
  margin-bottom: 1rem;
}

.op-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 320px;
  margin-top: 1rem;
}

.op-form input,
.op-form select {
  padding: 5px;
}

button {
  padding: 6px 12px;
  cursor: pointer;
}

.message {
  margin-top: 1rem;
  color: green;
}
</style>
