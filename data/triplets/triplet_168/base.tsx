'use client'
import React from 'react'
<<<<<<< HEAD
import { Brain, Cloud, Shield, Zap, ArrowRight, CheckCircle, Star, TrendingUp, Users, Award, Clock, Globe, Check } from 'lucide-react';;

=======
import { Brain, Cloud, Shield, Zap, ArrowRight, CheckCircle } from 'lucide-react'
>>>>>>> origin/main
const EnhancedServicesShowcase: React.FC = () => {
  const services = [
    {
      title: 'AI Solutions',
      description: 'Transform your business with cutting-edge artificial intelligence',
      icon: Brain,
      color: 'text-purple-400',
      features: ['Machine Learning', 'Natural Language Processing', 'Computer Vision', 'Predictive Analytics'],
      stats: '300% ROI',
    },
    {
      title: 'IT Infrastructure',
      description: 'Build and maintain robust technology foundations',
      icon: Cloud,
      color: 'text-blue-400',
      features: ['Cloud Migration', 'Server Management', 'Network Security', 'Data Backup'],
      stats: '99.9% Uptime',
    },
    {
      title: 'Cybersecurity',
      description: 'Protect your business with enterprise-grade security',
      icon: Shield,
      color: 'text-green-400',
      features: ['Threat Detection', 'Security Audits', 'Compliance', 'Incident Response'],
      stats: 'Zero Breaches',
    },
    {
      title: 'Performance Optimization',
      description: 'Maximize efficiency and speed across all systems',
      icon: Zap,
      color: 'text-yellow-400',
      features: ['Code Optimization', 'Database Tuning', 'Caching Strategies', 'Load Balancing'],
      stats: '10x Faster'
    }
  ]

  return (
    <div className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Enhanced Services Showcase
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Discover our comprehensive range of technology services designed to accelerate your business growth.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 group"
            >
              <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <service.icon className="h-8 w-8 text-white" />
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 text-center">
                {service.title}
              </h3>
              
              <p className="text-gray-300 text-center mb-4">
                {service.description}
              </p>

              <div className="mb-4">
                <div className="text-2xl font-bold text-purple-400 text-center mb-2">
                  {service.stats}
                </div>
                <div className="text-sm text-gray-400 text-center">
                  Average Improvement
                </div>
              </div>

              <ul className="space-y-2 mb-6">
                {service.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                    <span className="text-gray-300 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <button className="w-full bg-gradient-to-r from-purple-500 to-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:from-purple-600 hover:to-blue-700 transition-all duration-300 flex items-center justify-center">
                Learn More
                <ArrowRight className="h-4 w-4 ml-2" />
              </button>
            </div>
<<<<<<< HEAD
          ))}
=======
<<<<<<< HEAD
          ))}
=======
<<<<<<< HEAD
          ))}
=======
<<<<<<< HEAD
          </div>
        ))}
=======
          ))}
>>>>>>> origin/main
>>>>>>> origin/main
>>>>>>> origin/main
>>>>>>> origin/main
        </div>
      </div>
    </div>
  )
}

export default EnhancedServicesShowcase