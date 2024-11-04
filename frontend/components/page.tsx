'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { PlusCircle } from "lucide-react"

interface User {
  id: number
  name: string
  email: string
  avatar: string
}

interface ApiResponse {
  users: User[]
}

export function PageComponent() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [newUser, setNewUser] = useState({ name: '', email: '', avatar: '' })

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/return')
      if (!response.ok) {
        throw new Error('Failed to fetch data')
      }
      const data: ApiResponse = await response.json()
      setUsers(data.users)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setNewUser(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log(newUser);
    try {
      const response = await fetch('http://localhost:8000/api/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      })
      if (!response.ok) {
        throw new Error('Failed to add user')
      }
      await fetchUsers() // Refresh the user list
      setNewUser({ name: '', email: '', avatar: '' }) // Reset form
      setIsDialogOpen(false) // Close the dialog
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add user')
    }
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Card className="w-[300px]">
          <CardHeader>
            <CardTitle className="text-center text-red-500">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-center">{error}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <main className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Users</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" size="icon">
              <PlusCircle className="h-6 w-6" />
              <span className="sr-only">Add new user</span>
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New User</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  name="name"
                  value={newUser.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={newUser.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div>
                <Label htmlFor="avatar">Avatar URL</Label>
                <Input
                  id="avatar"
                  name="avatar"
                  type="url"
                  value={newUser.avatar}
                  onChange={handleInputChange}
                />
              </div>
              <Button type="submit">Add User</Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading
          ? Array(6).fill(0).map((_, index) => (
              <Card key={index} className="overflow-hidden">
                <CardHeader className="pb-0">
                  <Skeleton className="h-12 w-12 rounded-full mx-auto" />
                </CardHeader>
                <CardContent className="pb-6 space-y-2">
                  <Skeleton className="h-4 w-3/4 mx-auto" />
                  <Skeleton className="h-4 w-1/2 mx-auto" />
                </CardContent>
              </Card>
            ))
          : users.map((user) => (
              <Card key={user.id} className="overflow-hidden">
                <CardHeader className="pb-0">
                  <Avatar className="w-24 h-24 mx-auto">
                    <AvatarImage src={user.avatar} alt={`${user.name}'s avatar`} />
                    <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                </CardHeader>
                <CardContent className="text-center pb-6">
                  <CardTitle className="mb-2">{user.name}</CardTitle>
                  <p className="text-sm text-muted-foreground">{user.email}</p>
                </CardContent>
              </Card>
            ))}
      </div>
    </main>
  )
}