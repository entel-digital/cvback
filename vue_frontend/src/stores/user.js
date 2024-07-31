import { defineStore } from 'pinia'
import { api } from "@/services/utils/axios";


export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),
  persist:{
    paths: ['user']
  },
  actions: {
    async SIGN_IN(data) {
      try {
        const user = await api.post('_allauth/browser/v1/auth/login ', JSON.stringify(data))
        this.user = user.data
        return user
      } catch (error) {
        console.log('HERE IN ERROR SIGN_IN', error)
      }
    },
    async SIGN_OUT() {
      try {
        this.user = null
        await api.delete('_allauth/browser/v1/auth/session')
      } catch (error) {
        console.log('HERE IN ERROR SIGN_OUT')
      }
    },
    async GET_SESSION() {
      try {
        const session = await api.get('_allauth/browser/v1/auth/session')
        return session.data.meta
      } catch (error) {
        console.log('HERE IN ERROR SESSION')
        // return error
      }
    }
  }
})
