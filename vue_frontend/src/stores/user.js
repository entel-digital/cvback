import { defineStore } from 'pinia'
import { api } from '@/services/utils/axios'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),
  persist: {
    paths: ['user']
  },
  actions: {
    async SIGN_IN(data) {
      try {
        const user = await api.post('_allauth/browser/v1/auth/login ', JSON.stringify(data))
        this.user = user.data
        return user.data
      } catch (error) {
        console.log('HERE IN ERROR SIGN_IN')
        return error.response.data
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
        return session.data
      } catch (error) {
        console.log('HERE IN ERROR SESSION')
        // return error
      }
    },
    async REQUEST_PASSWORD(email) {
      try {
        const response = await api.post('_allauth/browser/v1/auth/password/request', {
          email: email
        })
        return response.data.status
      } catch (error) {
        console.log('HERE IN ERROR REQUEST PASSWORD')
        return error.response.data
      }
    },
    async RESET_PASSWORD(key, password) {
      try {
        const response = await api.post('_allauth/browser/v1/auth/password/reset',{
          key: key,
          password: password
      })
        return response
      } catch (error) {
        console.log('HERE IN ERROR RESET PASSWORD')
        return error.response.data
      }
    },
    async TOKEN_SESSION(token) {
      try {
   
        const response = await api.get('events/login_by_link/',{
          headers: {
            'Authorization': `Bearer ${token}`
          }
      })
        return response
      } catch (error) {
        console.log('HERE IN ERROR TOKEN SESSION', error)
        return error
      }
    }
  }
})
