import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getEvent, mintTicket } from '@/lib/api';

export default function EventDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [event, setEvent] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [minting, setMinting] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  useEffect(() => {
    if (id) {
      loadEvent();
    }
  }, [id]);

  const loadEvent = async () => {
    try {
      const data = await getEvent(id as string);
      setEvent(data);
    } catch (error) {
      console.error('Error loading event:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedImage(e.target.files[0]);
    }
  };

  const handleBuyTicket = async () => {
    const walletAddress = localStorage.getItem('walletAddress');
    if (!walletAddress) {
      alert('Please connect your wallet first');
      return;
    }

    if (!selectedImage) {
      alert('Please upload your photo for the ticket');
      return;
    }

    setMinting(true);
    try {
      const formData = new FormData();
      formData.append('event_id', id as string);
      formData.append('wallet_address', walletAddress);
      formData.append('buyer_image', selectedImage);

      const result = await mintTicket(formData);
      alert(`Ticket minted successfully! Token ID: ${result.token_id}`);
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Error minting ticket:', error);
      alert(`Failed to mint ticket: ${error.response?.data?.detail || error.message}`);
    } finally {
      setMinting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-qie-primary"></div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Event not found</p>
      </div>
    );
  }

  const availability = event.total_supply - event.sold_count;

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="h-64 bg-gradient-to-br from-qie-primary to-qie-secondary flex items-center justify-center text-white text-9xl">
            🎭
          </div>

          <div className="p-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">{event.title}</h1>
            <p className="text-gray-600 mb-6">{event.description}</p>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div className="space-y-3">
                <div className="flex items-center text-gray-700">
                  <span className="mr-3 text-2xl">📍</span>
                  <div>
                    <p className="text-sm text-gray-500">Venue</p>
                    <p className="font-semibold">{event.venue}</p>
                  </div>
                </div>
                <div className="flex items-center text-gray-700">
                  <span className="mr-3 text-2xl">📅</span>
                  <div>
                    <p className="text-sm text-gray-500">Date</p>
                    <p className="font-semibold">{new Date(event.date).toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center text-gray-700">
                  <span className="mr-3 text-2xl">💰</span>
                  <div>
                    <p className="text-sm text-gray-500">Price</p>
                    <p className="font-semibold text-2xl">{event.ticket_price} QIE</p>
                  </div>
                </div>
                <div className="flex items-center text-gray-700">
                  <span className="mr-3 text-2xl">🎫</span>
                  <div>
                    <p className="text-sm text-gray-500">Available Tickets</p>
                    <p className="font-semibold">{availability} / {event.total_supply}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="border-t pt-8">
              <h2 className="text-2xl font-bold mb-4">Buy Ticket</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Your Photo (for AI verification)
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-qie-primary file:text-white hover:file:bg-qie-secondary"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    This photo will be used for AI verification at the event entrance
                  </p>
                </div>

                {selectedImage && (
                  <div className="mt-4">
                    <img
                      src={URL.createObjectURL(selectedImage)}
                      alt="Preview"
                      className="w-32 h-32 object-cover rounded-lg border-2 border-gray-300"
                    />
                  </div>
                )}

                <button
                  onClick={handleBuyTicket}
                  disabled={minting || availability === 0 || !selectedImage}
                  className="w-full bg-qie-primary hover:bg-qie-secondary disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold transition-colors"
                >
                  {minting ? 'Minting Ticket...' : availability === 0 ? 'Sold Out' : 'Buy Ticket'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
