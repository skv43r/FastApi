'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle } from 'lucide-react'

export default function Success() {
  const router = useRouter()
  const [bookingDetails, setBookingDetails] = useState<any>(null)

  useEffect(() => {
    // In a real application, you would fetch the booking details from an API
    // or get them from a state management solution like Redux
    // For this example, we'll use mock data
    const mockBookingDetails = {
      serviceName: "Персональная тренировка",
      trainerName: "Иван Петров",
      date: "2023-06-15",
      time: "14:00"
    }
    setBookingDetails(mockBookingDetails)
  }, [])

  const handleReturnHome = () => {
    router.push('/')
  }

  if (!bookingDetails) {
    return <div className="flex justify-center items-center min-h-screen">Загрузка...</div>
  }

  return (
    <main className="container mx-auto p-8">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-center mb-4">
              <CheckCircle className="w-16 h-16 text-green-500" />
            </div>
            <CardTitle className="text-3xl font-bold text-center">Бронирование успешно!</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <p className="text-center text-muted-foreground">
              Ваша запись успешно подтверждена. Вот детали вашего бронирования:
            </p>
            <div className="space-y-2">
              <p><strong>Услуга:</strong> {bookingDetails.serviceName}</p>
              <p><strong>Тренер:</strong> {bookingDetails.trainerName}</p>
              <p><strong>Дата:</strong> {new Date(bookingDetails.date).toLocaleDateString('ru-RU')}</p>
              <p><strong>Время:</strong> {bookingDetails.time}</p>
            </div>
            <p className="text-center text-sm text-muted-foreground">
              Мы отправили подтверждение на вашу электронную почту. Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.
            </p>
            <div className="flex justify-center">
              <Button onClick={handleReturnHome}>
                Вернуться на главную
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}