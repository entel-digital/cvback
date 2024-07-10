import { defineStore } from "pinia";
import { api } from "src/boot/axios";


export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
  }),
  actions: {
    async SIGN_IN(data) {
      try {
        this.user =  await api.post("_allauth/browser/v1/auth/login ", JSON.stringify(data))
        return this.user;
      } catch (error) {
        console.log("HERE IN ERROR SIGN_IN", error);
      }
    },
    async SIGN_OUT() {
      try {
        this.user = null
        await api.delete("_allauth/browser/v1/auth/session ")
      } catch (error) {
        console.log("HERE IN ERROR SIGN_IN", error);
      }
    },
  },
});
