import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import TicketCard from '@/components/TicketCard';
import { getUserTickets } from '@/lib/api';

export default function Dashboard() {
  const router = useRouter();
  const [tickets, setTickets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const walletAddress = localStorage.getItem('walletAddress');
    if (!walletAddress) {
      router.push('/');
      return;
    }
    loadTickets(walletAddress);
  }, []);

  const loadTickets = async (walletAddress: string) => {
    try {
      const data = await getUserTickets(walletAddress);
      setTickets(data.tickets || []);
    } catch (error) {
      console.error('Error loading tickets:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">My Tickets</h1>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-qie-primary"></div>
            <p className="mt-4 text-gray-600">Loading tickets...</p>
          </div>
        ) : tickets.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-600 text-lg">No tickets found.</p>
            <p className="text-gray-500 mt-2">Purchase tickets to see them here!</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tickets.map((ticket) => (
              <TicketCard key={ticket.token_id} ticket={ticket} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
