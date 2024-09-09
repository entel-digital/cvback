createWebHashHistory
<template>
  <div class="flex flex-center">
    <div class="bg-blue-5 border-radius flex flex-center column q-pa-lg" style="height: 50vh">
      <div class="column">
        <p class="q-py-lg text-center text-white barlow-bold">Cambiar contraseña</p>
        <div v-if="!responseRequest">
          <form
            @submit.prevent="resetPassword()"
            class="q-gutter-md text-center q-pa-md"
            style="min-width: 300px"
          >
            <q-input dark standard v-model="email" label="Email" lazy-rules color="white" />

            <div class="q-py-md">
              <q-btn
                label="Cambiar contraseña"
                no-caps
                type="submit"
                color="accent"
                class="full-width"
                :loading="loading"
              />
            </div>
          </form>
        </div>
        <div v-else class="q-px-xl text-center">
          <p class="text-accent barlow-bold fs-16-19">
            Te enviamos un correo para restaurar tu contraseña
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useUserStore } from '@/stores/user.js'

export default defineComponent({
  name: 'ResetPasswordIndex',
  setup() {
    const email = ref('')
    const userStore = useUserStore()
    const responseRequest = ref(false)
    const $q = useQuasar()
    const loading = ref(false)

    const clearForm = () => {
      email.value = ''
    }

    const resetPassword = async () => {
      loading.value = true
      const request = await userStore.REQUEST_PASSWORD(email.value)
      if (request === 200) {
        responseRequest.value = true
        clearForm()
      } else {
        loading.value = false
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'report_problem',
          message: request.erros[0].message
        })
      }
    }

    return {
      email,
      resetPassword,
      responseRequest,
      loading
    }
  }
})
</script>

<style lang="scss" scoped>
.border-radius {
  border-radius: 10px;
}
</style>
