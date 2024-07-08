import axios from "axios";

export const getToken = async(url) => {
  try {
    const response = await axios.get(url);
    const token = extractTokenFromHTML(response.data);
    console.log('Token:', token);
  } catch (error) {
    console.error('Error obteniendo el token:', error);
  }
};

const extractTokenFromHTML = (html) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  // Supongamos que el token está dentro de una etiqueta <meta name="token" content="EL_TOKEN">
  const tokenMeta = doc.querySelector('input[name="csrfmiddlewaretoken"]');
  console.log("tokenMeta", tokenMeta);
  return tokenMeta ? tokenMeta.getAttribute('content') : null;
}
