// import extras from '@quasar/extras'
import { Notify } from 'quasar'
// import iconSet from 'quasar/icon-set/material-icons' // opcional
// import lang from 'quasar/lang/es.js' // opcional
import {
  QBtn,
  QTable,
  QCard,
  QCardActions,
  QList,
  QItem,
  QItemLabel,
  QItemSection,
  QCarousel,
  QBtnDropdown,
  QInput,
  QDate,
  QSelect
} from 'quasar'

export default {
  config: {
    css: ['app.scss'],
    extras: [
      'material-icons', // optional, you are not bound to it
      'material-icons-outlined'
    ],
    framework: {
      iconSet: 'material-icons', // Quasar icon set
      lang: 'es' // Quasar language pack
    },
    components: {
      QBtn,
      QTable,
      QCard,
      QCardActions,
      QList,
      QItem,
      QItemLabel,
      QItemSection,
      QCarousel,
      QBtnDropdown,
      QInput,
      QDate,
      QSelect
    }
  },
  plugins: {
    Notify
  } // importar plugins si es necesario
  // lang: lang,
  // iconSet: iconSet
}
