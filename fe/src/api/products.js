import axios from 'axios';
import Cookies from 'js-cookie';

const base = import.meta.env.VITE_BE_BASE_URI;


export async function getProducts() {
  const token = Cookies.get("token")

  const res = await axios.get(`${base}/api/products`, {
    headers: {
      Authorization: "Bearer "+token,
    },
  });

  return res?.data;
}


export async function getProductOffers(){
  const token = Cookies.get("token")

  const res = await axios.get(`${base}/api/product-offers`, {
    headers: {
      Authorization: "Bearer "+token,
    },
  });

  return res?.data;
}
