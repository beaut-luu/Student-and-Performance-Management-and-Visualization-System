<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, 'Segoe UI', 'Microsoft YaHei', sans-serif;
  background: #f5f6fa;
  color: #2c2c2c;
}
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.card {
  background: #fff;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.card h2, .card h3 { margin: 0 0 4px; }
label { display: flex; flex-direction: column; gap: 6px; font-size: 14px; color: #555; }
input, select {
  padding: 9px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}
input:focus, select:focus { border-color: #4a7dff; }
button {
  padding: 10px;
  border: none;
  border-radius: 6px;
  background: #4a7dff;
  color: #fff;
  font-size: 15px;
  cursor: pointer;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error { color: #e34d4d; font-size: 13px; margin: 0; }
.success { color: #22a06b; font-size: 13px; margin: 0; }
.tip { font-size: 13px; color: #888; text-align: center; margin: 0; }
.tip a { color: #4a7dff; text-decoration: none; }
</style>
