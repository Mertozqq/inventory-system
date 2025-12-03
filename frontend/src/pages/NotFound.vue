<template>
  <div class="not-found">
    <h2>Страница не найдена</h2>
    <p>Вы перешли по несуществующему маршруту.</p>
    <a href="#/">Вернуться на главную</a>
  </div>
</template>

<script setup>
// Никакой логики — это просто статическая страница
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 3rem;
}
a {
  display: inline-block;
  margin-top: 1rem;
  color: #007acc;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
