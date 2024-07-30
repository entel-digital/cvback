import { defineStore } from 'pinia'
import { getAllEvents } from "@/services/cv-api/modules/events/index.js";


export const useEventsStore = defineStore('events', {
  state: () => ({
    allEvents: [],
    dateSelected: null,
    timeSelected: null,
    labelsTypeSelected: null,
    summaryEvents: null
  }),
  actions: {
    async FETCH_EVENTS() {
      try {
        const data = await getAllEvents(0, 50);
        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate);
        });
        this.allEvents =  data.filteredAndPaginatedEvents.events;
        console.log("filteredAndPaginatedEvents", data.filteredAndPaginatedEvents);
        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelSummary: data.filteredAndPaginatedEvents.labelSummary,
          typesSummary: data.filteredAndPaginatedEvents.typesSummary,

        }
        console.log("summaryEvents store", this.summaryEvents);
        console.log("allEvents store", this.allEvents);
        return data
      } catch (error) {
        console.log("HERE IN ERROR FETCH_EVENTS", error);
        this.allEvents = [];

      }
    },
  }
})
