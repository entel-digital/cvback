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
    sortAsc: true, 
  }),
  actions: {
    async FETCH_EVENTS() {
      
      this.loadingEvents = true
      this.allEvents = []

      try {
        const data = await getAllEvents(this.pagination.offset, this.pagination.rowsPerPage, "addedDate", this.sortAsc)

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
          "addedDate",
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
          "addedDate",
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
          "addedDate",
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
    async FETCH_EVENTS_BY_ID(eventId) {
      this.allEvents = []
      this.loadingEvents = true
      try {
        const data = await getAllEventsById(eventId)

        data.filteredAndPaginatedEvents.events.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate)
        })
        console.log(
          'data.filteredAndPaginatedEvents by date y label',
          data.filteredAndPaginatedEvents.filtered
        )
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

        this.labelTypesList = parseData(data.filteredAndPaginatedEvents.labelsSummary).map(
          (itm) => itm.key
        )

        this.allEvents = data.filteredAndPaginatedEvents.events
        this.loadingEvents = false

        return
      } catch (error) {
        console.log('HERE IN ERROR FETCH_EVENTS_BY_ID')
        this.allEvents = []
        this.loadingEvents = false
        return
      }
    },

    async EXPORT_DATA(format) {
      this.loadingExport = true
      // let url = `${api.defaults.baseURL}events/csv_events/?format=${format.toUpperCase()}`
      // console.log("api.default base", api.defaults.baseURL);
      // // let url = `localhost:8000/events/csv_events/`


      // if (this.labelsSelected) {
      //   url = `${url}&label_id_filter=${this.labelsSelected}`
      // }
      // if(this.dateSelected){
      //   url = `${url}&date_greater_than_equal=${this.dateSelected.from}&date_lower_than=${this.dateSelected.to}`
      // }

      // console.log('url export' ,url)
      // const response = 
      // setTimeout(() => {
      //   // const enlace = document.createElement('a')

      //   // enlace.href = url

      //   // enlace.download = `data_export_${new Date().toISOString()}.csv`

      //   // enlace.style.display = 'none'

      //   // document.body.appendChild(enlace)

      //   // enlace.click()

      //   // document.body.removeChild(enlace)
      //   this.loadingExport = false
      // }, 2000)
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
