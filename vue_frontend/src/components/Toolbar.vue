<script setup>
import { useUserStore } from '@/stores/user.js'
import { useRouter } from 'vue-router'
import { baseStorageUrl } from '@/services/utils/globals.js'

const logoVision = `${baseStorageUrl}/images/logo_vision_azul.png`
const userStore = useUserStore()
const router = useRouter()

const signOut = async () => {
  await userStore.SIGN_OUT()
  router.push({ name: 'login' })
}
</script>

<template>
  <q-toolbar class="bg-info text-primary toolbar-height justify-between items-center q-px-md">
    <q-toolbar-title style="max-width: 750px">
      <div class="fit q-px-md">
        <img :src="logoVision" alt="logo vision" class="logo-vision" />
      </div>

    </q-toolbar-title>
    <q-btn-dropdown
      flat
      width="auto"
      class="text-grey-6 text-bold"
      push
      icon="person_outline"
      :label="userStore.user?.data.user.display"
      dropdown-icon="expand_more"
      style="width: 100px;"
    >
      <q-list>
        <q-item class="fit" clickable v-close-popup @click="signOut">
          <q-item-section>
            <q-item-label>Cerrar sesión</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-icon name="logout" color="grey-6" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </q-toolbar>
</template>

<style lang="scss" scoped>
.logo-vision {
  width: 100px;
  height: auto;
}
.toolbar-height {
  height: 60px;
}
</style>
