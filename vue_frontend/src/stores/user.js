import { defineStore } from 'pinia'
import { api } from "@/services/utils/axios";


export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),
  actions: {
    async SIGN_IN(data) {
      try {
        this.user = await api.post('_allauth/browser/v1/auth/login ', JSON.stringify(data))
       console.log("this.user", this.user);
        return this.user
      } catch (error) {
        console.log('HERE IN ERROR SIGN_IN', error)
      }
    },
    async SIGN_OUT() {
      try {
        this.user = null
        await api.delete('_allauth/browser/v1/auth/session ')
      } catch (error) {
        console.log('HERE IN ERROR SIGN_OUT')
      }
    },
    async GET_SESSION() {
      // return await request('GET', URLs.SESSIONS)
      try {
        const session = await api.get('_allauth/browser/v1/auth/session ')
        return session.status
      } catch (error) {
        console.log('HERE IN ERROR SESSION', error)
        // return error
      }
    }
  }
})
