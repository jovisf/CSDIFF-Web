'use client'
import React, { useState, useEffect } from 'react'
<<<<<<< HEAD
import { Cloud, Zap, Shield, Globe, Brain, Star } from 'lucide-react';

=======
import { Zap, Brain, Globe, Shield } from 'lucide-react'
>>>>>>> origin/main
const DynamicContentShowcase: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0)

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Solutions',
      description: 'Advanced AI technology to transform your business operations and improve efficiency',
      color: 'from-purple-500 to-pink-600'
    },
    {
      icon: Zap,
      title: 'High Performance',
      description: 'Lightning-fast processing and real-time analytics for optimal results',
      color: 'from-blue-500 to-cyan-600'
    },
    {
      icon: Shield,
      title: 'Enterprise Security',
      description: 'Bank-level security with encryption and compliance standards',
      color: 'from-green-500 to-emerald-600'
    },
    {
      icon: Globe,
      title: 'Global Reach',
      description: 'Worldwide deployment and support for international businesses',
      color: 'from-orange-500 to-red-600'
    }
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % features.length)
    }, 3000)

    return () => clearInterval(timer)
  }, [features.length])

  const currentFeature = features[currentIndex]

  return (
    <div className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Dynamic Content Showcase
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Experience our cutting-edge solutions through interactive demonstrations and real-time updates.
          </p>
        </div>

        <div className="relative">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 md:p-12 border border-white/20">
            <div className="flex items-center justify-center mb-8">
              <div className={`bg-gradient-to-r ${currentFeature.color} p-4 rounded-full`}>
                <currentFeature.icon className="h-12 w-12 text-white" />
              </div>
            </div>
            
            <h3 className="text-2xl md:text-3xl font-bold text-white text-center mb-4">
              {currentFeature.title}
            </h3>
            
            <p className="text-lg text-gray-300 text-center mb-8 max-w-2xl mx-auto">
              {currentFeature.description}
            </p>

            <div className="flex justify-center space-x-2 mb-8">
              {features.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentIndex(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentIndex ? 'bg-white' : 'bg-white/30'
                  }`}
                />
              ))}
            </div>

            <div className="text-center">
              <button className="bg-gradient-to-r from-purple-500 to-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-600 hover:to-blue-700 transition-all duration-300">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DynamicContentShowcase