import { defineStore } from 'pinia'
import {
  getAllEvents,
  getAllEventsByDate,
  getAllEventsByDateAndLabel,
  getAllEventsById,
  getAllEventsByLabel
} from '@/services/cv-api/modules/events/index.js'

const parseData = (data) => {
  const replaces = data.replace(/\\\"/g, '"').slice(1, -1).replace('no cumple', 'no_cumple')
  return Object.entries(JSON.parse(replaces)).map(([key, value]) => ({ key, value })).filter(itm => itm.key !== 'total');
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
    labelsTypes: null,
    loadingEvents: false
  }),
  actions: {
    async FETCH_EVENTS() {
      this.loadingEvents = true
      this.allEvents = []

      try {
        const data = await getAllEvents(this.pagination.offset, this.pagination.rowsPerPage)

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })

        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }

        this.labelsTypes = Object.keys(parseData(data.filteredAndPaginatedEvents.labelsSummary)).filter(itm => itm !== 'total')
        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_DATE', error)
        this.allEvents = []
        this.loadingEvents = false
      }
    },
    async FETCH_EVENTS_BY_DATE() {
      this.loadingEvents = true
      this.allEvents = []

      try {
        const data = await getAllEventsByDate(
          this.pagination.offset,
          this.pagination.rowsPerPage,
          this.dateSelected.from,
          this.dateSelected.to
        )

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })

        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }
        this.labelsTypes = Object.keys(parseData(data.filteredAndPaginatedEvents.labelsSummary)).filter(itm => itm !== 'total')


        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_DATE', error)
        this.allEvents = []
        this.loadingEvents = false
      }
    },
    async FETCH_EVENTS_BY_LABEL() {
      this.allEvents = []
      this.loadingEvents = true
      try {
        const data = await getAllEventsByLabel(
          this.pagination.offset,
          this.pagination.rowsPerPage,
          this.labelsTypeSelected
        )

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })

        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }

        this.labelsTypes = Object.keys(parseData(data.filteredAndPaginatedEvents.labelsSummary)).filter(itm => itm !== 'total')

        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_LABEL', error)
        this.allEvents = []
      }
    },
    async FETCH_EVENTS_BY_DATE_BY_LABEL() {
      this.allEvents = []
      this.loadingEvents = true
      try {
        const data = await getAllEventsByDateAndLabel(
          this.pagination.offset,
          this.pagination.rowsPerPage,
          this.dateSelected.from,
          this.dateSelected.to,
          this.labelsTypeSelected
        )

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })

        this.summaryEvents = {
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary)
        }
        this.labelsTypes = Object.keys(parseData(data.filteredAndPaginatedEvents.labelsSummary)).filter(itm => itm !== 'total')

        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false

        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_DATE_BY_LABEL', error)
        this.allEvents = []
      }
    }
  }
})
