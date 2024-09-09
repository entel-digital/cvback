createWebHashHistory
<template>
  <div class="flex flex-center">
    <div class="bg-blue-5 border-radius flex flex-center column q-pa-lg" style="height: 70vh">
      <div class="column">
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
              <li>Debe tener al menos 8 carácteres</li>
              <li>No debe ser solo númerica</li>
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
              :disable="disableRestore"
            />
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useUserStore } from '@/stores/user.js'

export default defineComponent({
  name: 'SignInIndex',
  setup() {
    const key = ref('')
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
    const regexPassword = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/g

    const checkPass = (value) => {
      if (regexPassword.test(value)) {
        return true // La validación es exitosa
      } else {
        return 'La contraseña no cumple con los requisitos'
      }
    }
    const disableRestore = computed(() => {
      return password.value !== password2.value || password.value == ''
    })
   
    const resetPassword = async () => {      
      let response = null
      if (password.value !== password2.value) {
        return
      } else {
        if (regexPassword.test(password.value) || regexPassword.test(password2.value)) {
          loading.value = true
          response = await userStore.RESET_PASSWORD(key.value, password.value)
          if (response?.status !== 200) {
            $q.notify({
              color: 'red-5',
              textColor: 'white',
              icon: 'report_problem',
              message: response.errors[0].message
            })
          } else {
            router.push({ name: 'home' })
          }
          clearForm()
          loading.value = false
        } else {
          clearForm()
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'report_problem',
            message: response?.errors[0].message || 'Ocurrio un error. Vuelve a intentarlo'
          })
        }
      }
    }
    onMounted(() => {
      key.value = router.currentRoute.value.params.key
    })

    const goHome = () => {
      router.push({ path: '/' })
    }

    return {
      password,
      password2,
      resetPassword,
      loading,
      checkPass,
      regexPassword,
      goHome,
      disableRestore
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
