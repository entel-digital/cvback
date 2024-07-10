<template>
  <div class="flex flex-center">
    <div
      class="bg-blue-5 border-radius flex flex-center column q-pa-lg"
      style="height: 50vh"
    >
      <p class="q-py-lg text-center text-white barlow-bold">Iniciar sesión</p>
      <form
        @submit.prevent="signInVision()"
        class="q-gutter-md text-center q-pa-md"
        style="min-width: 300px"
      >
        <q-input
          dark
          standard
          v-model="username"
          label="Usuario"
          lazy-rules
          color="white"
          :rules="nameRules"
        />

        <q-input
          dark
          standard
          type="password"
          v-model="password"
          label="Contraseña"
          lazy-rules
          :rules="passwordRules"
        />

        <div class="q-py-lg">
          <q-btn
            label="Ingresar"
            no-caps
            type="submit"
            color="accent"
            class="full-width"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "stores/user-store";


export default defineComponent({
  name: "SignInIndex",
  setup() {
    const username = ref("");
    const password = ref("");
    const router = useRouter();
    const userStore = useUserStore();

    const signInVision = async () =>  {
          console.log("Sign in");
          await userStore.SIGN_IN({username: username.value, password: password.value});
          console.log("userstore user", userStore.user);
          if(userStore.user?.status === 200){
            router.push({ name: "events" })
          } else {
            $q.notify({
              color: "red-5",
              textColor: "white",
              icon: "report_problem",
              message: "Usuario o contraseña incorrectos",
            });
          }
          // router.push({ name: "events" }).catch((err) => {
          //   console.error("Failed to navigate:", err);
          // });
        }

    return {
      username,
      password,
      signInVision,
    };
  },
});
</script>

<style lang="scss" scoped>
.container-img {
  background-image: url("src/assets/bg_vision.png");
}
.border-radius {
  border-radius: 10px;
}
</style>
