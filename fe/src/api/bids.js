import axios from 'axios';
import Cookies from 'js-cookie';

const base = import.meta.env.VITE_BE_BASE_URI;

export async function getBids() {
  const token = Cookies.get("token")

  const res = await axios.get(`${base}/api/bids`, {
    headers: {
      Authorization: "Bearer "+token,
    },
  });

  return res?.data;
}


export async function postBid({product_id, quantity, offer_price}) {
  const token = Cookies.get("token")

  const res = await axios.post(
    `${base}/api/bids`, 
    {
      product_id,
      quantity,
      offer_price,
    },
    {
      headers: {
        Authorization: "Bearer "+token,
      },
    }
  );
}

export async function acceptBid(bidId) {
  const token = Cookies.get("token")

  const res = await axios.post(`${base}/api/bids/${bidId}/accept`, 
    {},
    {
      headers: {
        Authorization: "Bearer "+token,
      },
    }
  );
}

export async function rejectBid(bidId) {
  const token = Cookies.get("token")

  const res = await axios.post(`${base}/api/bids/${bidId}/reject`, 
    {},
    {
      headers: {
        Authorization: "Bearer "+token,
      },
    }
  );
}
