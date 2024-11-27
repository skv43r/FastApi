'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ChevronRight, Clock, CalendarIcon, User2, Users, Scissors, GiftIcon as Massage } from 'lucide-react'

interface Service {
  id: string
  name: string
  duration: number
  price: number
  category: string
  type: 'individual' | 'group'
}

interface Trainer {
  id: string
  name: string
  avatar: string
  specialization: string
}

interface TimeSlot {
  id: string
  date: string
  time: string
  available: boolean
  serviceId: string
  trainerId: string
}

export function BlockPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState<'serviceType' | 'category' | 'service' | 'trainer' | 'datetime' | 'confirmation'>('serviceType')
  const [selectedServiceType, setSelectedServiceType] = useState<'individual' | 'group' | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [selectedService, setSelectedService] = useState<Service | null>(null)
  const [selectedTrainer, setSelectedTrainer] = useState<Trainer | null>(null)
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined)
  const [selectedTimeSlot, setSelectedTimeSlot] = useState<TimeSlot | null>(null)

  const [services, setServices] = useState<Service[]>([])
  const [trainers, setTrainers] = useState<Trainer[]>([])
  const [timeSlots, setTimeSlots] = useState<TimeSlot[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchServices()
  }, [])

  const fetchServices = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8002/api/services')
      if (!response.ok) {
        throw new Error('Failed to fetch services')
      }
      const data = await response.json()
      setServices(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while fetching services')
    } finally {
      setLoading(false)
    }
  }

  const fetchTrainers = async (serviceId: string) => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8002/api/trainers?serviceId=${serviceId}`)
      if (!response.ok) {
        throw new Error('Failed to fetch trainers')
      }
      const data = await response.json()
      setTrainers(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while fetching trainers')
    } finally {
      setLoading(false)
    }
  }

  const fetchTimeSlots = async (serviceId: string, trainerId: string) => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8002/api/timeslots?serviceId=${serviceId}&trainerId=${trainerId}`)
      if (!response.ok) {
        throw new Error('Failed to fetch time slots')
      }
      const data = await response.json()
      setTimeSlots(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while fetching time slots')
    } finally {
      setLoading(false)
    }
  }

  const handleServiceTypeSelect = (type: 'individual' | 'group') => {
    setSelectedServiceType(type)
    setCurrentStep('category')
  }

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category)
    setCurrentStep('service')
  }

  const handleServiceSelect = (service: Service) => {
    setSelectedService(service)
    fetchTrainers(service.id)
    setCurrentStep('trainer')
  }

  const handleTrainerSelect = (trainer: Trainer) => {
    setSelectedTrainer(trainer)
    if (selectedService) {
      fetchTimeSlots(selectedService.id, trainer.id)
    }
    setCurrentStep('datetime')
  }

  const handleTimeSlotSelect = (timeSlot: TimeSlot) => {
    setSelectedTimeSlot(timeSlot)
    setCurrentStep('confirmation')
  }

  const handleConfirmBooking = async () => {
    if (!selectedService || !selectedTrainer || !selectedTimeSlot) {
      setError('Please complete all booking steps before confirming')
      return
    }

    try {
      const response = await fetch('http://localhost:8002/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          serviceId: selectedService.id,
          trainerId: selectedTrainer.id,
          timeSlotId: selectedTimeSlot.id,
        }),
      })
      if (!response.ok) {
        throw new Error('Booking failed')
      }
      // Booking successful, you can handle the response here
      router.push('/booking-success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while confirming the booking')
    }
  }

  const renderServiceTypeSelection = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card 
        className="cursor-pointer hover:bg-accent transition-colors"
        onClick={() => handleServiceTypeSelect('individual')}
      >
        <CardContent className="flex items-center justify-between p-6">
          <div className="flex items-center gap-4">
            <User2 className="h-8 w-8" />
            <div>
              <CardTitle>Individual Services</CardTitle>
              <p className="text-sm text-muted-foreground">Personal training and massage</p>
            </div>
          </div>
          <ChevronRight className="h-5 w-5" />
        </CardContent>
      </Card>
      <Card 
        className="cursor-pointer hover:bg-accent transition-colors"
        onClick={() => handleServiceTypeSelect('group')}
      >
        <CardContent className="flex items-center justify-between p-6">
          <div className="flex items-center gap-4">
            <Users className="h-8 w-8" />
            <div>
              <CardTitle>Group Classes</CardTitle>
              <p className="text-sm text-muted-foreground">Join group fitness sessions</p>
            </div>
          </div>
          <ChevronRight className="h-5 w-5" />
        </CardContent>
      </Card>
    </div>
  )

  const renderCategorySelection = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {['training', 'massage'].map(category => (
        <Card 
          key={category}
          className="cursor-pointer hover:bg-accent transition-colors"
          onClick={() => handleCategorySelect(category)}
        >
          <CardContent className="flex items-center justify-between p-6">
            <div className="flex items-center gap-4">
              {category === 'training' ? <User2 className="h-8 w-8" /> : <Massage className="h-8 w-8" />}
              <div>
                <CardTitle>{category === 'training' ? 'Individual Training' : 'Massage Services'}</CardTitle>
                <p className="text-sm text-muted-foreground">
                  {category === 'training' ? 'Personal training sessions' : 'Therapeutic massage sessions'}
                </p>
              </div>
            </div>
            <ChevronRight className="h-5 w-5" />
          </CardContent>
        </Card>
      ))}
    </div>
  )

  const renderServiceSelection = () => (
    <ScrollArea className="h-[600px] pr-4">
      <div className="space-y-4">
        {services
          .filter(service => service.category === selectedCategory && service.type === selectedServiceType)
          .map(service => (
            <Card 
              key={service.id}
              className="cursor-pointer hover:bg-accent transition-colors"
              onClick={() => handleServiceSelect(service)}
            >
              <CardContent className="flex items-center justify-between p-6">
                <div>
                  <CardTitle>{service.name}</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    {service.duration} minutes • ${service.price}
                  </p>
                </div>
                <ChevronRight className="h-5 w-5" />
              </CardContent>
            </Card>
          ))}
      </div>
    </ScrollArea>
  )

  const renderTrainerSelection = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {trainers.map(trainer => (
        <Card 
          key={trainer.id}
          className="cursor-pointer hover:bg-accent transition-colors"
          onClick={() => handleTrainerSelect(trainer)}
        >
          <CardContent className="flex flex-col items-center gap-4 p-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={trainer.avatar} alt={trainer.name} />
              <AvatarFallback>{trainer.name[0]}</AvatarFallback>
            </Avatar>
            <div className="text-center">
              <CardTitle>{trainer.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{trainer.specialization}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )

  const renderDateTimeSelection = () => (
    <div className="space-y-6">
      <Calendar
        mode="single"
        selected={selectedDate}
        onSelect={setSelectedDate}
        className="rounded-md border"
      />
      <ScrollArea className="h-[300px]">
        <div className="grid grid-cols-2 gap-2">
          {timeSlots
            .filter(slot => selectedDate ? new Date(slot.date).toDateString() === selectedDate.toDateString() : true)
            .map((slot) => (
              <Button
                key={slot.id}
                variant={slot.available ? "outline" : "ghost"}
                disabled={!slot.available}
                onClick={() => handleTimeSlotSelect(slot)}
                className={selectedTimeSlot?.id === slot.id ? "border-primary" : ""}
              >
                <Clock className="mr-2 h-4 w-4" />
                {slot.time}
              </Button>
            ))}
        </div>
      </ScrollArea>
    </div>
  )

  const renderConfirmation = () => (
    <Card>
      <CardHeader>
        <CardTitle>Booking Confirmation</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <p className="font-medium">Service:</p>
          <p className="text-muted-foreground">{selectedService?.name}</p>
        </div>
        <div className="space-y-2">
          <p className="font-medium">Trainer:</p>
          <p className="text-muted-foreground">{selectedTrainer?.name}</p>
        </div>
        <div className="space-y-2">
          <p className="font-medium">Date & Time:</p>
          <p className="text-muted-foreground">
            {selectedTimeSlot ? `${new Date(selectedTimeSlot.date).toLocaleDateString()} at ${selectedTimeSlot.time}` : 'Not selected'}
          </p>
        </div>
        <Button 
          className="w-full"
          onClick={handleConfirmBooking}
        >
          Confirm Booking
        </Button>
      </CardContent>
    </Card>
  )

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">{error}</div>
  }

  return (
    <main className="container mx-auto p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Book an Appointment</h1>
          <p className="text-muted-foreground">
            {currentStep === 'serviceType' && "Select a service type"}
            {currentStep === 'category' && "Select a service category"}
            {currentStep === 'service' && "Choose your service"}
            {currentStep === 'trainer' && "Select your preferred trainer"}
            {currentStep === 'datetime' && "Pick a date and time"}
            {currentStep === 'confirmation' && "Confirm your booking"}
          </p>
        </div>

        {currentStep === 'serviceType' && renderServiceTypeSelection()}
        {currentStep === 'category' && renderCategorySelection()}
        {currentStep === 'service' && renderServiceSelection()}
        {currentStep === 'trainer' && renderTrainerSelection()}
        {currentStep === 'datetime' && renderDateTimeSelection()}
        {currentStep === 'confirmation' && renderConfirmation()}

        {currentStep !== 'serviceType' && currentStep !== 'confirmation' && (
          <Button
            variant="outline"
            className="mt-6"
            onClick={() => {
              if (currentStep === 'category') setCurrentStep('serviceType')
              if (currentStep === 'service') setCurrentStep('category')
              if (currentStep === 'trainer') setCurrentStep('service')
              if (currentStep === 'datetime') setCurrentStep('trainer')
            }}
          >
            Back
          </Button>
        )}
      </div>
    </main>
  )
}