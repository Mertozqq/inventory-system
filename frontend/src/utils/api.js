const API_BASE = '/api';

// Список ресторанов
export async function fetchRestaurants() {
  const res = await fetch(`${API_BASE}/`);
  if (!res.ok) {
    throw new Error(`Ошибка загрузки ресторанов: ${res.status}`);
  }
  return res.json();
}

// Остатки по ресторану
export async function fetchInventory(restaurantId) {
  const res = await fetch(`${API_BASE}/${restaurantId}`);
  if (!res.ok) {
    throw new Error(`Ошибка загрузки склада ресторана ${restaurantId}: ${res.status}`);
  }
  return res.json();
}

// Сводка аналитики
export async function fetchSummary() {
  const res = await fetch(`${API_BASE}/summary`);
  if (!res.ok) {
    throw new Error(`Ошибка загрузки сводки: ${res.status}`);
  }
  return res.json();
}

// (если у тебя где-то используется expiring — можно добавить и это)
export async function fetchExpiring() {
  const res = await fetch(`${API_BASE}/expiring`);
  if (!res.ok) {
    throw new Error(`Ошибка загрузки списка истекающих остатков: ${res.status}`);
  }
  return res.json();
}
