import { defineStore } from 'pinia'
import { getAllEvents } from "@/services/cv-api/modules/events/index.js";


export const useEventsStore = defineStore('events', {
  state: () => ({
    allEvents: [],
    dateSelected: null,
    timeSelected: null,
    labelsTypeSelected: null,
  }),
  actions: {
    async FETCH_EVENTS() {
      try {
        const data = await getAllEvents(25, 0, this.dateSelected);
        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate);
        });
        this.allEvents =  data.filteredAndPaginatedEvents.events;
        console.log("allEvents store", this.allEvents);
      } catch (error) {
        console.log("HERE IN ERROR FETCH_EVENTS");
        this.allEvents = [];

      }
    },
  }
})
