createWebHashHistory<template>
  <div class="flex flex-center">
    <div class="bg-blue-5 border-radius flex flex-center column q-pa-lg" style="height: 50vh">
      <div class="column">
        <p class="q-py-lg text-center text-white barlow-bold">Iniciar sesión</p>
        <form
          @submit.prevent="signInVision()"
          class="q-gutter-md text-center q-pa-md"
          style="min-width: 300px"
        >
          <q-input dark standard v-model="username" label="Usuario" lazy-rules color="white" />

          <q-input dark standard type="password" v-model="password" label="Contraseña" lazy-rules />

          <div class="q-py-lg">
            <q-btn
              label="Ingresar"
              no-caps
              type="submit"
              color="accent"
              class="full-width"
              :loading="loading"
            />
          </div>
        </form>
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
  name: 'SignInIndex',
  setup() {
    const username = ref('')
    const password = ref('')
    const router = useRouter()
    const userStore = useUserStore()

    const $q = useQuasar()
    const loading = ref(false)

    const clearForm = () => {
      username.value = ''
      password.value = ''
    }

    const signInVision = async () => {
      loading.value = true
      await userStore.SIGN_IN({
        username: username.value,
        password: password.value
      })
      if (userStore.user?.meta.is_authenticated) {
        router.push({ name: 'home' })
        loading.value = false
        clearForm()
      } else {
        loading.value = false
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'report_problem',
          message: 'Usuario o contraseña incorrectos'
        })
        clearForm()
      }
    }

    return {
      username,
      password,
      signInVision,
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
