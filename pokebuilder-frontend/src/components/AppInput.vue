<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  hint: { type: String, default: '' },
  error: { type: String, default: '' },
  autocomplete: { type: String, default: 'off' },
  multiline: { type: Boolean, default: false },
  rows: { type: Number, default: 3 },
})
defineEmits(['update:modelValue', 'blur'])
</script>

<template>
  <label class="field" :class="{ 'has-error': error }">
    <span class="field__label">{{ label }}</span>
    <textarea
      v-if="multiline"
      class="field__input field__input--textarea"
      :rows="rows"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur', $event)"
    ></textarea>
    <input
      v-else
      class="field__input"
      :type="type"
      :value="modelValue"
      :autocomplete="autocomplete"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur', $event)"
    />
    <span class="field__bar" aria-hidden="true"></span>
    <span v-if="error" class="field__message field__message--error">{{ error }}</span>
    <span v-else-if="hint" class="field__message">{{ hint }}</span>
  </label>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: left;
}

.field__label {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.field__input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: 16px;
  padding: 8px 2px;
  outline: none;
  transition: border-color 0.2s ease;
}

.field__input::placeholder {
  color: var(--color-text-muted);
}

.field__input--textarea {
  font: inherit;
  resize: vertical;
  min-height: 76px;
  line-height: 1.5;
}

.field__bar {
  display: block;
  height: 2px;
  width: 0%;
  background: var(--color-mint);
  transition: width 0.25s ease;
}

.field__input:focus + .field__bar {
  width: 100%;
}

.field.has-error .field__bar {
  background: var(--color-coral);
  width: 100%;
}

.field.has-error .field__input {
  border-color: var(--color-coral);
}

.field__message {
  font-size: 12.5px;
  color: var(--color-text-muted);
}

.field__message--error {
  color: var(--color-coral);
}

.field__input:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: 2px;
}
</style>
