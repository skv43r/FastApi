'use client'

import { useState } from 'react'
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
}

interface ServiceProvider {
  id: string
  name: string
  avatar: string
  specialization: string
}

interface TimeSlot {
  time: string
  available: boolean
}

interface GroupClass {
  id: string
  name: string
  date: Date
  time: string
  duration: number
  capacity: number
  booked: number
}

const services: Service[] = [
  { id: '1', name: 'Individual Training', duration: 60, price: 80, category: 'training' },
  { id: '2', name: 'Massage Therapy', duration: 60, price: 70, category: 'massage' },
  { id: '3', name: 'Sports Massage', duration: 45, price: 60, category: 'massage' },
  { id: '4', name: 'Personal Fitness Session', duration: 45, price: 65, category: 'training' },
]

const serviceProviders: ServiceProvider[] = [
  { id: '1', name: 'John Smith', avatar: '/placeholder.svg?height=100&width=100', specialization: 'Personal Trainer' },
  { id: '2', name: 'Sarah Johnson', avatar: '/placeholder.svg?height=100&width=100', specialization: 'Massage Therapist' },
  { id: '3', name: 'Mike Wilson', avatar: '/placeholder.svg?height=100&width=100', specialization: 'Personal Trainer' },
]

const timeSlots: TimeSlot[] = [
  { time: '09:00', available: true },
  { time: '10:00', available: true },
  { time: '11:00', available: false },
  { time: '12:00', available: true },
  { time: '13:00', available: true },
  { time: '14:00', available: false },
  { time: '15:00', available: true },
  { time: '16:00', available: true },
  { time: '17:00', available: true },
]

const groupClasses: GroupClass[] = [
  { id: '1', name: 'Yoga Class', date: new Date(2024, 10, 27), time: '10:00', duration: 60, capacity: 20, booked: 15 },
  { id: '2', name: 'HIIT Workout', date: new Date(2024, 10, 27), time: '14:00', duration: 45, capacity: 15, booked: 10 },
  { id: '3', name: 'Pilates', date: new Date(2024, 10, 28), time: '11:00', duration: 60, capacity: 12, booked: 8 },
]

type BookingStep = 'serviceType' | 'category' | 'service' | 'provider' | 'datetime' | 'groupClass' | 'confirmation'

