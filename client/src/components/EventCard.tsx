import React, { useState } from 'react';
import Link from 'next/link';
import { getIPFSGatewayURL } from '@/lib/ipfs';

interface EventCardProps {
  event: {
    _id: string;
    title: string;
    description: string;
    date: string;
    venue: string;
    image_url: string;
    ticket_price: number;
    total_supply: number;
    sold_count: number;
  };
}

export default function EventCard({ event }: EventCardProps) {
  const availability = event.total_supply - event.sold_count;
  const percentageSold = (event.sold_count / event.total_supply) * 100;
  const imageUrl = getIPFSGatewayURL(event.image_url);
  const [imageError, setImageError] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
      <div className="h-48 bg-gradient-to-br from-qie-primary to-qie-secondary flex items-center justify-center text-white text-6xl overflow-hidden">
        {imageUrl && !imageError ? (
          <img
            src={imageUrl}
            alt={event.title}
            className="w-full h-full object-cover"
            onError={() => setImageError(true)}
          />
        ) : (
          <span>🎭</span>
        )}
      </div>
      <div className="p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">{event.title}</h3>
        <p className="text-gray-600 mb-4 line-clamp-2">{event.description}</p>
        
        <div className="space-y-2 mb-4">
          <div className="flex items-center text-sm text-gray-700">
            <span className="mr-2">📍</span>
            <span>{event.venue}</span>
          </div>
          <div className="flex items-center text-sm text-gray-700">
            <span className="mr-2">📅</span>
            <span>{new Date(event.date).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center text-sm text-gray-700">
            <span className="mr-2">💰</span>
            <span className="font-semibold">{event.ticket_price} QIE</span>
          </div>
        </div>

        <div className="mb-4">
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600">Availability</span>
            <span className="font-semibold text-gray-900">
              {availability} / {event.total_supply}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-qie-primary h-2 rounded-full transition-all"
              style={{ width: `${percentageSold}%` }}
            ></div>
          </div>
        </div>

        <Link
          href={`/events/${event._id}`}
          className="block w-full bg-qie-primary hover:bg-qie-secondary text-white text-center py-2 rounded-md font-semibold transition-colors"
        >
          View Details
        </Link>
      </div>
    </div>
  );
}
