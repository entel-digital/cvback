<script setup>
import { baseStorageUrl } from '@/services/utils/globals.js'
import ResetPass from '@/components/ResetPass.vue'

import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useRouter } from 'vue-router'

const logoVisionBlue = `${baseStorageUrl}/images/logo_vision_azul.png`
const logoEntelDigitalBlue = `${baseStorageUrl}/images/entel_digital_azul.png`

const logoVisionWhite = `${baseStorageUrl}/images/logo_vision_blanco.png`
const logoEntelDigitalWhite = `${baseStorageUrl}/images/entel_digital_blanco.png`

const pathImageBg = `${baseStorageUrl}/images/torreentel.png`
const styleBg = `background-image: url(${pathImageBg}); background-size: cover; background-repeat: no-repeat; background-position: center;  height: 100vh;
  width: 100%;`

const router = useRouter()

const goHome = () => {
  router.push({ path: '/' })
}
onMounted(() => {
  if (!router.currentRoute.value.params.key) {
    router.push({ name: 'login' })
  }
})
</script>

<template>
  <q-layout view="hHh Lpr lFf">
    <div class="gt-sm row">
      <div class="col-6">
        <div class="flex flex-center" style="height: 100vh">
          <img id="logo-vision-b" :src="logoVisionBlue" alt="vision-logo" style="width: 70%" />
        </div>
        <div class="mt-minus-15 flex justify-center">
          <img
            id="logo-edigital-b"
            :src="logoEntelDigitalBlue"
            alt="entel-digital-logo"
            style="width: 20%"
          />
        </div>
      </div>
      <div class="col-6">
        <div class="flex flex-center column" :style="styleBg">
          <ResetPass />
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
      </div>
    </div>

    <div class="lt-md fit">
      <q-page-container class="container-img flex column justify-evenly" style="height: 100vh">
        <div class="q-pt-xl flex justify-center">
          <img :src="logoVisionWhite" alt="vision-logo" style="width: 70%" />
        </div>

        <ResetPass />
        <div class="flex justify-center self-end">
          <img :src="logoEntelDigitalWhite" alt="vlogo" style="width: 30%" />
        </div>
      </q-page-container>
    </div>
  </q-layout>
</template>

<style scoped>
.mt-minus-15 {
  margin-top: -15vh;
}
</style>
