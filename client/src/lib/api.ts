import axios from 'axios';

const API_BASE_URL = typeof window !== 'undefined' 
  ? window.location.origin + '/api'
  : 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const walletLogin = async (walletAddress: string, signature: string, message: string) => {
  const response = await api.post('/auth/wallet', {
    wallet_address: walletAddress,
    signature,
    message,
  });
  return response.data;
};

export const getEvents = async () => {
  const response = await api.get('/events');
  return response.data;
};

export const getEvent = async (eventId: string) => {
  const response = await api.get(`/events/${eventId}`);
  return response.data;
};

export const createEvent = async (formData: FormData) => {
  const response = await api.post('/events', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const mintTicket = async (formData: FormData) => {
  const response = await api.post('/tickets/mint', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getUserTickets = async (walletAddress: string) => {
  const response = await api.get(`/tickets/${walletAddress}`);
  return response.data;
};

export const verifyTicket = async (formData: FormData) => {
  const response = await api.post('/verify', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getVerificationLogs = async () => {
  const response = await api.get('/verify/logs');
  return response.data;
};
