createWebHashHistory
<template>
  <div class="flex flex-center">
    <div class="bg-blue-5 border-radius flex flex-center column q-pa-lg" style="height: 70vh">
      <div v-if="!showResponse" class="column">
        <p class="q-py-lg text-center text-white barlow-bold">Restaurar contraseña</p>
        <form
          @submit.prevent="resetPassword()"
          class="q-gutter-md text-center q-pa-md"
          style="min-width: 300px"
        >
          <q-input
            dark
            standard
            type="password"
            v-model="password"
            label="Nueva contraseña"
            lazy-rules
            :rules="[
              (val) => regexPassword.test(val) || 'La contraseña no cumple con los requisitos'
            ]"
          />

          <q-input
            dark
            standard
            type="password"
            v-model="password2"
            label="Repetir nueva contraseña"
            lazy-rules
            :rules="[(val) => val === password || 'Contraseñas no coinciden']"
          />

          <div class="q-py-md text-left text-white">
            Contraseña debe incluir:
            <ul>
              <li>Al menos 8 carácteres</li>
              <li>Al menos una mayúscula</li>
              <li>Al menos una minúscula</li>
              <li>Al menos un número</li>
            </ul>
          </div>
          <div class="q-pt-md q-pb-lg">
            <q-btn
              label="Restaurar"
              no-caps
              type="submit"
              color="accent"
              class="full-width"
              :loading="loading"
            />
          </div>
        </form>
      </div>
      <div v-else>
        <p>¡El cambio ha sido exitoso!</p>
        <div class="q-pt-md q-pb-lg">
          <q-btn
            label="Volver al inicio"
            no-caps
            type="submit"
            color="accent"
            class="full-width"
            @click="goHome"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useUserStore } from '@/stores/user.js'

export default defineComponent({
  name: 'SignInIndex',
  setup() {
    const password = ref('')
    const password2 = ref('')

    const router = useRouter()
    const userStore = useUserStore()

    const $q = useQuasar()
    const loading = ref(false)

    const clearForm = () => {
      password.value = ''
      password2.value = ''
    }

    const regexPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/

    const checkPass = (value) => {
      if (regexPassword.test(value)) {
        return true // La validación es exitosa
      } else {
        return 'La contraseña no cumple con los requisitos'
      }
    }

    const resetPassword = async () => {
      if (password.value !== password2.value) {
        return
      } else {
        if (regexPassword.test(password.value) && regexPassword.test(password2.value)) {
          loading.value = true
          await userStore.RESET_PASSWORD({
            key: router.currentRoute.value.params.key,
            password: password.value
          })
          loading.value = false
          router.push({ name: '/' })
          clearForm()
        }
        else {
          clearForm()
          $q.notify({
            color: 'negative',
            position: 'top',
            message: 'Ha ocurrido un error. Intente nuevamente',
          })
        }
      }
    }
    const goHome = () => {
      router.push({ path: '/login' })
    }

    return {
      password,
      password2,
      resetPassword,
      loading,
      checkPass,
      regexPassword,
      goHome
    }
  }
})
</script>

<style lang="scss" scoped>
.border-radius {
  border-radius: 10px;
}
:deep(.q-field__append.q-field__marginal.row.no-wrap.items-center.q-anchor--skip) {
  display: none;
}
</style>
