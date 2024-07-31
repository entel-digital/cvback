<script setup>
import { ref } from 'vue'

import SingIn from '@/components/SingIn.vue'

const logoVisionBlue = ref('/static/images/logo_vision_azul.png')
const logoEntelDigitalBlue = ref('/static/images/entel_digital_azul.png')

const logoVisionWhite = ref('/static/images/logo_vision_blanco.png')
const logoEntelDigitalWhite = ref('/static/images/entel_digital_blanco.png')

</script>

<template>
  <q-layout view="hHh Lpr lFf">
    <div class="gt-sm row">
      <div class="col-6">
        <div class="flex flex-center" style="height: 100vh">
          <img :src="logoVisionBlue" alt="vision-logo" style="width: 70%" />
        </div>
        <div class="mt-minus-15 flex justify-center">
          <img :src="logoEntelDigitalBlue" alt="entel-digital-logo" style="width: 20%" />
        </div>
      </div>
      <div class="col-6">
        <div class="container-img flex flex-center">
          <SingIn />
        </div>
      </div>
    </div>

    <div class="lt-md fit">
      <q-page-container class="container-img flex column justify-evenly" style="height: 100vh">
        <div class="q-pt-xl flex justify-center">
          <img :src="logoVisionWhite" alt="vision-logo" style="width: 70%" />
        </div>

        <SingIn />
        <div class="flex justify-center self-end">
          <img :src="logoEntelDigitalWhite" alt="vlogo" style="width: 30%" />
        </div>
      </q-page-container>
    </div>
  </q-layout>
</template>

<style scoped>
.container-img {
  background-image: url('/static/images/torreentel.png');
  background-size: cover; /* Asegura que la imagen de fondo cubra todo el espacio */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  background-position: center; /* Centra la imagen de fondo */
  height: 100vh;
  width: 100%;
}
.mt-minus-15 {
  margin-top: -15vh;
}
/* header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */
</style>
