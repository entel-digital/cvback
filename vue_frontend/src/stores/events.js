import { defineStore } from 'pinia'
import {
  getAllEvents,
  getAllEventsByDate,
  getAllEventsByDateAndLabel,
  getAllEventsById,
  getAllEventsByLabel
} from '@/services/cv-api/modules/events/index.js'
import { api } from '@/services/utils/axios'

const parseData = (data) => {
  const replaces = data.replace(/\\\"/g, '"').slice(1, -1)
  const parsedData = JSON.parse(replaces)

  return Object.entries(parsedData)
    .filter(([key, value]) => key !== 'total')
    .map(([key, value]) => ({
      key,
      value: value.total,
      id: value.id
    }))
}

export const useEventsStore = defineStore('events', {
  state: () => ({
    allEvents: [],
    eventById: [],
    dateSelected: null,
    timeSelected: null,
    labelsSelected: null,
    typesSelected: null,
    summaryEvents: null,
    pagination: {
      sortBy: 'desc',
      descending: false,
      page: 1,
      offset: 0,
      rowsPerPage: 50
    },
    funtionToUse: 'allevents',
    labelTypesList: null,
    loadingEvents: false,
    loadingExport: false,
    sortAsc: false, 
  }),
  actions: {
    async FETCH_EVENTS() {
      
      this.loadingEvents = true
      this.allEvents = []

      try {
        const data = await getAllEvents(this.pagination.offset, this.pagination.rowsPerPage, "added_date", this.sortAsc)

        this.summaryEvents = {
          filtered: data.filteredAndPaginatedEvents.filtered,
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary),
          globalTotalNumber: data.filteredAndPaginatedEvents.globalTotalNumber,
          labelTextFilter: data.filteredAndPaginatedEvents.labelTextFilter,
          queryTotalNumber: data.filteredAndPaginatedEvents.queryTotalNumber,
          uniqueLabelsCount: data.filteredAndPaginatedEvents.uniqueLabelsCount,
          queryTotalEventsYear: data.filteredAndPaginatedEvents.queryTotalEventsYear,
          queryTotalEventsWeek: data.filteredAndPaginatedEvents.queryTotalEventsWeek,
          queryTotalEventsMonth: data.filteredAndPaginatedEvents.queryTotalEventsMonth,
          queryTotalEventsDay: data.filteredAndPaginatedEvents.queryTotalEventsDay
        }
        this.labelsTypes = parseData(data.filteredAndPaginatedEvents.labelsSummary).map(
          (itm) => itm.key
        )

        this.allEvents = data.filteredAndPaginatedEvents.events

        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH EVENTS')
        this.allEvents = []
        this.summaryEvents = { error: 'error'}
        this.loadingEvents = false
        return
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
          this.dateSelected.to,
          "added_date",
          this.sortAsc
        )

        // data.filteredAndPaginatedEvents.events.sort((a, b) => {
        //   return new Date(b.addedDate) - new Date(a.addedDate)
        // })
        this.summaryEvents = {
          filtered: data.filteredAndPaginatedEvents.filtered,
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary),
          globalTotalNumber: data.filteredAndPaginatedEvents.globalTotalNumber,
          labelTextFilter: data.filteredAndPaginatedEvents.labelTextFilter,
          queryTotalNumber: data.filteredAndPaginatedEvents.queryTotalNumber,
          uniqueLabelsCount: data.filteredAndPaginatedEvents.uniqueLabelsCount,
          queryTotalEventsYear: data.filteredAndPaginatedEvents.queryTotalEventsYear,
          queryTotalEventsWeek: data.filteredAndPaginatedEvents.queryTotalEventsWeek,
          queryTotalEventsMonth: data.filteredAndPaginatedEvents.queryTotalEventsMonth,
          queryTotalEventsDay: data.filteredAndPaginatedEvents.queryTotalEventsDay
        }

        this.labelsTypes = parseData(data.filteredAndPaginatedEvents.labelsSummary).map(
          (itm) => itm.key
        )

        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_DATE')
        this.allEvents = []
        this.loadingEvents = false
        return
      }
    },
    async FETCH_EVENTS_BY_LABEL() {
      this.allEvents = []
      this.loadingEvents = true
      try {
        const data = await getAllEventsByLabel(
          this.pagination.offset,
          this.pagination.rowsPerPage,
          this.labelsSelected,
          "added_date",
          this.sortAsc
        )

        // data.filteredAndPaginatedEvents.events.sort((a, b) => {
        //   return new Date(b.addedDate) - new Date(a.addedDate)
        // })
        this.summaryEvents = {
          filtered: data.filteredAndPaginatedEvents.filtered,
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary),
          globalTotalNumber: data.filteredAndPaginatedEvents.globalTotalNumber,
          labelTextFilter: data.filteredAndPaginatedEvents.labelTextFilter,
          queryTotalNumber: data.filteredAndPaginatedEvents.queryTotalNumber,
          uniqueLabelsCount: data.filteredAndPaginatedEvents.uniqueLabelsCount,
          queryTotalEventsYear: data.filteredAndPaginatedEvents.queryTotalEventsYear,
          queryTotalEventsWeek: data.filteredAndPaginatedEvents.queryTotalEventsWeek,
          queryTotalEventsMonth: data.filteredAndPaginatedEvents.queryTotalEventsMonth,
          queryTotalEventsDay: data.filteredAndPaginatedEvents.queryTotalEventsDay
        }

        this.labelsTypes = parseData(data.filteredAndPaginatedEvents.labelsSummary).map(
          (itm) => itm.key
        )
        this.allEvents = data.filteredAndPaginatedEvents.events

        this.loadingEvents = false
        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_LABEL')
        this.allEvents = []
        this.loadingEvents = false
        return
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
          this.labelsSelected,
          "added_date",
          this.sortAsc
        )

        // data.filteredAndPaginatedEvents.events.sort((a, b) => {
        //   return new Date(b.addedDate) - new Date(a.addedDate)
        // })
        this.summaryEvents = {
          filtered: data.filteredAndPaginatedEvents.filtered,
          totalEvents: data.filteredAndPaginatedEvents.globalTotalNumber,
          totalQueryEvents: data.filteredAndPaginatedEvents.queryTotalNumber,
          labelsSummary: parseData(data.filteredAndPaginatedEvents.labelsSummary),
          typesSummary: parseData(data.filteredAndPaginatedEvents.typesSummary),
          globalTotalNumber: data.filteredAndPaginatedEvents.globalTotalNumber,
          labelTextFilter: data.filteredAndPaginatedEvents.labelTextFilter,
          queryTotalNumber: data.filteredAndPaginatedEvents.queryTotalNumber,
          uniqueLabelsCount: data.filteredAndPaginatedEvents.uniqueLabelsCount,
          queryTotalEventsYear: data.filteredAndPaginatedEvents.queryTotalEventsYear,
          queryTotalEventsWeek: data.filteredAndPaginatedEvents.queryTotalEventsWeek,
          queryTotalEventsMonth: data.filteredAndPaginatedEvents.queryTotalEventsMonth,
          queryTotalEventsDay: data.filteredAndPaginatedEvents.queryTotalEventsDay
        }

        this.labelsTypes = parseData(data.filteredAndPaginatedEvents.labelsSummary).map(
          (itm) => itm.key
        )

        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false

        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_DATE_BY_LABEL')
        this.allEvents = []
        this.loadingEvents = false
        return
      }
    },
    async FETCH_EVENTS_BY_ID(token, eventId) {
      this.eventById = []
      this.loadingEvents = true
      try {
        const data = await getAllEventsById(token, eventId)

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })
  
        this.eventById = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false

        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_ID')
        this.eventById = []
        this.loadingEvents = false
        return
      }
    },

    async EXPORT_DATA(format) {
      this.loadingExport = true
      try{
        let url = `${api.defaults.baseURL}events/csv_events/?format=${format.toUpperCase()}`

        if (this.labelsSelected) {
          url = `${url}&label_id_filter=${this.labelsSelected}`
        }
        if(this.dateSelected){
          url = `${url}&date_greater_than_equal=${this.dateSelected.from}&date_lower_than=${this.dateSelected.to}`
        }
  
        const response = await api.get(url)
          this.loadingExport = false
        return response 
      }catch(error){
        return error
        this.loadingExport = false

      }
    }
  }
})
