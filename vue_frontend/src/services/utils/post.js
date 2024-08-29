import { api } from '@/services/utils/axios'

export const Post = async (body) => {
  try {
    const url = `events/graphql/`

    const { data, status } = await api.post(url, JSON.stringify(body), {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (Array.isArray(data.errors) && data.errors.length > 0) {
      const [err] = data.errors
      const { message } = err
      throw new Error(`invalid error message=${message}`)
    }

    if (data.data == null) {
      throw new Error('invalid null data response')
    }

    if (status !== 200) {
      throw new Error(`invalid request status=${status}`)
    }

    return data
  } catch (err) {
    console.log('HERE IN ERROR POST', err)
    throw err
  }
}

