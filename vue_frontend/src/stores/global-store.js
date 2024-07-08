import { defineStore } from "pinia";
import { getAllEvents } from "src/services/cv-api/modules/events/index.js";

export const useGlobalStore = defineStore("global", {
  state: () => ({
    allEvents: [],
  }),
  actions: {
    async FETCH_EVENTS() {
      try {
        const data = await getAllEvents();
        console.log("data", data);
        // this.allEvents = data;
        return data.allEvents;
      } catch (error) {
        console.log("HERE IN ERROR FETCH_EVENTS", error);
      }
    },
  },
});
