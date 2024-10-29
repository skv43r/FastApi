'use client';
import { useEffect, useState } from 'react';

// Определяем интерфейс для структуры данных пользователя
interface User {
  id: number;
  name: string;
  email: string;
  avatar: string;
}

// Интерфейс для всего ответа
interface ApiResponse {
  users: User[];
}

export default function Home() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // Делаем запрос к вашему endpoint
        const response = await fetch('http://localhost:8000/api/return');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data: ApiResponse = await response.json();
        setUsers(data.users);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-6 text-center">Users</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {users.map((user) => (
          <div 
            key={user.id} 
            className="border rounded-lg p-4 shadow-sm"
          >
            <img
              src={`http://localhost:8000/public/user_${user.id}.jpg`}
              alt={`${user.name}'s avatar`}
              className="w-20 h-20 rounded-full mx-auto mb-4"
            />
            <h2 className="text-xl font-semibold text-center">{user.name}</h2>
            <p className="text-gray-600 text-center">{user.email}</p>
          </div>
        ))}
      </div>
    </main>
  );
}