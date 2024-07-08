<template>
  <div class="flex flex-center">
    <div
      class="bg-blue-5 border-radius flex flex-center column q-pa-lg"
      style="height: 50vh"
    >
      <p class="q-py-lg text-center text-white barlow-bold">Iniciar sesión</p>
      <form
        @submit.prevent="signInVision"
        class="q-gutter-md text-center q-pa-md"
        style="min-width: 300px"
      >
        <q-input
          dark
          standard
          v-model="email"
          label="Correo electrónico"
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
          :rules="ageRules"
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
import { defineComponent } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "SignInIndex",
  setup() {
    const router = useRouter();

    function signInVision() {
      console.log("Sign in");
      router.push({ name: "events" }).catch((err) => {
        console.error("Failed to navigate:", err);
      });
    }

    return {
      signInVision,
    };
  },
});
</script>

<style lang="scss" scoped>
.container-img {
  background-image: url("src/assets/vision_img_test.jpg");
}
.border-radius {
  border-radius: 10px;
}
</style>
