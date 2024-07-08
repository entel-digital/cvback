<template>
  <q-layout view="hHh Lpr lFf" class="shadow-2">
    <div class="gt-md fit row">
      <div class="col-6">
        <div class="flex flex-center" style="height: 100vh">
          <img
            src="~assets/logo_vision_azul.png"
            alt="vision-logo"
            style="width: 50%"
          />
        </div>
        <div class="mt-minus-15 flex justify-center">
          <img
            src="~assets/entel_digital_azul.png"
            alt="entel-digital-logo"
            style="width: 20%"
          />
        </div>
      </div>
      <div class="col-6">
        <q-page-container class="container-img flex flex-center">
          <router-view />
        </q-page-container>
      </div>
    </div>

    <div class="lt-sm fit">
      <q-page-container
        class="container-img flex column justify-evenly"
        style="height: 100vh"
      >
        <div class="q-pt-xl flex justify-center">
          <img
            src="~assets/logo_vision.png"
            alt="vision-logo"
            style="width: 50%"
          />
        </div>

        <router-view />
        <div class="flex justify-center self-end">
          <img
            src="~assets/entel_digital_blanco.png"
            alt="vlogo"
            style="width: 30%"
          />
        </div>
      </q-page-container>
    </div>
  </q-layout>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "SingIn",
  components: {},

  setup() {
    return {};
  },
});
</script>

<style lang="scss" scoped>
.container-img {
  background-image: url("src/assets/vision_img_test.png");
  background-size: cover; /* Asegura que la imagen de fondo cubra todo el espacio */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  background-position: center; /* Centra la imagen de fondo */
  height: 100vh; /* Asegura que el contenedor ocupe toda la altura de la pantalla */
  width: 100%;
}
.mt-minus-15 {
  margin-top: -15vh;
}
</style>
