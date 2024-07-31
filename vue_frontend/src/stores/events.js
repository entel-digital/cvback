import { defineStore } from 'pinia'
import {
  getAllEvents,
  getAllEventsByDate,
  getAllEventsByDateAndLabel,
  getAllEventsById,
  getAllEventsByLabel,
  getSummary
} from '@/services/cv-api/modules/events/index.js'

const parseData = (data) => {
  const replaces = data.replace(/\\\"/g, '"').slice(1, -1).replace('no cumple', 'no_cumple')
  return JSON.parse(replaces)
}

export const useEventsStore = defineStore('events', {
  state: () => ({
    allEvents: [],
    dateSelected: null,
    timeSelected: null,
    labelsTypeSelected: null,
    summaryEvents: null,
    pagination: {
      sortBy: 'desc',
      descending: false,
      page: 1,
      offset: 0,
      rowsPerPage: 50
    },
    funtionToUse: 'allevents',
    labelTypes: null
  }),
  actions: {
    async FETCH_SUMMARY() {
      try {
        const data = await getSummary()
        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }
        return data
      } catch (error) {
        console.log('HERE IN ERROR FETCH_SUMMARY', error)
        this.allEvents = []
      }
    },
    async FETCH_EVENTS() {
      try {
        let data = []
        console.log("this.functionToUse stire", this.funtionToUse);
        if (this.funtionToUse === 'bydateandlabel') {
          console.log('entro al bydateandlabel')
          data = await getAllEventsByDateAndLabel(
            this.dateSelected.from,
            this.dateSelected.to,
            this.labelsTypeSelected
          )
        }
        if (this.funtionToUse === 'bydate') {
          console.log('entro al bydate')

          data = await getAllEventsByDate(this.dateSelected.from, this.dateSelected.to)
        }
        if (this.funtionToUse === 'bylabel') {
          console.log('entro al bylabel')

          data = await getAllEventsByLabel(this.labelsTypeSelected)
        }
        if (this.funtionToUse === 'allevents') {
          console.log('entro al allevents')

          data = await getAllEvents(this.pagination.offset, this.pagination.rowsPerPage)
        }

        if (data.filteredAndPaginatedEvents) {
          data.filteredAndPaginatedEvents.events.sort((a, b) => {
            return new Date(b.addedDate) - new Date(a.addedDate)
          })

        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }
        this.labelsTypes = Object.keys(parseData(data.filteredAndPaginatedEvents.labelsSummary))
      }
      this.allEvents = data.filteredAndPaginatedEvents.events
console.log("allEvents store", this.allEvents);
        return this.allEvents
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS', error)
        this.allEvents = []
      }
    }
  }
})