export function BlockPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState<BookingStep>('serviceType')
  const [selectedServiceType, setSelectedServiceType] = useState<'individual' | 'group' | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [selectedService, setSelectedService] = useState<Service | null>(null)
  const [selectedProvider, setSelectedProvider] = useState<ServiceProvider | null>(null)
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined)
  const [selectedTime, setSelectedTime] = useState<string>('')
  const [selectedGroupClass, setSelectedGroupClass] = useState<GroupClass | null>(null)

  const handleServiceTypeSelect = (type: 'individual' | 'group') => {
    setSelectedServiceType(type)
    if (type === 'individual') {
      setCurrentStep('category')
    } else {
      setCurrentStep('groupClass')
    }
  }

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category)
    setCurrentStep('service')
  }

  const handleServiceSelect = (service: Service) => {
    setSelectedService(service)
    setCurrentStep('provider')
  }

  const handleProviderSelect = (provider: ServiceProvider) => {
    setSelectedProvider(provider)
    setCurrentStep('datetime')
  }

  const handleTimeSelect = (time: string) => {
    setSelectedTime(time)
    setCurrentStep('confirmation')
  }

  const handleGroupClassSelect = (groupClass: GroupClass) => {
    setSelectedGroupClass(groupClass)
    setCurrentStep('confirmation')
  }

  const handleConfirmBooking = async () => {
    try {
      // Here you would typically make an API call to save the booking
      const response = await fetch('http://localhost:8002/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(
          selectedServiceType === 'individual'
            ? {
                serviceId: selectedService?.id,
                providerId: selectedProvider?.id,
                date: selectedDate,
                time: selectedTime,
              }
            : {
                groupClassId: selectedGroupClass?.id,
              }
        ),
      })
      if (!response.ok) {
        throw new Error('Booking failed')
      }
      // Booking successful, you can handle the response here
    } catch (error) {
      console.error('Booking failed:', error)
      // Handle error (e.g., show error message to user)
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
      <Card 
        className="cursor-pointer hover:bg-accent transition-colors"
        onClick={() => handleCategorySelect('training')}
      >
        <CardContent className="flex items-center justify-between p-6">
          <div className="flex items-center gap-4">
            <User2 className="h-8 w-8" />
            <div>
              <CardTitle>Individual Training</CardTitle>
              <p className="text-sm text-muted-foreground">Personal training sessions</p>
            </div>
          </div>
          <ChevronRight className="h-5 w-5" />
        </CardContent>
      </Card>
      <Card 
        className="cursor-pointer hover:bg-accent transition-colors"
        onClick={() => handleCategorySelect('massage')}
      >
        <CardContent className="flex items-center justify-between p-6">
          <div className="flex items-center gap-4">
            <Massage className="h-8 w-8" />
            <div>
              <CardTitle>Massage Services</CardTitle>
              <p className="text-sm text-muted-foreground">Therapeutic massage sessions</p>
            </div>
          </div>
          <ChevronRight className="h-5 w-5" />
        </CardContent>
      </Card>
    </div>
  )

  const renderServiceSelection = () => (
    <ScrollArea className="h-[600px] pr-4">
      <div className="space-y-4">
        {services
          .filter(service => service.category === selectedCategory)
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

  const renderProviderSelection = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {serviceProviders.map(provider => (
        <Card 
          key={provider.id}
          className="cursor-pointer hover:bg-accent transition-colors"
          onClick={() => handleProviderSelect(provider)}
        >
          <CardContent className="flex flex-col items-center gap-4 p-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={provider.avatar} alt={provider.name} />
              <AvatarFallback>{provider.name[0]}</AvatarFallback>
            </Avatar>
            <div className="text-center">
              <CardTitle>{provider.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{provider.specialization}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )

  const renderDateTimeSelection = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Select Date</CardTitle>
        </CardHeader>
        <CardContent>
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={setSelectedDate}
            className="rounded-md border"
          />
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Select Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-2">
            {timeSlots.map((slot, index) => (
              <Button
                key={index}
                variant={slot.available ? "outline" : "ghost"}
                disabled={!slot.available}
                onClick={() => handleTimeSelect(slot.time)}
                className={selectedTime === slot.time ? "border-primary" : ""}
              >
                <Clock className="mr-2 h-4 w-4" />
                {slot.time}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderGroupClassSelection = () => (
    <div className="space-y-6">
      <Calendar
        mode="single"
        selected={selectedDate}
        onSelect={setSelectedDate}
        className="rounded-md border"
      />
      <ScrollArea className="h-[400px]">
        <div className="space-y-4">
          {groupClasses
            .filter(groupClass => 
              selectedDate ? groupClass.date.toDateString() === selectedDate.toDateString() : true
            )
            .map(groupClass => (
              <Card 
                key={groupClass.id}
                className="cursor-pointer hover:bg-accent transition-colors"
                onClick={() => handleGroupClassSelect(groupClass)}
              >
                <CardContent className="flex items-center justify-between p-6">
                  <div>
                    <CardTitle>{groupClass.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {groupClass.date.toLocaleDateString()} at {groupClass.time} • {groupClass.duration} minutes
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {groupClass.booked}/{groupClass.capacity} spots booked
                    </p>
                  </div>
                  <ChevronRight className="h-5 w-5" />
                </CardContent>
              </Card>
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
        {selectedServiceType === 'individual' ? (
          <>
            <div className="space-y-2">
              <p className="font-medium">Service:</p>
              <p className="text-muted-foreground">{selectedService?.name}</p>
            </div>
            <div className="space-y-2">
              <p className="font-medium">Provider:</p>
              <p className="text-muted-foreground">{selectedProvider?.name}</p>
            </div>
            <div className="space-y-2">
              <p className="font-medium">Date & Time:</p>
              <p className="text-muted-foreground">
                {selectedDate?.toLocaleDateString()} at {selectedTime}
              </p>
            </div>
          </>
        ) : (
          <>
            <div className="space-y-2">
              <p className="font-medium">Group Class:</p>
              <p className="text-muted-foreground">{selectedGroupClass?.name}</p>
            </div>
            <div className="space-y-2">
              <p className="font-medium">Date & Time:</p>
              <p className="text-muted-foreground">
                {selectedGroupClass?.date.toLocaleDateString()} at {selectedGroupClass?.time}
              </p>
            </div>
            <div className="space-y-2">
              <p className="font-medium">Duration:</p>
              <p className="text-muted-foreground">{selectedGroupClass?.duration} minutes</p>
            </div>
          </>
        )}
        <Button 
          className="w-full"
          onClick={handleConfirmBooking}
        >
          Confirm Booking
        </Button>
      </CardContent>
    </Card>
  )

  return (
    <main className="container mx-auto p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Book an Appointment</h1>
          <p className="text-muted-foreground">
            {currentStep === 'serviceType' && "Select a service type"}
            {currentStep === 'category' && "Select a service category"}
            {currentStep === 'service' && "Choose your service"}
            {currentStep === 'provider' && "Select your preferred provider"}
            {currentStep === 'datetime' && "Pick a date and time"}
            {currentStep === 'groupClass' && "Select a group class"}
            {currentStep === 'confirmation' && "Confirm your booking"}
          </p>
        </div>

        {currentStep === 'serviceType' && renderServiceTypeSelection()}
        {currentStep === 'category' && renderCategorySelection()}
        {currentStep === 'service' && renderServiceSelection()}
        {currentStep === 'provider' && renderProviderSelection()}
        {currentStep === 'datetime' && renderDateTimeSelection()}
        {currentStep === 'groupClass' && renderGroupClassSelection()}
        {currentStep === 'confirmation' && renderConfirmation()}

        {currentStep !== 'serviceType' && currentStep !== 'confirmation' && (
          <Button
            variant="outline"
            className="mt-6"
            onClick={() => {
              if (currentStep === 'category') setCurrentStep('serviceType')
              if (currentStep === 'service') setCurrentStep('category')
              if (currentStep === 'provider') setCurrentStep('service')
              if (currentStep === 'datetime') setCurrentStep('provider')
              if (currentStep === 'groupClass') setCurrentStep('serviceType')
            }}
          >
            Back
          </Button>
        )}
      </div>
    </main>
  )
}