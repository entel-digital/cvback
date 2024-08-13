<template>
  <div class="about">
    <h1 class="barlow-bold text-dark">Volver al home</h1>
    <div class="q-py-md">
      <q-btn
        flat
        label="Volver"
        no-caps
        type="submit"
        color="white"
        class="full-width"
        style="text-decoration: underline"
        @click="goHome()"
      />
    </div>
  </div>
</template>
<script>
import { defineComponent } from '@vue/composition-api'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const router = useRouter()

    const goHome = () => {
      router.push({ path: '/login' })
    }
    return {
      goHome
    }
  }
})
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
