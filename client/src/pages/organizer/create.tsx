import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { createEvent } from '@/lib/api';

export default function CreateEvent() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: '',
    venue: '',
    ticket_price: '',
    total_supply: '',
  });
  const [image, setImage] = useState<File | null>(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const isOrganizer = localStorage.getItem('isOrganizer') === 'true';
    if (!isOrganizer) {
      alert('Only organizers can create events');
      router.push('/');
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const walletAddress = localStorage.getItem('walletAddress');
    if (!walletAddress) {
      alert('Please connect your wallet');
      return;
    }

    if (!image) {
      alert('Please select an event image');
      return;
    }

    setCreating(true);
    try {
      const data = new FormData();
      data.append('title', formData.title);
      data.append('description', formData.description);
      data.append('date', new Date(formData.date).toISOString());
      data.append('venue', formData.venue);
      data.append('ticket_price', formData.ticket_price);
      data.append('total_supply', formData.total_supply);
      data.append('organizer_address', walletAddress);
      data.append('image', image);

      await createEvent(data);
      alert('Event created successfully!');
      router.push('/events');
    } catch (error: any) {
      console.error('Error creating event:', error);
      alert(`Failed to create event: ${error.response?.data?.detail || error.message}`);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Create Event</h1>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Event Title
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows={4}
              className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date & Time
              </label>
              <input
                type="datetime-local"
                name="date"
                value={formData.date}
                onChange={handleChange}
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Venue
              </label>
              <input
                type="text"
                name="venue"
                value={formData.venue}
                onChange={handleChange}
                required
                className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ticket Price (QIE)
              </label>
              <input
                type="number"
                name="ticket_price"
                value={formData.ticket_price}
                onChange={handleChange}
                required
                step="0.01"
                min="0"
                className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Total Supply
              </label>
              <input
                type="number"
                name="total_supply"
                value={formData.total_supply}
                onChange={handleChange}
                required
                min="1"
                className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-900 bg-white focus:ring-2 focus:ring-qie-primary focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Event Image
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              required
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-qie-primary file:text-white hover:file:bg-qie-secondary"
            />
            {image && (
              <div className="mt-4">
                <img
                  src={URL.createObjectURL(image)}
                  alt="Event preview"
                  className="w-full h-48 object-cover rounded-lg"
                />
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={creating}
            className="w-full bg-qie-primary hover:bg-qie-secondary disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold text-lg transition-colors"
          >
            {creating ? 'Creating Event...' : 'Create Event'}
          </button>
        </form>
      </div>
    </div>
  );
}
