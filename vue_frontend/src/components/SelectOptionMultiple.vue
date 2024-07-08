<template>
  <div class="q-gutter-md">
    <q-select
      filled
      v-model="model"
      :options="options"
      label="Multi with toggle"
      multiple
      emit-value
      map-options
    >
      <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
        <q-item v-bind="itemProps">
          <q-item-section>
            <!-- <q-item-label v-html="opt.label" /> -->
          </q-item-section>
          <q-item-section side>
            <q-toggle
              :model-value="selected"
              @update:model-value="toggleOption(opt)"
            />
          </q-item-section>
        </q-item>
      </template>
    </q-select>
  </div>
</template>
<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "SelectOptionMultiple",
  setup() {
    const date = ref(null);
    return {
      date,
    };
  },
});
</script>
