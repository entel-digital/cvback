import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
// Crear una instancia de Axios con la configuración deseada
const api = axios.create({
  baseURL: '/',
  withCredentials: true,
  withXSRFToken: true
});

// Función para obtener una cookie
function getCookie(name) {
  const value = '; ' + document.cookie;
  const parts = value.split('; ' + name + '=');
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}
// Interceptor para agregar el CSRF token a las solicitudes POST y PUT
api.interceptors.request.use((config) => {
  if (
      config.method?.toLowerCase() === 'post' ||
      config.method?.toLowerCase() === 'put' ||
        config.method?.toLowerCase() === 'delete'

  ) {
      const csrfToken = getCookie('csrftoken');
      if (csrfToken) {
          config.headers['X-CSRFToken'] = csrfToken;
      }
  }
  return config;
});

export { api };
