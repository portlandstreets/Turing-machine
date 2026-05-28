<template>
  <div class="emulator-container">
    <h2>Машина Тьюрінга</h2>
    
    <div class="tape-view">
      <div v-for="offset in tapeWindow" :key="offset" class="tape-cell" :class="{ 'head-cell': offset === 0 }">
        {{ getSymbolAt(offset) }}
        <div v-if="offset === 0" class="head-pointer">▲</div>
      </div>
    </div>

    <div class="controls">
      <button @click="applyCode">Скинути / Завантажити</button>
      <button @click="doStep" :disabled="isHalted || isRequesting">Крок</button>
      <button @click="togglePlay" :disabled="isHalted">
        {{ isRunning ? 'Пауза' : 'Авто' }}
      </button>
      <span class="status">Стан: {{ currentState }} | Кроки: {{ steps }}</span>
    </div>

    <div class="editor-section">
      <textarea v-model="code" class="code-editor"></textarea>
      <div class="settings">
        <label>Стрічка: <input v-model="initialTape" /></label>
        <label>Старт: <input v-model="startState" /></label>
        <label>Порожнеча: <input v-model="blankSymbol" /></label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const tape = ref({});
const head = ref(0);
const currentState = ref('0');
const steps = ref(0);
const isHalted = ref(false);

const code = ref("0 0 1 R 0\n0 1 0 R 0\n0 _ _ N HALT");
const initialTape = ref("101100");
const startState = ref("0");
const blankSymbol = ref("_");

const isRequesting = ref(false);
const isRunning = ref(false);
let timer = null;

const tapeWindow = computed(() => Array.from({ length: 21 }, (_, i) => i - 10));

const getSymbolAt = (offset) => {
  const pos = head.value + offset;
  return tape.value[pos] !== undefined ? tape.value[pos] : blankSymbol.value;
};

const applyCode = () => {
  isRunning.value = false;
  clearTimeout(timer);
  
  let newTape = {};
  for (let i = 0; i < initialTape.value.length; i++) {
    newTape[i] = initialTape.value[i];
  }
  tape.value = newTape;
  head.value = 0;
  currentState.value = startState.value;
  isHalted.value = false;
  steps.value = 0;
};

const doStep = async () => {
  if (isHalted.value || isRequesting.value) return;
  
  isRequesting.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/step/', {
      tape: tape.value,
      head: head.value,
      state: currentState.value,
      blank: blankSymbol.value,
      code: code.value
    });

    tape.value = response.data.tape;
    head.value = response.data.head;
    currentState.value = response.data.state;
    isHalted.value = response.data.halted;
    
    if (!response.data.halted) {
      steps.value++;
    }
  } catch (error) {
    console.error("Помилка зв'язку з бекендом:", error);
    isHalted.value = true;
  } finally {
    isRequesting.value = false;
  }
};

const togglePlay = () => {
  if (isHalted.value) return;
  isRunning.value = !isRunning.value;
  if (isRunning.value) {
    playLoop();
  } else {
    clearTimeout(timer);
  }
};

const playLoop = async () => {
  if (isRunning.value && !isHalted.value) {
    await doStep();
    timer = setTimeout(playLoop, 300); 
  } else {
    isRunning.value = false;
  }
};

applyCode();
</script>

<style scoped>
.emulator-container { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
.tape-view { display: flex; justify-content: center; background: #2c3e50; padding: 20px; margin-bottom: 20px; border-radius: 8px;}
.tape-cell { width: 40px; height: 40px; background: white; border: 1px solid #bdc3c7; display: flex; align-items: center; justify-content: center; font-size: 20px; position: relative; font-weight: bold;}
.head-cell { background: #f1c40f; border-color: #d35400; }
.head-pointer { position: absolute; bottom: -20px; color: #e74c3c; font-size: 16px; }
.controls { display: flex; gap: 10px; margin-bottom: 20px; align-items: center; }
button { padding: 8px 16px; cursor: pointer; background: #3498db; color: white; border: none; border-radius: 4px; }
button:disabled { background: #95a5a6; cursor: not-allowed; }
.status { font-weight: bold; font-family: monospace; font-size: 16px;}
.editor-section { display: flex; gap: 20px; }
.code-editor { flex: 2; height: 150px; background: #2b2b2b; color: #a9b7c6; font-family: monospace; padding: 10px; border-radius: 4px;}
.settings { flex: 1; display: flex; flex-direction: column; gap: 10px; }
</style>