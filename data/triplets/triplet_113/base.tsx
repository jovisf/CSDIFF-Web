'use client';
<<<<<<< HEAD
import React from 'react';
import { Circle, ArrowRight, Brain, Globe, Cloud, Smartphone } from 'lucide-react';;
=======
import { Brain, Globe, ArrowRight, Smartphone, Circle, Cloud } from 'lucide-react';
>>>>>>> origin/main
const ServicesPage: React.FC = () => {
  const serviceCategories = [
  {
      title: 'AI Solutions',
      icon: Brain,
      description: 'Cutting-edge artificial intelligence solutions to transform your business operations.',
    services: [
        'AI Chatbots & Virtual Assistants',
        'Machine Learning Models',
        'Natural Language Processing',
        'Computer Vision',
        'Predictive Analytics',
    'AI Automation'
      ]
    },
    {
      title: 'IT Services',
      icon: Cloud,
      description: 'Comprehensive IT services to modernize your infrastructure and operations.',
    services: [
        'Cloud Migration & Management',
        'Cybersecurity Solutions',
        'DevOps & CI/CD',
        'Database Management',
        'Network Infrastructure',
    'IT Support & Maintenance'
      ]
    },
    {
      title: 'Web Development',
      icon: Globe,
      description: 'Custom web applications and websites built with modern technologies.',
    services: [
        'React & Next.js Applications',
        'E-commerce Solutions',
        'Progressive Web Apps',
        'API Development',
        'Mobile-First Design',
    'Performance Optimization'
      ]
    },
    {
      title: 'Mobile Development',
      icon: Smartphone,
      description: 'Native and cross-platform mobile applications for iOS and Android.',
    services: [
        'iOS App Development',
        'Android App Development',
        'React Native Apps',
        'Flutter Applications',
        'App Store Optimization',
    'Mobile UI/UX Design'
  ]
}
  ]
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 pt-16">
      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md: text-6xl font-bold text-white mb-6">
            Our <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Services</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            We provide comprehensive AI and IT solutions to help your business thrive in the digital age.
          </p>
          <div className="flex flex-col sm: flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-cyan-500 to-purple-500 hover: from-cyan-600 hover:to-purple-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center">
              Get Started
              <ArrowRight className="w-8 h-8" />
            </button>
            <button className="border-2 border-cyan-400 text-cyan-400 hover: bg-cyan-400 hover:text-white font-bold py-4 px-8 rounded-lg transition-all duration-300 flex items-center justify-center">
              View Portfolio
            </button>
          </div>
        </div>
      </section>
      {/* Services Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md: grid-cols-2 gap-8">
            {serviceCategories.map((category, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-8 hover: bg-white/20 transition-all duration-300">
                <div className="flex items-center mb-6">
                  <category.icon className="w-8 h-8 text-cyan-400" />
                  <h3 className="text-2xl font-bold text-white ml-4">{category.title}</h3>
                </div>
                <p className="text-gray-300 mb-6">{category.description}</p>
                <ul className="space-y-3">
                  {category.services.map((service, idx) => (
                    <li key={idx} className="flex items-center text-gray-300">
                      <Circle className="w-8 h-8" />
                      {service}
                    </li>
                  ))}
                </ul>
                <button className="mt-6 text-cyan-400 hover: text-cyan-300 font-semibold flex items-center">
                  Learn More
                  <ArrowRight className="w-8 h-8" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-sm rounded-2xl p-12">
            <h2 className="text-4xl font-bold text-white mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Let's discuss your project and see how we can help you achieve your goals.
            </p>
            <div className="flex flex-col sm: flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-cyan-500 to-purple-500 hover: from-cyan-600 hover:to-purple-600 text-white font-bold py-4 px-8 rounded-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center">
                Contact Us
                <ArrowRight className="w-8 h-8" />
              </button>
              <button className="border-2 border-white text-white hover: bg-white hover:text-gray-900 font-bold py-4 px-8 rounded-lg transition-all duration-300 flex items-center justify-center">
                Schedule Call
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
export default ServicesPage