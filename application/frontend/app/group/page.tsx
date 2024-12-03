'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import { ChevronLeft, ChevronRight, Clock, User } from 'lucide-react'

interface GroupClass {
  id: number
  name: string
  duration: number | null
  time: string
  description: string
  price: number
  availableSpots: number
  trainerId: number
}

interface Trainer {
  id: number
  name: string
  title: string
  photo: string | null
}

interface BookingFormData {
  name: string
  phone: string
  email: string
}

export default function Group() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date())
  const [classes, setClasses] = useState<GroupClass[]>([])
  const [trainers, setTrainers] = useState<Trainer[]>([])
  const [selectedClass, setSelectedClass] = useState<GroupClass | null>(null)
  const [showDetails, setShowDetails] = useState(false)
  const [showBookingForm, setShowBookingForm] = useState(false)
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [formData, setFormData] = useState<BookingFormData>({
    name: '',
    phone: '',
    email: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTrainers()
  }, [])

  useEffect(() => {
    fetchClasses(selectedDate)
  }, [selectedDate])

  const fetchTrainers = async () => {
    try {
      const response = await fetch(`http://localhost:8002/api/trainers`)
      if (!response.ok) throw new Error('Failed to fetch trainers')
      const data: Trainer[] = await response.json()
      setTrainers(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch trainers')
    }
  }

  const fetchClasses = async (date: Date) => {
    try {
      setLoading(true)
      const formattedDate = format(date, 'yyyy-MM-dd')
      const response = await fetch(`http://localhost:8002/api/group-classes?date=${formattedDate}`)
      if (!response.ok) throw new Error('Failed to fetch classes')
      const data: GroupClass[] = await response.json()
      setClasses(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch classes')
    } finally {
      setLoading(false)
    }
  }

  const handleClassClick = (groupClass: GroupClass) => {
    setSelectedClass(groupClass)
    setShowDetails(true)
  }

  const handleBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8002/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          classId: selectedClass?.id,
          date: format(selectedDate, 'yyyy-MM-dd'),
          ...formData
        }),
      })
      if (!response.ok) throw new Error('Booking failed')
      setShowBookingForm(false)
      setShowConfirmation(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while confirming the booking')
    } finally {
      setLoading(false)
    }
  }

  const renderCalendarHeader = () => (
    <div className="flex items-center justify-between p-4 border-b">
      <Button
        variant="ghost"
        onClick={() => {
          const prevMonth = new Date(selectedDate)
          prevMonth.setMonth(prevMonth.getMonth() - 1)
          setSelectedDate(prevMonth)
        }}
      >
        <ChevronLeft className="h-4 w-4" />
      </Button>
      <h2 className="text-lg font-semibold">
        {format(selectedDate, 'LLLL yyyy', { locale: ru })}
      </h2>
      <Button
        variant="ghost"
        onClick={() => {
          const nextMonth = new Date(selectedDate)
          nextMonth.setMonth(nextMonth.getMonth() + 1)
          setSelectedDate(nextMonth)
        }}
      >
        <ChevronRight className="h-4 w-4" />
      </Button>
    </div>
  )

  const renderClassCard = (groupClass: GroupClass) => {
    const trainer = trainers.find(t => t.id === groupClass.trainerId)
    return (
      <Card 
        key={groupClass.id}
        className="cursor-pointer hover:bg-accent transition-colors"
        onClick={() => handleClassClick(groupClass)}
      >
        <CardContent className="p-4">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Clock className="h-4 w-4" />
                {groupClass.time}
              </div>
              <h3 className="font-semibold mb-1">{groupClass.name}</h3>
              <p className="text-sm text-muted-foreground mb-2">{groupClass.duration}</p>
              <div className="flex items-center gap-2">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={trainer?.photo || ''} alt={trainer?.name} />
                  <AvatarFallback><User className="h-4 w-4" /></AvatarFallback>
                </Avatar>
                <div className="text-sm">
                  <div>{trainer?.name}</div>
                  <div className="text-muted-foreground">{trainer?.title}</div>
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium">{groupClass.price} ₽</div>
              <div className="text-sm text-muted-foreground mt-1">
                Осталось {groupClass.availableSpots} мест
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  const renderClassDetails = () => {
    const trainer = trainers.find(t => t.id === selectedClass?.trainerId)
    return (
      <Dialog open={showDetails} onOpenChange={setShowDetails}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{selectedClass?.name}</DialogTitle>
            <DialogDescription>
              <div className="grid gap-4 py-4">
                <div className="flex items-center gap-4">
                  <Avatar className="h-12 w-12">
                    <AvatarImage src={trainer?.photo || ''} alt={trainer?.name} />
                    <AvatarFallback><User className="h-6 w-6" /></AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="font-medium">{trainer?.name}</div>
                    <div className="text-sm text-muted-foreground">{trainer?.title}</div>
                  </div>
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span>{selectedClass?.duration}</span>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Осталось {selectedClass?.availableSpots} мест
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">{selectedClass?.description}</p>
                <div className="flex justify-between items-center">
                  <div className="text-lg font-semibold">{selectedClass?.price} ₽</div>
                  <Button onClick={() => {
                    setShowDetails(false)
                    setShowBookingForm(true)
                  }}>
                    Продолжить
                  </Button>
                </div>
              </div>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    )
  }

  const renderBookingForm = () => (
    <Dialog open={showBookingForm} onOpenChange={setShowBookingForm}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Заполните данные для записи</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleBookingSubmit} className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="name">Имя</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              required
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="phone">Телефон</Label>
            <Input
              id="phone"
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
              required
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              required
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? 'Отправка...' : 'Записаться'}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )

  const renderConfirmation = () => (
    <Dialog open={showConfirmation} onOpenChange={setShowConfirmation}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Запись подтверждена</DialogTitle>
          <DialogDescription>
            <div className="grid gap-4 py-4">
              <p>Вы успешно записаны на {selectedClass?.name}</p>
              <p>Дата: {format(selectedDate, 'd MMMM yyyy', { locale: ru })}</p>
              <p>Время: {selectedClass?.time}</p>
              <Button onClick={() => setShowConfirmation(false)}>
                Закрыть
              </Button>
            </div>
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  )

  if (loading && classes.length === 0) {
    return <div className="flex justify-center items-center min-h-screen">Загрузка...</div>
  }

  if (error) {
    return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>
  }

  return (
    <main className="container mx-auto p-4 max-w-3xl">
      {renderCalendarHeader()}
      <Calendar
        mode="single"
        selected={selectedDate}
        onSelect={(date) => {
          if (date) {
            setSelectedDate(date)
          }
        }}
        className="rounded-md border"
        locale={ru}
      />
      <div className="space-y-4 mt-6">
        {classes.map(renderClassCard)}
      </div>
      {selectedClass && renderClassDetails()}
      {renderBookingForm()}
      {renderConfirmation()}
    </main>
  )
}