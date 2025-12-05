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
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="item in inventory"
        :key="item.ingredient_id"
      >
        <td>{{ item.name }}</td>
        <td>{{ item.category }}</td>
        <td :class="{ low: item.amount < item.min_amount }">
          {{ item.amount }}
        </td>
        <td>{{ item.unit }}</td>
        <td>{{ item.min_amount }}</td>
        <td>{{ item.expiration_date || '—' }}</td>
        <td>
          <button @click="openSupply(item)">Поставка</button>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Простая модалка для оформления поставки -->
  <div v-if="selected" class="modal">
    <div class="modal-content">
      <h3>Поставка: {{ selected.name }}</h3>

      <label>Количество</label>
      <input
        v-model.number="amount"
        type="number"
        min="0"
        step="0.1"
      />

      <label>Комментарий</label>
      <input
        v-model="comment"
        type="text"
        placeholder="Необязательно"
      />

      <div class="actions">
        <button @click="submitSupply">Сохранить</button>
        <button @click="closeSupply">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  inventory: {
    type: Array,
    required: true
  },
  // id ресторана, для которого показываем инвентарь
  restaurantId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['updated'])

const selected = ref(null)
const amount = ref(0)
const comment = ref('')

function openSupply(item) {
  selected.value = item
  amount.value = 0
  comment.value = ''
}

function closeSupply() {
  selected.value = null
}

async function submitSupply() {
  if (!selected.value) return
  if (!amount.value || amount.value <= 0) {
    alert('Введите количество > 0')
    return
  }

  try {
    const res = await fetch('/api/operations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        restaurant_id: props.restaurantId,
        ingredient_id: selected.value.ingredient_id,
        op_type: 'IN', // ПРИХОД
        amount: amount.value,
        comment: comment.value || null
      })
    })

    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || 'Ошибка сервера')
    }

    // говорим родителю: "данные изменились, перезагрузи инвентарь"
    emit('updated')
    closeSupply()
  } catch (e) {
    console.error(e)
    alert('Не удалось создать поставку')
  }
}
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

/* простая модалка */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 1rem;
  border-radius: 6px;
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}
</style>
